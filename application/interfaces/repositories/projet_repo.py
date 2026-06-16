"""
Interface Repository : ProjetRepository
========================================
Définit les opérations de persistance pour les projets.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.projet import Projet


class ProjetRepository(ABC):
    """Contrat pour la gestion des projets."""

    @abstractmethod
    def recuperer_tous(self, actif_seulement: bool = False) -> List[Projet]:
        """
        Liste tous les projets, éventuellement filtrés par visibilité.

        Args:
            actif_seulement: Si True, ne retourne que les projets actifs.

        Returns:
            Liste des projets.
        """
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[Projet]:
        """
        Récupère un projet par son identifiant.
        """
        pass

    @abstractmethod
    def recuperer_par_slug(self, slug: str) -> Optional[Projet]:
        """
        Récupère un projet par son slug (pour les URLs publiques).
        """
        pass

    @abstractmethod
    def ajouter(self, projet: Projet) -> Projet:
        """
        Ajoute un nouveau projet.
        """
        pass

    @abstractmethod
    def mettre_a_jour(self, projet: Projet) -> Projet:
        """
        Met à jour un projet existant.
        """
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        """
        Supprime un projet par son identifiant.
        """
        pass

    @abstractmethod
    def basculer_actif(self, id: int) -> Optional[Projet]:
        """
        Inverse l'état actif/inactif d'un projet.
        Returns:
            Le projet mis à jour ou None si inexistant.
        """
        pass