"""
Use Case : TemoignageService
=============================
Orchestre la logique métier liée aux témoignages.
Dépend de l'interface TemoignageRepository.
"""

from typing import List, Optional
from domain.entities.temoignage import Temoignage
from application.interfaces.repositories.temoignage_repo import TemoignageRepository


class TemoignageService:
    """
    Service applicatif pour la gestion des témoignages.

    Attributes:
        temoignage_repo (TemoignageRepository): Repository injecté.
    """

    def __init__(self, temoignage_repo: TemoignageRepository):
        self.temoignage_repo = temoignage_repo

    def lister_temoignages(self, actif_seulement: bool = False) -> List[Temoignage]:
        """
        Retourne la liste des témoignages, éventuellement filtrés.

        Args:
            actif_seulement: Si True, ne retourne que les témoignages actifs.

        Returns:
            Liste des témoignages.
        """
        return self.temoignage_repo.recuperer_tous(actif_seulement=actif_seulement)

    def recuperer_temoignage(self, id: int) -> Optional[Temoignage]:
        """Retourne un témoignage par son ID."""
        return self.temoignage_repo.recuperer_par_id(id)

    def creer_temoignage(
        self,
        nom: str,
        texte: str,
        photo_url: Optional[str] = None,
        entreprise: Optional[str] = None,
        actif: bool = True,
        ordre: int = 0,
    ) -> Temoignage:
        """
        Crée un nouveau témoignage.

        Args:
            nom: Nom de la personne.
            texte: Contenu du témoignage.
            photo_url: Photo ou avatar (optionnel).
            entreprise: Entreprise/fonction (optionnel).
            actif: Visibilité.
            ordre: Position d'affichage.

        Returns:
            Le témoignage créé (avec ID).

        Raises:
            ValueError: Si les données sont invalides.
        """
        temoignage = Temoignage(
            nom=nom,
            texte=texte,
            photo_url=photo_url,
            entreprise=entreprise,
            actif=actif,
            ordre=ordre,
        )
        return self.temoignage_repo.ajouter(temoignage)

    def modifier_temoignage(
        self,
        id: int,
        nom: Optional[str] = None,
        texte: Optional[str] = None,
        photo_url: Optional[str] = None,
        entreprise: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> Optional[Temoignage]:
        """
        Modifie un témoignage existant.

        Args:
            id: Identifiant du témoignage.
            nom, texte, photo_url, entreprise, actif, ordre: Nouvelles valeurs.

        Returns:
            Le témoignage modifié, ou None si l'ID n'existe pas.
        """
        temoignage = self.temoignage_repo.recuperer_par_id(id)
        if not temoignage:
            return None

        temoignage_modifie = temoignage.mettre_a_jour(
            nom=nom,
            texte=texte,
            photo_url=photo_url,
            entreprise=entreprise,
            actif=actif,
            ordre=ordre,
        )
        return self.temoignage_repo.mettre_a_jour(temoignage_modifie)

    def supprimer_temoignage(self, id: int) -> bool:
        """
        Supprime un témoignage par ID.

        Returns:
            True si supprimé, False si non trouvé.
        """
        temoignage = self.temoignage_repo.recuperer_par_id(id)
        if not temoignage:
            return False
        self.temoignage_repo.supprimer(id)
        return True

    def basculer_actif_temoignage(self, id: int) -> Optional[Temoignage]:
        """
        Inverse l'état actif/inactif d'un témoignage.

        Returns:
            Le témoignage après basculement, ou None si non trouvé.
        """
        return self.temoignage_repo.basculer_actif(id)