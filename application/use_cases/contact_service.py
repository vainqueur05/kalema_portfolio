"""
Use Case : ContactService
==========================
Orchestre la logique métier liée aux messages de contact (mini CRM).
Dépend de l'interface ContactRepository.
"""

from typing import List, Optional
from domain.entities.contact import Contact
from domain.value_objects.email import Email
from application.interfaces.repositories.contact_repo import ContactRepository


class ContactService:
    """
    Service applicatif pour la gestion des messages de contact.
    """

    def __init__(self, contact_repo: ContactRepository):
        self.contact_repo = contact_repo

    def lister_messages(self, statut: Optional[str] = None) -> List[Contact]:
        return self.contact_repo.recuperer_tous(statut=statut)

    def recuperer_message(self, id: int) -> Optional[Contact]:
        return self.contact_repo.recuperer_par_id(id)

    def envoyer_message(
        self,
        nom: str,
        email: str,
        message: str,
        telephone: Optional[str] = None,
    ) -> Contact:
        contact = Contact(
            nom=nom,
            email=Email(email),
            message=message,
            telephone=telephone,
            statut="Nouveau",
        )
        return self.contact_repo.ajouter(contact)

    def changer_statut(self, id: int, statut: str) -> Optional[Contact]:
        contact = self.contact_repo.recuperer_par_id(id)
        if not contact:
            return None
        contact_modifie = contact.mettre_a_jour(statut=statut)
        return self.contact_repo.mettre_a_jour(contact_modifie)

    def ajouter_note_admin(self, id: int, note_admin: str) -> Optional[Contact]:
        contact = self.contact_repo.recuperer_par_id(id)
        if not contact:
            return None
        contact_modifie = contact.mettre_a_jour(note_admin=note_admin)
        return self.contact_repo.mettre_a_jour(contact_modifie)

    def supprimer_message(self, id: int) -> bool:
        contact = self.contact_repo.recuperer_par_id(id)
        if not contact:
            return False
        self.contact_repo.supprimer(id)
        return True