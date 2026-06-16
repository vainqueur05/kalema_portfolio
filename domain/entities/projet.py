"""
Entité : Projet
================
Représente un projet réalisé par le développeur, présenté dans le portfolio.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- titre : obligatoire, 2 à 200 caractères.
- slug : obligatoire, généré automatiquement à partir du titre si non fourni,
  format : minuscules, lettres, chiffres, tirets, sans accents.
- description_courte : obligatoire, 20 à 300 caractères (accroche).
- description_longue : obligatoire, 50 à 5000 caractères (détail technique).
- histoire : optionnelle, texte libre qui raconte l'histoire du projet.
- image_url : optionnelle, chemin ou URL valide.
- actif : booléen (True = visible publiquement, False = masqué).
- ordre : entier >= 0, détermine la position d'affichage.
- created_at : NON inclus ici, géré par la couche infrastructure.
"""

from dataclasses import dataclass, field
from typing import Optional
import re
import unicodedata


@dataclass
class Projet:
    """
    Entité représentant un projet du portfolio.

    Attributes:
        titre (str): Titre du projet.
        slug (str): Identifiant unique dans l'URL (généré automatiquement).
        description_courte (str): Résumé attractif (20-300 caractères).
        description_longue (str): Description complète (50-5000 caractères).
        histoire (str): Histoire narrative du projet (peut être vide).
        image_url (Optional[str]): Chemin ou URL de l'image principale.
        actif (bool): Visibilité du projet (True par défaut).
        ordre (int): Ordre d'affichage (0 = premier).
        id (Optional[int]): Identifiant technique (None avant persistance).

    Raises:
        ValueError: Si l'un des champs obligatoires ne respecte pas les règles.
    """

    titre: str
    description_courte: str
    description_longue: str
    slug: Optional[str] = None
    histoire: str = ""
    image_url: Optional[str] = None
    actif: bool = True
    ordre: int = 0
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation et nettoyage des champs après initialisation."""
        # --- Titre ---
        if not self.titre or not self.titre.strip():
            raise ValueError("Le titre du projet est obligatoire.")
        titre_clean = self.titre.strip()
        if len(titre_clean) < 2:
            raise ValueError("Le titre doit contenir au moins 2 caractères.")
        if len(titre_clean) > 200:
            raise ValueError("Le titre ne doit pas dépasser 200 caractères.")
        object.__setattr__(self, "titre", titre_clean)

        # --- Slug ---
        if self.slug is not None and self.slug.strip():
            slug_clean = self.slug.strip()
            if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug_clean):
                raise ValueError(
                    "Le slug doit contenir uniquement des lettres minuscules, "
                    "des chiffres et des tirets (ex: mon-projet-1)."
                )
            object.__setattr__(self, "slug", slug_clean)
        else:
            # Génération automatique du slug à partir du titre
            object.__setattr__(self, "slug", self._generer_slug(self.titre))

        # --- Description courte ---
        if not self.description_courte or not self.description_courte.strip():
            raise ValueError("La description courte est obligatoire.")
        desc_c_clean = self.description_courte.strip()
        if len(desc_c_clean) < 20:
            raise ValueError(
                "La description courte doit contenir au moins 20 caractères."
            )
        if len(desc_c_clean) > 300:
            raise ValueError(
                "La description courte ne doit pas dépasser 300 caractères."
            )
        object.__setattr__(self, "description_courte", desc_c_clean)

        # --- Description longue ---
        if not self.description_longue or not self.description_longue.strip():
            raise ValueError("La description longue est obligatoire.")
        desc_l_clean = self.description_longue.strip()
        if len(desc_l_clean) < 50:
            raise ValueError(
                "La description longue doit contenir au moins 50 caractères."
            )
        if len(desc_l_clean) > 5000:
            raise ValueError(
                "La description longue ne doit pas dépasser 5000 caractères."
            )
        object.__setattr__(self, "description_longue", desc_l_clean)

        # --- Histoire ---
        if self.histoire:
            histoire_clean = self.histoire.strip()
            object.__setattr__(self, "histoire", histoire_clean)
        else:
            object.__setattr__(self, "histoire", "")

        # --- Image URL ---
        if self.image_url is not None:
            img_clean = self.image_url.strip()
            if not img_clean:
                object.__setattr__(self, "image_url", None)
            elif not (
                img_clean.startswith("/")
                or img_clean.startswith("http://")
                or img_clean.startswith("https://")
            ):
                raise ValueError(
                    "L'URL de l'image doit être un chemin relatif (commençant par '/') "
                    "ou une URL complète (http/https)."
                )
            else:
                object.__setattr__(self, "image_url", img_clean)

        # --- Actif (booléen, déjà typé) ---
        # Pas de validation supplémentaire.

        # --- Ordre ---
        if not isinstance(self.ordre, int) or self.ordre < 0:
            raise ValueError("L'ordre doit être un entier positif ou zéro.")
        object.__setattr__(self, "ordre", self.ordre)

    @staticmethod
    def _generer_slug(texte: str) -> str:
        """
        Génère un slug SEO-friendly à partir d'un texte.
        - Suppression des accents
        - Conversion en minuscules
        - Remplacement des espaces par des tirets
        - Suppression de tout caractère non alphanumérique (sauf tirets)

        Args:
            texte (str): Le texte à transformer.

        Returns:
            str: Le slug nettoyé.
        """
        texte = unicodedata.normalize("NFKD", texte).encode("ASCII", "ignore").decode()
        texte = texte.lower().strip()
        # Remplace tout ce qui n'est pas alphanumérique ou espace par un tiret
        texte = re.sub(r"[^a-z0-9\s-]", "", texte)
        texte = re.sub(r"\s+", "-", texte)
        texte = re.sub(r"-+", "-", texte).strip("-")
        if not texte:
            raise ValueError(
                "Impossible de générer un slug valide à partir du titre fourni. "
                "Veuillez fournir un slug manuellement."
            )
        return texte

    def mettre_a_jour(
        self,
        titre: Optional[str] = None,
        description_courte: Optional[str] = None,
        description_longue: Optional[str] = None,
        slug: Optional[str] = None,
        histoire: Optional[str] = None,
        image_url: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> "Projet":
        """
        Crée une nouvelle instance de Projet avec les champs mis à jour.
        La validation est ré-exécutée complètement.

        Args:
            titre: Nouveau titre.
            description_courte: Nouvelle description courte.
            description_longue: Nouvelle description longue.
            slug: Nouveau slug (généré si None et titre fourni).
            histoire: Nouvelle histoire.
            image_url: Nouvelle URL d'image.
            actif: Visibilité (True/False).
            ordre: Nouvel ordre d'affichage.

        Returns:
            Projet: Une nouvelle instance avec les modifications.
        """
        return Projet(
            titre=titre if titre is not None else self.titre,
            description_courte=description_courte if description_courte is not None else self.description_courte,
            description_longue=description_longue if description_longue is not None else self.description_longue,
            slug=slug if slug is not None else self.slug,
            histoire=histoire if histoire is not None else self.histoire,
            image_url=image_url if image_url is not None else self.image_url,
            actif=actif if actif is not None else self.actif,
            ordre=ordre if ordre is not None else self.ordre,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire pour les APIs/templates.

        Returns:
            dict: Représentation du projet.
        """
        return {
            "id": self.id,
            "titre": self.titre,
            "slug": self.slug,
            "description_courte": self.description_courte,
            "description_longue": self.description_longue,
            "histoire": self.histoire,
            "image_url": self.image_url,
            "actif": self.actif,
            "ordre": self.ordre,
        }

    def __repr__(self) -> str:
        return (
            f"Projet(id={self.id}, titre='{self.titre}', slug='{self.slug}', "
            f"actif={self.actif})"
        )