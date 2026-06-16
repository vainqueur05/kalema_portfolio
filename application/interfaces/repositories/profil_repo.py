"""
Interface Repository : ProfilRepository
========================================
Définit les opérations de persistance pour l'entité Profil.
"""

from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.profil import Profil


class ProfilRepository(ABC):
    """Contrat pour la gestion du profil."""

    @abstractmethod
    def recuperer(self) -> Optional[Profil]:
        """
        Récupère le profil unique (il n'y en a qu'un).
        Returns:
            Profil ou None si aucun profil en base.
        """
        pass

    @abstractmethod
    def sauvegarder(self, profil: Profil) -> Profil:
        """
        Crée ou met à jour le profil.
        Args:
            profil: L'entité Profil à persister.
        Returns:
            Le profil persisté (avec un id si création).
        """
        pass