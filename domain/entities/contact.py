"""
Entité : Contact
=================
Représente un message reçu via le formulaire de contact public.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- nom : obligatoire, 2 à 100 caractères.
- email : obligatoire, adresse email valide (Value Object Email).
- telephone : optionnel, chaîne avec format international accepté.
- message : obligatoire, 20 à 2000 caractères.
- statut : parmi 'Nouveau', 'Lu', 'Répondu'. Par défaut 'Nouveau'.
- note_admin : optionnelle, texte libre (max 2000 caractères) pour suivi interne.
- created_at : NON inclus, géré par la couche infrastructure.
"""

from dataclasses import dataclass, field
from typing import Optional
import re
from domain.value_objects.email import Email


# Statuts autorisés
STATUTS_VALIDES = {"Nouveau", "Lu", "Répondu"}


@dataclass
class Contact:
    """
    Entité représentant un message de contact.

    Attributes:
        nom (str): Nom de l'expéditeur.
        email (Email): Adresse email valide.
        message (str): Contenu du message.
        telephone (Optional[str]): Numéro de téléphone (format international).
        statut (str): État de traitement du message.
        note_admin (Optional[str]): Note privée de l'administrateur.
        id (Optional[int]): Identifiant technique.
    """

    nom: str
    email: Email
    message: str
    telephone: Optional[str] = None
    statut: str = "Nouveau"
    note_admin: Optional[str] = None
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation métier."""
        # --- Nom ---
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom est obligatoire.")
        nom_clean = self.nom.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères.")
        if len(nom_clean) > 100:
            raise ValueError("Le nom ne doit pas dépasser 100 caractères.")
        object.__setattr__(self, "nom", nom_clean)

        # --- Email ---
        # L'email est déjà un Value Object, il se valide lui-même.
        # S'assurer que c'est bien une instance d'Email (ou le convertir)
        if isinstance(self.email, str):
            # Tentative de conversion automatique
            try:
                object.__setattr__(self, "email", Email(self.email))
            except ValueError as e:
                raise ValueError(f"Email invalide : {e}")
        elif not isinstance(self.email, Email):
            raise ValueError("L'email doit être une instance de Email ou une chaîne valide.")

        # --- Message ---
        if not self.message or not self.message.strip():
            raise ValueError("Le message est obligatoire.")
        msg_clean = self.message.strip()
        if len(msg_clean) < 20:
            raise ValueError("Le message doit contenir au moins 20 caractères.")
        if len(msg_clean) > 2000:
            raise ValueError("Le message ne doit pas dépasser 2000 caractères.")
        object.__setattr__(self, "message", msg_clean)

        # --- Téléphone (optionnel) ---
        if self.telephone is not None:
            tel_clean = self.telephone.strip()
            if not tel_clean:
                object.__setattr__(self, "telephone", None)
            else:
                # Validation basique : autoriser +, chiffres, espaces, tirets, points, parenthèses
                if not re.match(r"^[+\d\s\-().]{7,30}$", tel_clean):
                    raise ValueError(
                        "Le numéro de téléphone contient des caractères non autorisés "
                        "ou une longueur incorrecte (7 à 30 caractères acceptés)."
                    )
                object.__setattr__(self, "telephone", tel_clean)

        # --- Statut ---
        if self.statut not in STATUTS_VALIDES:
            raise ValueError(
                f"Statut invalide. Valeurs acceptées : {', '.join(sorted(STATUTS_VALIDES))}."
            )
        # Déjà nettoyé, pas de modification

        # --- Note admin ---
        if self.note_admin is not None:
            note_clean = self.note_admin.strip()
            if not note_clean:
                object.__setattr__(self, "note_admin", None)
            elif len(note_clean) > 2000:
                raise ValueError("La note admin ne doit pas dépasser 2000 caractères.")
            else:
                object.__setattr__(self, "note_admin", note_clean)

    def mettre_a_jour(
        self,
        nom: Optional[str] = None,
        email: Optional[Email] = None,
        message: Optional[str] = None,
        telephone: Optional[str] = None,
        statut: Optional[str] = None,
        note_admin: Optional[str] = None,
    ) -> "Contact":
        """
        Crée une nouvelle instance avec les champs modifiés.

        Args:
            nom: Nouveau nom.
            email: Nouvel email (Value Object Email).
            message: Nouveau message.
            telephone: Nouveau téléphone.
            statut: Nouveau statut.
            note_admin: Nouvelle note admin.

        Returns:
            Contact: Nouvelle instance mise à jour.
        """
        return Contact(
            nom=nom if nom is not None else self.nom,
            email=email if email is not None else self.email,
            message=message if message is not None else self.message,
            telephone=telephone if telephone is not None else self.telephone,
            statut=statut if statut is not None else self.statut,
            note_admin=note_admin if note_admin is not None else self.note_admin,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire.

        Returns:
            dict: Données du contact.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "email": str(self.email),  # Conversion explicite
            "telephone": self.telephone,
            "message": self.message,
            "statut": self.statut,
            "note_admin": self.note_admin,
        }

    def __repr__(self) -> str:
        return (
            f"Contact(id={self.id}, nom='{self.nom}', "
            f"email='{self.email}', statut='{self.statut}')"
        )