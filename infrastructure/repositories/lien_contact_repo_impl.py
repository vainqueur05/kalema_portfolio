"""
Implémentation du Repository LienContact
=========================================
Adaptateur concret entre le domaine et la persistance SQLAlchemy.
Implémente l'interface LienContactRepository.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.lien_contact import LienContact
from application.interfaces.repositories.lien_contact_repo import LienContactRepository
from infrastructure.database.models import LienContactModel


class LienContactRepositoryImpl(LienContactRepository):
    """
    Implémentation SQLAlchemy pour la gestion des liens de contact.

    Attributes:
        db (Session): Session SQLAlchemy injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self, actif_seulement: bool = False) -> List[LienContact]:
        """Retourne tous les liens, triés par ordre."""
        query = self.db.query(LienContactModel)
        if actif_seulement:
            query = query.filter(LienContactModel.actif == True)
        liens_db = query.order_by(LienContactModel.ordre.asc()).all()
        return [self._to_entity(lien) for lien in liens_db]

    def recuperer_par_id(self, id: int) -> Optional[LienContact]:
        """Récupère un lien par son ID."""
        lien_db = self.db.query(LienContactModel).filter(LienContactModel.id == id).first()
        if not lien_db:
            return None
        return self._to_entity(lien_db)

    def ajouter(self, lien: LienContact) -> LienContact:
        """Ajoute un nouveau lien."""
        lien_db = LienContactModel(
            nom=lien.nom,
            url=lien.url,
            icone=lien.icone,
            actif=lien.actif,
            ordre=lien.ordre,
        )
        self.db.add(lien_db)
        self.db.commit()
        self.db.refresh(lien_db)
        return self._to_entity(lien_db)

    def mettre_a_jour(self, lien: LienContact) -> LienContact:
        """Met à jour un lien existant (basé sur l'id de l'entité)."""
        lien_db = self.db.query(LienContactModel).filter(LienContactModel.id == lien.id).first()
        if not lien_db:
            raise ValueError(f"Lien de contact avec id {lien.id} introuvable.")
        lien_db.nom = lien.nom
        lien_db.url = lien.url
        lien_db.icone = lien.icone
        lien_db.actif = lien.actif
        lien_db.ordre = lien.ordre
        self.db.commit()
        self.db.refresh(lien_db)
        return self._to_entity(lien_db)

    def supprimer(self, id: int) -> None:
        """Supprime un lien par son ID."""
        lien_db = self.db.query(LienContactModel).filter(LienContactModel.id == id).first()
        if lien_db:
            self.db.delete(lien_db)
            self.db.commit()

    def basculer_actif(self, id: int) -> Optional[LienContact]:
        """Inverse l'état actif/inactif."""
        lien_db = self.db.query(LienContactModel).filter(LienContactModel.id == id).first()
        if not lien_db:
            return None
        lien_db.actif = not lien_db.actif
        self.db.commit()
        self.db.refresh(lien_db)
        return self._to_entity(lien_db)

    def _to_entity(self, model: LienContactModel) -> LienContact:
        """Mappe le modèle SQLAlchemy vers l'entité domaine."""
        return LienContact(
            id=model.id,
            nom=model.nom,
            url=model.url,
            icone=model.icone,
            actif=model.actif,
            ordre=model.ordre,
        )