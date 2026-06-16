"""
Implémentation du service de géolocalisation par IP.
Utilise ipapi.co (gratuit jusqu'à 1000 requêtes/jour).
Respecte l'interface GeoService.
"""

from typing import Optional, Tuple
import requests
from application.interfaces.services.geo_service import GeoService


class GeoServiceImpl(GeoService):
    """
    Service de géolocalisation utilisant l'API ipapi.co.
    """

    BASE_URL = "https://ipapi.co/{ip}/json/"

    def localiser(self, ip: str) -> Optional[Tuple[str, str]]:
        """
        Interroge ipapi.co pour obtenir le pays et la ville d'une IP.

        Args:
            ip: Adresse IP à géolocaliser.

        Returns:
            Tuple (pays, ville) ou None en cas d'échec.
        """
        # Ne pas géolocaliser les IP locales
        if ip in ("127.0.0.1", "::1", "localhost"):
            return "Localhost", "Localhost"

        try:
            response = requests.get(self.BASE_URL.format(ip=ip), timeout=2)
            if response.status_code == 200:
                data = response.json()
                pays = data.get("country_name")
                ville = data.get("city")
                if pays:
                    return pays, ville or "Inconnue"
        except (requests.RequestException, ValueError):
            pass  # Échec silencieux, la visite est enregistrée sans géoloc
        return None