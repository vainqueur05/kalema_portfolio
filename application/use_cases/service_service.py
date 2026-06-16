"""
Use Case : ServiceService
===========================
Orchestre la logique métier liée aux services proposés.
Dépend de l'interface ServiceRepository.
"""

from typing import List, Optional
from domain.entities.service import Service
from application.interfaces.repositories.service_repo import ServiceRepository


class ServiceService:
    """
    Service applicatif pour la gestion des services.

    Attributes:
        service_repo (ServiceRepository): Repository injecté.
    """

    def __init__(self, service_repo: ServiceRepository):
        self.service_repo = service_repo

    def lister_services(self, actif_seulement: bool = False) -> List[Service]:
        """
        Retourne la liste des services, éventuellement filtrés par visibilité.

        Args:
            actif_seulement: Si True, ne retourne que les services actifs.

        Returns:
            Liste des services.
        """
        return self.service_repo.recuperer_tous(actif_seulement=actif_seulement)

    def recuperer_service(self, id: int) -> Optional[Service]:
        """Retourne un service par son ID."""
        return self.service_repo.recuperer_par_id(id)

    def creer_service(
        self,
        nom: str,
        description: str,
        prix: Optional[float] = None,
        icone: Optional[str] = None,
        actif: bool = True,
        ordre: int = 0,
    ) -> Service:
        """
        Crée un nouveau service.

        Args:
            nom: Nom du service.
            description: Description détaillée.
            prix: Prix (optionnel, masqué sur l'accueil).
            icone: Classe CSS d'icône (ex: 'fa-solid fa-code').
            actif: Visibilité.
            ordre: Position d'affichage.

        Returns:
            Le service créé (avec ID).

        Raises:
            ValueError: Si les données sont invalides.
        """
        service = Service(
            nom=nom,
            description=description,
            prix=prix,
            icone=icone,
            actif=actif,
            ordre=ordre,
        )
        return self.service_repo.ajouter(service)

    def modifier_service(
        self,
        id: int,
        nom: Optional[str] = None,
        description: Optional[str] = None,
        prix: Optional[float] = None,
        icone: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> Optional[Service]:
        """
        Modifie un service existant. Seuls les champs fournis sont mis à jour.

        Args:
            id: Identifiant du service.
            nom, description, prix, icone, actif, ordre: Nouvelles valeurs.

        Returns:
            Le service modifié, ou None si l'ID n'existe pas.

        Raises:
            ValueError: Si les nouvelles valeurs sont invalides.
        """
        service = self.service_repo.recuperer_par_id(id)
        if not service:
            return None

        service_modifie = service.mettre_a_jour(
            nom=nom,
            description=description,
            prix=prix,
            icone=icone,
            actif=actif,
            ordre=ordre,
        )
        return self.service_repo.mettre_a_jour(service_modifie)

    def supprimer_service(self, id: int) -> bool:
        """
        Supprime un service par ID.

        Returns:
            True si supprimé, False si non trouvé.
        """
        service = self.service_repo.recuperer_par_id(id)
        if not service:
            return False
        self.service_repo.supprimer(id)
        return True

    def basculer_actif_service(self, id: int) -> Optional[Service]:
        """
        Inverse l'état actif/inactif d'un service.

        Returns:
            Le service après basculement, ou None si non trouvé.
        """
        return self.service_repo.basculer_actif(id)