"""
Entité : LienContact
=====================
Représente un lien de contact ou réseau social du développeur.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- nom : obligatoire, 2 à 100 caractères (ex: 'LinkedIn', 'WhatsApp').
- url : obligatoire, doit être une URL valide (http/https) ou un lien personnalisé (ex: 'mailto:', 'tel:').
- icone : obligatoire, chaîne représentant une icône Font Awesome (ex: 'fa-brands fa-linkedin').
- actif : booléen (True = visible).
- ordre : entier >= 0, détermine l'ordre d'affichage.
"""

from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class LienContact:
    """
    Entité représentant un lien de contact.

    Attributes:
        nom (str): Nom affiché du lien.
        url (str): URL ou chemin du lien.
        icone (str): Classe CSS de l'icône associée.
        actif (bool): Visibilité (True par défaut).
        ordre (int): Ordre d'affichage.
        id (Optional[int]): Identifiant technique.

    Raises:
        ValueError: Si les contraintes ne sont pas respectées.
    """

    nom: str
    url: str
    icone: str
    actif: bool = True
    ordre: int = 0
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation après création."""
        # --- Nom ---
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du lien de contact est obligatoire.")
        nom_clean = self.nom.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom du lien doit contenir au moins 2 caractères.")
        if len(nom_clean) > 100:
            raise ValueError("Le nom du lien ne doit pas dépasser 100 caractères.")
        object.__setattr__(self, "nom", nom_clean)

        # --- URL ---
        if not self.url or not self.url.strip():
            raise ValueError("L'URL du lien est obligatoire.")
        url_clean = self.url.strip()
        # Accepter http, https, mailto, tel, ou chemin relatif interne commençant par /
        if not (
            url_clean.startswith("http://")
            or url_clean.startswith("https://")
            or url_clean.startswith("mailto:")
            or url_clean.startswith("tel:")
            or url_clean.startswith("/")
        ):
            raise ValueError(
                "L'URL doit commencer par 'http://', 'https://', 'mailto:', 'tel:' ou '/'."
            )
        if len(url_clean) > 2000:
            raise ValueError("L'URL ne doit pas dépasser 2000 caractères.")
        object.__setattr__(self, "url", url_clean)

        # --- Icône ---
        if not self.icone or not self.icone.strip():
            raise ValueError("La classe de l'icône est obligatoire.")
        icone_clean = self.icone.strip()
        # Validation simple : lettres, tirets, espaces (classes CSS)
        if not re.match(r"^[a-zA-Z0-9\-_ ]+$", icone_clean):
            raise ValueError(
                "La classe d'icône contient des caractères non autorisés. "
                "Utilisez uniquement des lettres, chiffres, tirets et underscores."
            )
        object.__setattr__(self, "icone", icone_clean)

        # --- Ordre ---
        if not isinstance(self.ordre, int) or self.ordre < 0:
            raise ValueError("L'ordre doit être un entier positif ou zéro.")
        object.__setattr__(self, "ordre", self.ordre)

        # Actif est booléen, pas de validation supplémentaire

    def mettre_a_jour(
        self,
        nom: Optional[str] = None,
        url: Optional[str] = None,
        icone: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> "LienContact":
        """
        Crée une nouvelle instance avec les modifications souhaitées.

        Args:
            nom: Nouveau nom.
            url: Nouvelle URL.
            icone: Nouvelle icône.
            actif: Visibilité.
            ordre: Ordre d'affichage.

        Returns:
            LienContact: Nouvelle instance mise à jour.
        """
        return LienContact(
            nom=nom if nom is not None else self.nom,
            url=url if url is not None else self.url,
            icone=icone if icone is not None else self.icone,
            actif=actif if actif is not None else self.actif,
            ordre=ordre if ordre is not None else self.ordre,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire.

        Returns:
            dict: Représentation du lien de contact.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "url": self.url,
            "icone": self.icone,
            "actif": self.actif,
            "ordre": self.ordre,
        }

    def __repr__(self) -> str:
        return (
            f"LienContact(id={self.id}, nom='{self.nom}', url='{self.url}', actif={self.actif})"
        )