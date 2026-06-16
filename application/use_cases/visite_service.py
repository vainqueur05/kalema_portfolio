"""
Use Case : VisiteService
=========================
Orchestre la logique métier pour le suivi des visites.
Dépend de l'interface VisiteRepository et de GeoService.
"""

from typing import List, Dict, Any, Optional
from domain.entities.visite import Visite
from application.interfaces.repositories.visite_repo import VisiteRepository
from application.interfaces.services.geo_service import GeoService


class VisiteService:
    """
    Service applicatif pour l'enregistrement et la consultation des visites.

    Attributes:
        visite_repo (VisiteRepository): Repository des visites.
        geo_service (GeoService): Service de géolocalisation (optionnel).
    """

    def __init__(self, visite_repo: VisiteRepository, geo_service: Optional[GeoService] = None):
        self.visite_repo = visite_repo
        self.geo_service = geo_service

    def enregistrer_visite(
        self,
        page: str,
        ip: str,
        user_agent: Optional[str] = None,
        referrer: Optional[str] = None,
    ) -> Visite:
        """
        Enregistre une nouvelle visite et tente de géolocaliser l'IP.

        Args:
            page: Page visitée (ex: '/').
            ip: Adresse IP du visiteur.
            user_agent: User-Agent HTTP.
            referrer: Référent HTTP.

        Returns:
            L'entité Visite créée et persistée.
        """
        pays = None
        ville = None
        if self.geo_service:
            try:
                result = self.geo_service.localiser(ip)
                if result:
                    pays, ville = result
            except Exception:
                pass  # La géolocalisation ne doit pas bloquer l'enregistrement

        visite = Visite(
            page=page,
            ip=ip,
            user_agent=user_agent,
            referrer=referrer,
            pays=pays,
            ville=ville,
        )
        return self.visite_repo.enregistrer(visite)

    def lister_dernieres_visites(self, limite: int = 100) -> List[Visite]:
        """Retourne les dernières visites."""
        return self.visite_repo.recuperer_toutes(limite=limite)

    def obtenir_statistiques(self) -> Dict[str, Any]:
        """Retourne les statistiques agrégées des visites."""
        return self.visite_repo.statistiques()