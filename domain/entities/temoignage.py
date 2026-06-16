"""
Entité : Temoignage
=====================
Représente un témoignage d'un client ou partenaire.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- nom : obligatoire, 2 à 100 caractères (nom de la personne).
- texte : obligatoire, 20 à 1000 caractères (le témoignage lui-même).
- photo_url : optionnelle, chemin ou URL valide si fournie.
- entreprise : optionnelle, 2 à 200 caractères si renseignée.
- actif : booléen (True = affiché dans le mur public).
- ordre : entier >= 0, contrôle l'ordre d'affichage.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Temoignage:
    """
    Entité représentant un témoignage.

    Attributes:
        nom (str): Nom de la personne qui témoigne.
        texte (str): Contenu du témoignage.
        photo_url (Optional[str]): Photo de la personne (ou avatar).
        entreprise (Optional[str]): Entreprise ou fonction de la personne.
        actif (bool): Visibilité publique.
        ordre (int): Position d'affichage.
        id (Optional[int]): Identifiant technique.
    """

    nom: str
    texte: str
    photo_url: Optional[str] = None
    entreprise: Optional[str] = None
    actif: bool = True
    ordre: int = 0
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation métier."""
        # --- Nom ---
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du témoin est obligatoire.")
        nom_clean = self.nom.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères.")
        if len(nom_clean) > 100:
            raise ValueError("Le nom ne doit pas dépasser 100 caractères.")
        object.__setattr__(self, "nom", nom_clean)

        # --- Texte ---
        if not self.texte or not self.texte.strip():
            raise ValueError("Le texte du témoignage est obligatoire.")
        texte_clean = self.texte.strip()
        if len(texte_clean) < 20:
            raise ValueError(
                "Le témoignage doit contenir au moins 20 caractères pour être significatif."
            )
        if len(texte_clean) > 1000:
            raise ValueError("Le témoignage ne doit pas dépasser 1000 caractères.")
        object.__setattr__(self, "texte", texte_clean)

        # --- Photo URL ---
        if self.photo_url is not None:
            photo_clean = self.photo_url.strip()
            if not photo_clean:
                object.__setattr__(self, "photo_url", None)
            elif not (
                photo_clean.startswith("/")
                or photo_clean.startswith("http://")
                or photo_clean.startswith("https://")
            ):
                raise ValueError(
                    "La photo_url doit être un chemin relatif (commençant par '/') "
                    "ou une URL complète (http/https)."
                )
            else:
                object.__setattr__(self, "photo_url", photo_clean)

        # --- Entreprise ---
        if self.entreprise is not None:
            entreprise_clean = self.entreprise.strip()
            if not entreprise_clean:
                object.__setattr__(self, "entreprise", None)
            elif len(entreprise_clean) < 2:
                raise ValueError(
                    "Le nom de l'entreprise doit contenir au moins 2 caractères si fourni."
                )
            elif len(entreprise_clean) > 200:
                raise ValueError(
                    "Le nom de l'entreprise ne doit pas dépasser 200 caractères."
                )
            else:
                object.__setattr__(self, "entreprise", entreprise_clean)

        # --- Ordre ---
        if not isinstance(self.ordre, int) or self.ordre < 0:
            raise ValueError("L'ordre doit être un entier positif ou zéro.")
        object.__setattr__(self, "ordre", self.ordre)

        # Actif est déjà booléen.

    def mettre_a_jour(
        self,
        nom: Optional[str] = None,
        texte: Optional[str] = None,
        photo_url: Optional[str] = None,
        entreprise: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> "Temoignage":
        """
        Retourne une nouvelle instance avec les champs modifiés.

        Args:
            nom: Nouveau nom.
            texte: Nouveau texte.
            photo_url: Nouvelle photo.
            entreprise: Nouvelle entreprise.
            actif: Visibilité.
            ordre: Ordre d'affichage.

        Returns:
            Temoignage: Nouvelle instance mise à jour.
        """
        return Temoignage(
            nom=nom if nom is not None else self.nom,
            texte=texte if texte is not None else self.texte,
            photo_url=photo_url if photo_url is not None else self.photo_url,
            entreprise=entreprise if entreprise is not None else self.entreprise,
            actif=actif if actif is not None else self.actif,
            ordre=ordre if ordre is not None else self.ordre,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire.

        Returns:
            dict: Données du témoignage.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "texte": self.texte,
            "photo_url": self.photo_url,
            "entreprise": self.entreprise,
            "actif": self.actif,
            "ordre": self.ordre,
        }

    def __repr__(self) -> str:
        return (
            f"Temoignage(id={self.id}, nom='{self.nom}', "
            f"entreprise='{self.entreprise}', actif={self.actif})"
        )