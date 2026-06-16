"""
Interface Repository : VisiteRepository
=========================================
Définit les opérations de persistance pour les visites.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.visite import Visite


class VisiteRepository(ABC):
    """Contrat pour l'enregistrement et la consultation des visites."""

    @abstractmethod
    def enregistrer(self, visite: Visite) -> Visite:
        pass

    @abstractmethod
    def recuperer_toutes(self, limite: int = 100) -> List[Visite]:
        """
        Récupère les dernières visites (avec limite).
        """
        pass

    @abstractmethod
    def statistiques(self) -> dict:
        """
        Retourne des statistiques agrégées (total visites, par pays, etc.).
        La structure exacte est libre.
        """
        pass