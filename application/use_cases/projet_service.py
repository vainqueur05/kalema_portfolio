"""
Use Case : ProjetService
=========================
Orchestre la logique métier liée aux projets du portfolio.
Dépend de l'interface ProjetRepository.
"""

from typing import List, Optional
from domain.entities.projet import Projet
from application.interfaces.repositories.projet_repo import ProjetRepository


class ProjetService:
    """
    Service applicatif pour la gestion des projets.

    Attributes:
        projet_repo (ProjetRepository): Repository injecté.
    """

    def __init__(self, projet_repo: ProjetRepository):
        self.projet_repo = projet_repo

    def lister_projets(self, actif_seulement: bool = False) -> List[Projet]:
        """
        Retourne la liste des projets, éventuellement filtrée.

        Args:
            actif_seulement: Si True, ne renvoie que les projets visibles.

        Returns:
            Liste des projets.
        """
        return self.projet_repo.recuperer_tous(actif_seulement=actif_seulement)

    def recuperer_projet(self, id: int) -> Optional[Projet]:
        """Retourne un projet par son ID."""
        return self.projet_repo.recuperer_par_id(id)

    def recuperer_projet_par_slug(self, slug: str) -> Optional[Projet]:
        """Retourne un projet par son slug (URL publique)."""
        return self.projet_repo.recuperer_par_slug(slug)

    def creer_projet(
        self,
        titre: str,
        description_courte: str,
        description_longue: str,
        slug: Optional[str] = None,
        histoire: str = "",
        image_url: Optional[str] = None,
        actif: bool = True,
        ordre: int = 0,
    ) -> Projet:
        """
        Crée un nouveau projet et le persiste.

        Args:
            titre: Titre.
            description_courte: Accroche.
            description_longue: Détail.
            slug: Identifiant d'URL (généré automatiquement si absent).
            histoire: Histoire narrative.
            image_url: Image principale.
            actif: Visibilité.
            ordre: Position.

        Returns:
            Le projet créé (avec ID).

        Raises:
            ValueError: Si les données sont invalides.
        """
        projet = Projet(
            titre=titre,
            slug=slug,
            description_courte=description_courte,
            description_longue=description_longue,
            histoire=histoire,
            image_url=image_url,
            actif=actif,
            ordre=ordre,
        )
        return self.projet_repo.ajouter(projet)

    def modifier_projet(
        self,
        id: int,
        titre: Optional[str] = None,
        description_courte: Optional[str] = None,
        description_longue: Optional[str] = None,
        slug: Optional[str] = None,
        histoire: Optional[str] = None,
        image_url: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> Optional[Projet]:
        """
        Modifie un projet existant (seuls les champs fournis sont modifiés).

        Args:
            id: Identifiant du projet.
            (Les autres paramètres sont optionnels.)

        Returns:
            Le projet mis à jour, ou None si non trouvé.

        Raises:
            ValueError: Si les nouvelles données sont invalides.
        """
        projet = self.projet_repo.recuperer_par_id(id)
        if not projet:
            return None

        projet_modifie = projet.mettre_a_jour(
            titre=titre,
            description_courte=description_courte,
            description_longue=description_longue,
            slug=slug,
            histoire=histoire,
            image_url=image_url,
            actif=actif,
            ordre=ordre,
        )
        return self.projet_repo.mettre_a_jour(projet_modifie)

    def supprimer_projet(self, id: int) -> bool:
        """
        Supprime un projet par ID.

        Returns:
            True si le projet a été supprimé, False si non trouvé.
        """
        projet = self.projet_repo.recuperer_par_id(id)
        if not projet:
            return False
        self.projet_repo.supprimer(id)
        return True

    def basculer_actif_projet(self, id: int) -> Optional[Projet]:
        """
        Inverse l'état actif/inactif d'un projet.

        Returns:
            Le projet après basculement, ou None si non trouvé.
        """
        return self.projet_repo.basculer_actif(id)