"""
Interface Repository : AboutRepository
=======================================
Définit les opérations de persistance pour le contenu "À propos".
"""

from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.about import About


class AboutRepository(ABC):
    """Contrat pour la gestion du contenu À propos."""

    @abstractmethod
    def recuperer(self) -> Optional[About]:
        """
        Récupère le contenu unique de la page 'À propos'.
        """
        pass

    @abstractmethod
    def sauvegarder(self, about: About) -> About:
        """
        Crée ou met à jour le contenu.
        """
        pass