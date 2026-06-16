"""
Interface Repository : ServiceRepository
=========================================
Définit les opérations de persistance pour les services.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.service import Service


class ServiceRepository(ABC):
    """Contrat pour la gestion des services."""

    @abstractmethod
    def recuperer_tous(self, actif_seulement: bool = False) -> List[Service]:
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[Service]:
        pass

    @abstractmethod
    def ajouter(self, service: Service) -> Service:
        pass

    @abstractmethod
    def mettre_a_jour(self, service: Service) -> Service:
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        pass

    @abstractmethod
    def basculer_actif(self, id: int) -> Optional[Service]:
        pass