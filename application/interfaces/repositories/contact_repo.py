"""
Interface Repository : ContactRepository
=========================================
Définit les opérations de persistance pour les messages de contact.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.contact import Contact


class ContactRepository(ABC):
    """Contrat pour la gestion des contacts (mini CRM)."""

    @abstractmethod
    def recuperer_tous(self, statut: Optional[str] = None) -> List[Contact]:
        """
        Liste les messages, avec un filtre optionnel par statut.
        Args:
            statut: 'Nouveau', 'Lu', 'Répondu' ou None pour tous.
        """
        pass

    @abstractmethod
    def recuperer_par_id(self, id: int) -> Optional[Contact]:
        pass

    @abstractmethod
    def ajouter(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def mettre_a_jour(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def supprimer(self, id: int) -> None:
        pass