"""
Interface Service : MaintenanceService
=======================================
Contrat pour la gestion du mode maintenance.
"""

from abc import ABC, abstractmethod


class MaintenanceService(ABC):
    """
    Service pour vérifier et basculer le mode maintenance.
    """

    @abstractmethod
    def est_actif(self) -> bool:
        """Retourne True si le site est en maintenance."""
        pass

    @abstractmethod
    def activer(self) -> None:
        """Active le mode maintenance."""
        pass

    @abstractmethod
    def desactiver(self) -> None:
        """Désactive le mode maintenance."""
        pass