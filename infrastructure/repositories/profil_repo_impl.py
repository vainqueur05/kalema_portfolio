"""
Implémentation du Repository Profil
=====================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface ProfilRepository avec SQLAlchemy.
"""

from typing import Optional
from sqlalchemy.orm import Session
from domain.entities.profil import Profil
from application.interfaces.repositories.profil_repo import ProfilRepository
from infrastructure.database.models import ProfilModel


class ProfilRepositoryImpl(ProfilRepository):
    """
    Implémentation SQLAlchemy du repository Profil.

    Attributes:
        db (Session): La session de base de données injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer(self) -> Optional[Profil]:
        """
        Récupère le profil unique depuis la base.

        Returns:
            Profil ou None si la table est vide.
        """
        profil_db = self.db.query(ProfilModel).first()
        if not profil_db:
            return None
        return self._to_entity(profil_db)

    def sauvegarder(self, profil: Profil) -> Profil:
        """
        Crée ou met à jour le profil selon qu'il existe déjà ou non.
        Si un profil existe déjà, on le modifie ; sinon, on en crée un.

        Args:
            profil: L'entité Profil à persister.

        Returns:
            Profil persisté avec un id si nouvelle création.
        """
        profil_db = self.db.query(ProfilModel).first()
        if profil_db:
            # Mise à jour
            profil_db.photo_url = profil.photo_url
            profil_db.nom_complet = profil.nom_complet
            profil_db.titre = profil.titre
            profil_db.bio = profil.bio
        else:
            # Création
            profil_db = ProfilModel(
                photo_url=profil.photo_url,
                nom_complet=profil.nom_complet,
                titre=profil.titre,
                bio=profil.bio,
            )
            self.db.add(profil_db)
        self.db.commit()
        self.db.refresh(profil_db)
        return self._to_entity(profil_db)

    def _to_entity(self, model: ProfilModel) -> Profil:
        """
        Convertit un modèle SQLAlchemy en entité métier.

        Args:
            model: L'instance ProfilModel.

        Returns:
            Profil (entité domaine).
        """
        return Profil(
            id=model.id,
            nom_complet=model.nom_complet,
            titre=model.titre,
            bio=model.bio,
            photo_url=model.photo_url,
        )