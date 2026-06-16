"""
Implémentation du Repository Projet
=====================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface ProjetRepository avec SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.projet import Projet
from application.interfaces.repositories.projet_repo import ProjetRepository
from infrastructure.database.models import ProjetModel


class ProjetRepositoryImpl(ProjetRepository):
    """
    Implémentation SQLAlchemy pour la gestion des projets.

    Attributes:
        db (Session): Session de base de données injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self, actif_seulement: bool = False) -> List[Projet]:
        """
        Retourne la liste des projets, triés par ordre croissant.
        """
        query = self.db.query(ProjetModel)
        if actif_seulement:
            query = query.filter(ProjetModel.actif == True)
        projets_db = query.order_by(ProjetModel.ordre.asc()).all()
        return [self._to_entity(p) for p in projets_db]

    def recuperer_par_id(self, id: int) -> Optional[Projet]:
        """
        Récupère un projet par son identifiant.
        """
        projet_db = self.db.query(ProjetModel).filter(ProjetModel.id == id).first()
        if not projet_db:
            return None
        return self._to_entity(projet_db)

    def recuperer_par_slug(self, slug: str) -> Optional[Projet]:
        """
        Récupère un projet par son slug unique.
        """
        projet_db = self.db.query(ProjetModel).filter(ProjetModel.slug == slug).first()
        if not projet_db:
            return None
        return self._to_entity(projet_db)

    def ajouter(self, projet: Projet) -> Projet:
        """
        Ajoute un nouveau projet en base.
        """
        projet_db = ProjetModel(
            titre=projet.titre,
            slug=projet.slug,
            description_courte=projet.description_courte,
            description_longue=projet.description_longue,
            histoire=projet.histoire,
            image_url=projet.image_url,
            actif=projet.actif,
            ordre=projet.ordre,
        )
        self.db.add(projet_db)
        self.db.commit()
        self.db.refresh(projet_db)
        return self._to_entity(projet_db)

    def mettre_a_jour(self, projet: Projet) -> Projet:
        """
        Met à jour un projet existant.
        On suppose que l'entité possède un id correspondant à une ligne existante.
        """
        projet_db = self.db.query(ProjetModel).filter(ProjetModel.id == projet.id).first()
        if not projet_db:
            raise ValueError(f"Projet avec id {projet.id} introuvable.")
        projet_db.titre = projet.titre
        projet_db.slug = projet.slug
        projet_db.description_courte = projet.description_courte
        projet_db.description_longue = projet.description_longue
        projet_db.histoire = projet.histoire
        projet_db.image_url = projet.image_url
        projet_db.actif = projet.actif
        projet_db.ordre = projet.ordre
        self.db.commit()
        self.db.refresh(projet_db)
        return self._to_entity(projet_db)

    def supprimer(self, id: int) -> None:
        """
        Supprime un projet par son id.
        """
        projet_db = self.db.query(ProjetModel).filter(ProjetModel.id == id).first()
        if projet_db:
            self.db.delete(projet_db)
            self.db.commit()

    def basculer_actif(self, id: int) -> Optional[Projet]:
        """
        Inverse l'état actif/inactif d'un projet.
        """
        projet_db = self.db.query(ProjetModel).filter(ProjetModel.id == id).first()
        if not projet_db:
            return None
        projet_db.actif = not projet_db.actif
        self.db.commit()
        self.db.refresh(projet_db)
        return self._to_entity(projet_db)

    def _to_entity(self, model: ProjetModel) -> Projet:
        """
        Mappe un modèle SQLAlchemy vers l'entité domaine.
        """
        return Projet(
            id=model.id,
            titre=model.titre,
            slug=model.slug,
            description_courte=model.description_courte,
            description_longue=model.description_longue,
            histoire=model.histoire,
            image_url=model.image_url,
            actif=model.actif,
            ordre=model.ordre,
        )