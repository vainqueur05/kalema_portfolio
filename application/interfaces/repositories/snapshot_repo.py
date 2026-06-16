"""
Interface Repository : SnapshotRepository
==========================================
Définit les opérations de persistance pour les snapshots.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.snapshot import Snapshot


class SnapshotRepository(ABC):
    """Contrat pour la gestion des snapshots."""

    @abstractmethod
    def recuperer_tous(self) -> List[Snapshot]:
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[Snapshot]:
        pass

    @abstractmethod
    def sauvegarder(self, snapshot: Snapshot) -> Snapshot:
        """
        Ajoute un nouveau snapshot (création d'une sauvegarde).
        """
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        pass