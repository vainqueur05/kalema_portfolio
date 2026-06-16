"""
Entité : Profil
================
Représente le profil professionnel unique du développeur.
Une seule instance modifiable depuis l'interface d'administration.

Fait partie du domaine métier (Clean Architecture) :
- Indépendant de toute technologie de persistance.
- Contient uniquement les attributs et les règles métier.
- Aucune dépendance à SQLAlchemy, Flask ou FastAPI.

Règles métier :
- nom_complet : obligatoire, 2 à 150 caractères, lettres/espaces/accents/tirets/apostrophes.
- titre : obligatoire, 2 à 200 caractères, autorise les symboles courants.
- bio : obligatoire, minimum 20 caractères (description significative).
- photo_url : optionnelle, mais si fournie doit être un chemin ou URL valide (format simple).
"""

from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class Profil:
    """
    Entité représentant le profil personnel du propriétaire du portfolio.

    Attributes:
        nom_complet (str): Nom complet du développeur.
        titre (str): Titre professionnel (ex: Développeur Fullstack Web).
        bio (str): Biographie détaillée.
        photo_url (Optional[str]): Chemin ou URL de la photo de profil.
        id (Optional[int]): Identifiant unique (None tant que non persisté).

    Raises:
        ValueError: Si l'un des champs obligatoires est invalide.
    """

    nom_complet: str
    titre: str
    bio: str
    photo_url: Optional[str] = None
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """
        Validation des champs après initialisation.
        Lève une exception ValueError avec un message explicite si une règle est violée.
        """
        # Validation du nom complet
        if not self.nom_complet or not self.nom_complet.strip():
            raise ValueError("Le nom complet est obligatoire.")
        nom_clean = self.nom_complet.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom complet doit contenir au moins 2 caractères.")
        if len(nom_clean) > 150:
            raise ValueError("Le nom complet ne doit pas dépasser 150 caractères.")
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'.]+$", nom_clean):
            raise ValueError(
                "Le nom complet contient des caractères non autorisés. "
                "Seuls les lettres, espaces, tirets, apostrophes et points sont acceptés."
            )
        object.__setattr__(self, "nom_complet", nom_clean)

        # Validation du titre (élargie pour accepter &, ,, (), etc.)
        if not self.titre or not self.titre.strip():
            raise ValueError("Le titre professionnel est obligatoire.")
        titre_clean = self.titre.strip()
        if len(titre_clean) < 2:
            raise ValueError("Le titre doit contenir au moins 2 caractères.")
        if len(titre_clean) > 200:
            raise ValueError("Le titre ne doit pas dépasser 200 caractères.")
        # Autorise : lettres, chiffres, espaces, tirets, slashs, apostrophes, esperluette,
        # virgule, point, parenthèses, crochets, dièse, arobase, points d'exclamation/interrogation
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-'/.&,()\[\]+#@!?]+$", titre_clean):
            raise ValueError(
                "Le titre contient des caractères non autorisés. "
                "Seuls les lettres, chiffres, espaces, tirets, slashs, apostrophes, "
                "esperluettes, virgules, points, parenthèses, crochets et quelques symboles sont acceptés."
            )
        object.__setattr__(self, "titre", titre_clean)

        # Validation de la bio
        if not self.bio or not self.bio.strip():
            raise ValueError("La biographie est obligatoire.")
        bio_clean = self.bio.strip()
        if len(bio_clean) < 20:
            raise ValueError(
                "La biographie doit contenir au moins 20 caractères pour être significative."
            )
        object.__setattr__(self, "bio", bio_clean)

        # Validation de la photo_url (si fournie)
        if self.photo_url is not None:
            photo_clean = self.photo_url.strip()
            if not photo_clean:
                # Si vide, on la met à None (pas de photo)
                object.__setattr__(self, "photo_url", None)
            else:
                # Vérification simple : commence par /, http:// ou https://
                if not (
                    photo_clean.startswith("/")
                    or photo_clean.startswith("http://")
                    or photo_clean.startswith("https://")
                ):
                    raise ValueError(
                        "La photo_url doit être un chemin relatif (commençant par '/') "
                        "ou une URL complète (http/https)."
                    )
                object.__setattr__(self, "photo_url", photo_clean)

    def mettre_a_jour(
        self,
        nom_complet: Optional[str] = None,
        titre: Optional[str] = None,
        bio: Optional[str] = None,
        photo_url: Optional[str] = None,
    ) -> "Profil":
        """
        Crée une nouvelle instance avec les champs modifiés (immuabilité pratique).
        Permet une mise à jour partielle tout en validant les nouvelles valeurs.

        Args:
            nom_complet (Optional[str]): Nouveau nom complet.
            titre (Optional[str]): Nouveau titre.
            bio (Optional[str]): Nouvelle biographie.
            photo_url (Optional[str]): Nouvelle photo.

        Returns:
            Profil: Nouvelle instance de Profil avec les champs mis à jour.
        """
        return Profil(
            nom_complet=nom_complet if nom_complet is not None else self.nom_complet,
            titre=titre if titre is not None else self.titre,
            bio=bio if bio is not None else self.bio,
            photo_url=photo_url if photo_url is not None else self.photo_url,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire (utile pour JSON ou templates).

        Returns:
            dict: Représentation du profil.
        """
        return {
            "id": self.id,
            "nom_complet": self.nom_complet,
            "titre": self.titre,
            "bio": self.bio,
            "photo_url": self.photo_url,
        }

    def __repr__(self) -> str:
        return (
            f"Profil(id={self.id}, nom='{self.nom_complet}', titre='{self.titre}')"
        )