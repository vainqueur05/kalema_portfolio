"""
Interface Repository : TemoignageRepository
=============================================
Définit les opérations de persistance pour les témoignages.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.temoignage import Temoignage


class TemoignageRepository(ABC):
    """Contrat pour la gestion des témoignages."""

    @abstractmethod
    def recuperer_tous(self, actif_seulement: bool = False) -> List[Temoignage]:
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[Temoignage]:
        pass

    @abstractmethod
    def ajouter(self, temoignage: Temoignage) -> Temoignage:
        pass

    @abstractmethod
    def mettre_a_jour(self, temoignage: Temoignage) -> Temoignage:
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        pass

    @abstractmethod
    def basculer_actif(self, id: int) -> Optional[Temoignage]:
        pass