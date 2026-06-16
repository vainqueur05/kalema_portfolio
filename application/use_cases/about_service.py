"""
Use Case : AboutService
========================
Orchestre la logique métier pour la page "À propos".
Dépend de l'interface AboutRepository.
"""

from typing import Optional
from domain.entities.about import About
from application.interfaces.repositories.about_repo import AboutRepository


class AboutService:
    """
    Service applicatif pour gérer le contenu de la page À propos.

    Attributes:
        about_repo (AboutRepository): Repository injecté.
    """

    def __init__(self, about_repo: AboutRepository):
        self.about_repo = about_repo

    def recuperer_contenu(self) -> Optional[About]:
        """
        Retourne le contenu unique de la page À propos.

        Returns:
            L'entité About si elle existe, sinon None.
        """
        return self.about_repo.recuperer()

    def mettre_a_jour_contenu(self, contenu: str) -> About:
        """
        Crée ou met à jour le contenu de la page.

        Args:
            contenu: Le nouveau contenu (Markdown ou HTML).

        Returns:
            L'entité About persistée.

        Raises:
            ValueError: Si le contenu est invalide.
        """
        existant = self.about_repo.recuperer()

        if existant:
            nouveau = existant.mettre_a_jour(contenu=contenu)
        else:
            nouveau = About(contenu=contenu)

        return self.about_repo.sauvegarder(nouveau)