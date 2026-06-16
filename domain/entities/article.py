"""
Entité : Article
================
Représente un article de blog.
"""

from dataclasses import dataclass, field
from typing import Optional
import re
import unicodedata


@dataclass
class Article:
    titre: str
    contenu: str
    slug: Optional[str] = None
    image_url: Optional[str] = None
    actif: bool = True
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        if not self.titre or not self.titre.strip():
            raise ValueError("Le titre est obligatoire.")
        titre_clean = self.titre.strip()
        object.__setattr__(self, "titre", titre_clean)

        if not self.contenu or not self.contenu.strip():
            raise ValueError("Le contenu est obligatoire.")
        object.__setattr__(self, "contenu", self.contenu.strip())

        if self.slug and self.slug.strip():
            slug_clean = self.slug.strip().lower().replace(" ", "-")
            object.__setattr__(self, "slug", slug_clean)
        else:
            object.__setattr__(self, "slug", self._generer_slug(titre_clean))

        if self.image_url is not None:
            img = self.image_url.strip()
            object.__setattr__(self, "image_url", img if img else None)

    @staticmethod
    def _generer_slug(texte: str) -> str:
        texte = unicodedata.normalize("NFKD", texte).encode("ASCII", "ignore").decode()
        texte = texte.lower().strip()
        texte = re.sub(r"[^a-z0-9\s-]", "", texte)
        texte = re.sub(r"\s+", "-", texte)
        texte = re.sub(r"-+", "-", texte).strip("-")
        return texte if texte else "article"

    def mettre_a_jour(self, **kwargs) -> "Article":
        return Article(
            titre=kwargs.get("titre", self.titre),
            contenu=kwargs.get("contenu", self.contenu),
            slug=kwargs.get("slug", self.slug),
            image_url=kwargs.get("image_url", self.image_url),
            actif=kwargs.get("actif", self.actif),
            id=self.id,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titre": self.titre,
            "slug": self.slug,
            "contenu": self.contenu,
            "image_url": self.image_url,
            "actif": self.actif,
        }