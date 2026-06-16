"""
Entité : About
==============
Représente le contenu éditable de la page "À propos".
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- contenu : obligatoire, texte libre (Markdown ou WYSIWYG).
  Longueur minimale : 20 caractères (pour garantir un contenu significatif).
  Longueur maximale : 20 000 caractères (limite raisonnable pour une page).
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class About:
    """
    Entité représentant la page "À propos".

    Attributes:
        contenu (str): Texte de la page, en Markdown ou HTML.
        id (Optional[int]): Identifiant technique (None avant persistance).
    """

    contenu: str
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation du contenu."""
        if not self.contenu or not self.contenu.strip():
            raise ValueError("Le contenu de la page 'À propos' est obligatoire.")
        contenu_clean = self.contenu.strip()
        if len(contenu_clean) < 20:
            raise ValueError(
                "Le contenu de la page 'À propos' doit contenir au moins 20 caractères."
            )
        if len(contenu_clean) > 20000:
            raise ValueError(
                "Le contenu de la page 'À propos' ne doit pas dépasser 20 000 caractères."
            )
        object.__setattr__(self, "contenu", contenu_clean)

    def mettre_a_jour(self, contenu: Optional[str] = None) -> "About":
        """
        Retourne une nouvelle instance avec le contenu mis à jour.

        Args:
            contenu (Optional[str]): Nouveau contenu. Si None, conserve l'existant.

        Returns:
            About: Nouvelle instance.
        """
        return About(
            contenu=contenu if contenu is not None else self.contenu,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire.

        Returns:
            dict: Données de la page 'À propos'.
        """
        return {
            "id": self.id,
            "contenu": self.contenu,
        }

    def __repr__(self) -> str:
        apercu = (self.contenu[:50] + "...") if len(self.contenu) > 50 else self.contenu
        return f"About(id={self.id}, contenu='{apercu}')"