"""
Use Case : LienContactService
==============================
Orchestre la logique métier liée aux liens de contact.
Dépend de l'interface LienContactRepository.
"""

from typing import List, Optional
from domain.entities.lien_contact import LienContact
from application.interfaces.repositories.lien_contact_repo import LienContactRepository


class LienContactService:
    """
    Service applicatif pour la gestion des liens de contact.

    Attributes:
        lien_repo (LienContactRepository): Repository injecté.
    """

    def __init__(self, lien_repo: LienContactRepository):
        self.lien_repo = lien_repo

    def lister_liens(self, actif_seulement: bool = False) -> List[LienContact]:
        """
        Retourne la liste des liens de contact.

        Args:
            actif_seulement: Si True, ne retourne que les liens actifs.

        Returns:
            Liste des liens.
        """
        return self.lien_repo.recuperer_tous(actif_seulement=actif_seulement)

    def recuperer_lien(self, id: int) -> Optional[LienContact]:
        """Retourne un lien par son ID."""
        return self.lien_repo.recuperer_par_id(id)

    def creer_lien(
        self,
        nom: str,
        url: str,
        icone: str,
        actif: bool = True,
        ordre: int = 0,
    ) -> LienContact:
        """
        Crée un nouveau lien de contact.

        Args:
            nom: Nom affiché (ex: 'LinkedIn').
            url: URL du lien (http, https, mailto, tel, /).
            icone: Classe CSS Font Awesome.
            actif: Visibilité.
            ordre: Position d'affichage.

        Returns:
            Le lien créé (avec ID).

        Raises:
            ValueError: Si les données sont invalides.
        """
        lien = LienContact(
            nom=nom,
            url=url,
            icone=icone,
            actif=actif,
            ordre=ordre,
        )
        return self.lien_repo.ajouter(lien)

    def modifier_lien(
        self,
        id: int,
        nom: Optional[str] = None,
        url: Optional[str] = None,
        icone: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> Optional[LienContact]:
        """
        Modifie un lien existant. Seuls les champs fournis sont mis à jour.

        Args:
            id: Identifiant du lien.
            nom, url, icone, actif, ordre: Nouvelles valeurs (optionnelles).

        Returns:
            Le lien modifié, ou None si l'ID n'existe pas.
        """
        lien = self.lien_repo.recuperer_par_id(id)
        if not lien:
            return None

        lien_modifie = lien.mettre_a_jour(
            nom=nom,
            url=url,
            icone=icone,
            actif=actif,
            ordre=ordre,
        )
        return self.lien_repo.mettre_a_jour(lien_modifie)

    def supprimer_lien(self, id: int) -> bool:
        """
        Supprime un lien par ID.

        Returns:
            True si supprimé, False si non trouvé.
        """
        lien = self.lien_repo.recuperer_par_id(id)
        if not lien:
            return False
        self.lien_repo.supprimer(id)
        return True

    def basculer_actif_lien(self, id: int) -> Optional[LienContact]:
        """
        Inverse l'état actif/inactif d'un lien.

        Returns:
            Le lien après basculement, ou None si non trouvé.
        """
        return self.lien_repo.basculer_actif(id)