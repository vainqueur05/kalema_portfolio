"""
Implémentation du Repository Contact
=====================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface ContactRepository avec SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.contact import Contact
from domain.value_objects.email import Email
from application.interfaces.repositories.contact_repo import ContactRepository
from infrastructure.database.models import ContactModel


class ContactRepositoryImpl(ContactRepository):
    """
    Implémentation SQLAlchemy pour la gestion des messages de contact.

    Attributes:
        db (Session): Session SQLAlchemy injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self, statut: Optional[str] = None) -> List[Contact]:
        """Retourne la liste des messages, filtrée par statut si précisé."""
        query = self.db.query(ContactModel)
        if statut:
            query = query.filter(ContactModel.statut == statut)
        contacts_db = query.order_by(ContactModel.created_at.desc()).all()
        return [self._to_entity(c) for c in contacts_db]

    def recuperer_par_id(self, id: int) -> Optional[Contact]:
        """Récupère un message par son ID."""
        contact_db = self.db.query(ContactModel).filter(ContactModel.id == id).first()
        if not contact_db:
            return None
        return self._to_entity(contact_db)

    def ajouter(self, contact: Contact) -> Contact:
        """Enregistre un nouveau message."""
        contact_db = ContactModel(
            nom=contact.nom,
            email=str(contact.email),
            telephone=contact.telephone,
            message=contact.message,
            statut=contact.statut,
            note_admin=contact.note_admin,
        )
        self.db.add(contact_db)
        self.db.commit()
        self.db.refresh(contact_db)
        return self._to_entity(contact_db)

    def mettre_a_jour(self, contact: Contact) -> Contact:
        """Met à jour un message existant (statut, note)."""
        contact_db = self.db.query(ContactModel).filter(ContactModel.id == contact.id).first()
        if not contact_db:
            raise ValueError(f"Contact avec id {contact.id} introuvable.")
        contact_db.nom = contact.nom
        contact_db.email = str(contact.email)
        contact_db.telephone = contact.telephone
        contact_db.message = contact.message
        contact_db.statut = contact.statut
        contact_db.note_admin = contact.note_admin
        self.db.commit()
        self.db.refresh(contact_db)
        return self._to_entity(contact_db)

    def supprimer(self, id: int) -> None:
        """Supprime un message par son ID."""
        contact_db = self.db.query(ContactModel).filter(ContactModel.id == id).first()
        if contact_db:
            self.db.delete(contact_db)
            self.db.commit()

    def _to_entity(self, model: ContactModel) -> Contact:
        """Mappe le modèle SQLAlchemy vers l'entité domaine."""
        return Contact(
            id=model.id,
            nom=model.nom,
            email=Email(model.email),
            telephone=model.telephone,
            message=model.message,
            statut=model.statut,
            note_admin=model.note_admin,
        )