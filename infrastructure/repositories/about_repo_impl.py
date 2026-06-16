"""
Implémentation du Repository About
=====================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface AboutRepository avec SQLAlchemy.
"""

from typing import Optional
from sqlalchemy.orm import Session
from domain.entities.about import About
from application.interfaces.repositories.about_repo import AboutRepository
from infrastructure.database.models import AboutModel


class AboutRepositoryImpl(AboutRepository):
    """
    Implémentation SQLAlchemy pour la gestion du contenu "À propos".
    Une seule ligne existe dans la table.

    Attributes:
        db (Session): Session SQLAlchemy injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer(self) -> Optional[About]:
        """Récupère le contenu unique de la page À propos."""
        about_db = self.db.query(AboutModel).first()
        if not about_db:
            return None
        return self._to_entity(about_db)

    def sauvegarder(self, about: About) -> About:
        """
        Crée ou met à jour le contenu À propos.
        S'il existe déjà, mise à jour ; sinon création.
        """
        about_db = self.db.query(AboutModel).first()
        if about_db:
            about_db.contenu = about.contenu
        else:
            about_db = AboutModel(contenu=about.contenu)
            self.db.add(about_db)
        self.db.commit()
        self.db.refresh(about_db)
        return self._to_entity(about_db)

    def _to_entity(self, model: AboutModel) -> About:
        """Mappe le modèle SQLAlchemy vers l'entité domaine."""
        return About(
            id=model.id,
            contenu=model.contenu,
        )