"""
Use Case : ProfilService
=========================
Orchestre la logique métier liée au profil unique du développeur.
Dépend de l'interface ProfilRepository (injection de dépendance).
Ne connaît rien de la base de données ou du framework web.
"""

from typing import Optional
from domain.entities.profil import Profil
from application.interfaces.repositories.profil_repo import ProfilRepository


class ProfilService:
    """
    Service applicatif pour gérer le profil.

    Attributes:
        profil_repo (ProfilRepository): Le repository injecté.
    """

    def __init__(self, profil_repo: ProfilRepository):
        """
        Initialise le service avec le repository nécessaire.

        Args:
            profil_repo: Une implémentation concrète du repository profil.
        """
        self.profil_repo = profil_repo

    def recuperer_profil(self) -> Optional[Profil]:
        """
        Retourne le profil unique s'il existe.

        Returns:
            Profil ou None si aucun profil n'a encore été créé.
        """
        return self.profil_repo.recuperer()

    def mettre_a_jour_profil(
        self,
        nom_complet: str,
        titre: str,
        bio: str,
        photo_url: Optional[str] = None
    ) -> Profil:
        """
        Crée ou met à jour le profil avec les nouvelles valeurs.
        Si aucun profil n'existe, il sera créé.

        Args:
            nom_complet: Nom complet.
            titre: Titre professionnel.
            bio: Biographie.
            photo_url: URL ou chemin de la photo (optionnel).

        Returns:
            Le profil mis à jour ou créé, déjà persisté.

        Raises:
            ValueError: Si les données sont invalides (validées par l'entité).
        """
        profil_existant = self.profil_repo.recuperer()

        if profil_existant:
            # Mise à jour via la méthode de l'entité, puis persistance
            nouveau_profil = profil_existant.mettre_a_jour(
                nom_complet=nom_complet,
                titre=titre,
                bio=bio,
                photo_url=photo_url
            )
        else:
            # Création d'un nouveau profil
            nouveau_profil = Profil(
                nom_complet=nom_complet,
                titre=titre,
                bio=bio,
                photo_url=photo_url
            )

        # Sauvegarde (création ou mise à jour réelle)
        return self.profil_repo.sauvegarder(nouveau_profil)