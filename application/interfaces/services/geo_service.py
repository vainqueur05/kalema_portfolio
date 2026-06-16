"""
Interface Service : GeoService
===============================
Contrat pour le service de géolocalisation par IP.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple


class GeoService(ABC):
    """
    Service de géolocalisation : convertit une adresse IP en pays/ville.
    """

    @abstractmethod
    def localiser(self, ip: str) -> Optional[Tuple[str, str]]:
        """
        Retourne (pays, ville) pour une IP donnée, ou None si non trouvé.
        """
        pass