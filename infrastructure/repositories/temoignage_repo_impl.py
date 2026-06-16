"""
Implémentation du Repository Temoignage
========================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface TemoignageRepository avec SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.temoignage import Temoignage
from application.interfaces.repositories.temoignage_repo import TemoignageRepository
from infrastructure.database.models import TemoignageModel


class TemoignageRepositoryImpl(TemoignageRepository):
    """
    Implémentation SQLAlchemy pour la gestion des témoignages.

    Attributes:
        db (Session): Session de base de données injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self, actif_seulement: bool = False) -> List[Temoignage]:
        """Retourne tous les témoignages, triés par ordre."""
        query = self.db.query(TemoignageModel)
        if actif_seulement:
            query = query.filter(TemoignageModel.actif == True)
        temoignages_db = query.order_by(TemoignageModel.ordre.asc()).all()
        return [self._to_entity(t) for t in temoignages_db]

    def recuperer_par_id(self, id: int) -> Optional[Temoignage]:
        """Récupère un témoignage par son ID."""
        temoignage_db = self.db.query(TemoignageModel).filter(TemoignageModel.id == id).first()
        if not temoignage_db:
            return None
        return self._to_entity(temoignage_db)

    def ajouter(self, temoignage: Temoignage) -> Temoignage:
        """Ajoute un nouveau témoignage."""
        temoignage_db = TemoignageModel(
            nom=temoignage.nom,
            texte=temoignage.texte,
            photo_url=temoignage.photo_url,
            entreprise=temoignage.entreprise,
            actif=temoignage.actif,
            ordre=temoignage.ordre,
        )
        self.db.add(temoignage_db)
        self.db.commit()
        self.db.refresh(temoignage_db)
        return self._to_entity(temoignage_db)

    def mettre_a_jour(self, temoignage: Temoignage) -> Temoignage:
        """Met à jour un témoignage existant."""
        temoignage_db = self.db.query(TemoignageModel).filter(TemoignageModel.id == temoignage.id).first()
        if not temoignage_db:
            raise ValueError(f"Témoignage avec id {temoignage.id} introuvable.")
        temoignage_db.nom = temoignage.nom
        temoignage_db.texte = temoignage.texte
        temoignage_db.photo_url = temoignage.photo_url
        temoignage_db.entreprise = temoignage.entreprise
        temoignage_db.actif = temoignage.actif
        temoignage_db.ordre = temoignage.ordre
        self.db.commit()
        self.db.refresh(temoignage_db)
        return self._to_entity(temoignage_db)

    def supprimer(self, id: int) -> None:
        """Supprime un témoignage par son ID."""
        temoignage_db = self.db.query(TemoignageModel).filter(TemoignageModel.id == id).first()
        if temoignage_db:
            self.db.delete(temoignage_db)
            self.db.commit()

    def basculer_actif(self, id: int) -> Optional[Temoignage]:
        """Inverse l'état actif/inactif."""
        temoignage_db = self.db.query(TemoignageModel).filter(TemoignageModel.id == id).first()
        if not temoignage_db:
            return None
        temoignage_db.actif = not temoignage_db.actif
        self.db.commit()
        self.db.refresh(temoignage_db)
        return self._to_entity(temoignage_db)

    def _to_entity(self, model: TemoignageModel) -> Temoignage:
        """Mappe le modèle SQLAlchemy vers l'entité domaine."""
        return Temoignage(
            id=model.id,
            nom=model.nom,
            texte=model.texte,
            photo_url=model.photo_url,
            entreprise=model.entreprise,
            actif=model.actif,
            ordre=model.ordre,
        )