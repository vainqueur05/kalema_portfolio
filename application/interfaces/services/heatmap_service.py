"""
Interface Service : HeatmapService
===================================
Contrat pour l'enregistrement et la restitution des données de carte de chaleur.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class HeatmapService(ABC):
    """
    Service de carte de chaleur : enregistre les clics/scrolls et les restitue.
    """

    @abstractmethod
    def enregistrer_evenement(self, evenement: Dict[str, Any]) -> None:
        """
        Enregistre un événement (clic, scroll) avec ses coordonnées et métadonnées.
        """
        pass

    @abstractmethod
    def recuperer_donnees(self, page: str = None) -> List[Dict[str, Any]]:
        """
        Récupère les données de chaleur pour une page donnée (ou toutes).
        """
        pass