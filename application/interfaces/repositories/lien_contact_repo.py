"""
Interface Repository : LienContactRepository
=============================================
Définit les opérations de persistance pour les liens de contact.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.lien_contact import LienContact


class LienContactRepository(ABC):
    """Contrat pour la gestion des liens de contact."""

    @abstractmethod
    def recuperer_tous(self, actif_seulement: bool = False) -> List[LienContact]:
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[LienContact]:
        pass

    @abstractmethod
    def ajouter(self, lien: LienContact) -> LienContact:
        pass

    @abstractmethod
    def mettre_a_jour(self, lien: LienContact) -> LienContact:
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        pass

    @abstractmethod
    def basculer_actif(self, id: int) -> Optional[LienContact]:
        pass