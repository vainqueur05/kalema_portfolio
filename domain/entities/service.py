"""
Entité : Service
=================
Représente une prestation proposée par le développeur.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- nom : obligatoire, 2 à 150 caractères.
- description : obligatoire, 20 à 500 caractères.
- prix : optionnel (float >= 0 si présent), masqué sur la page d'accueil.
- icone : optionnel, chaîne représentant une classe CSS (ex: 'fa-solid fa-code').
- actif : booléen (True = visible).
- ordre : entier >= 0, position d'affichage.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Service:
    """
    Entité représentant un service offert.

    Attributes:
        nom (str): Nom du service.
        description (str): Description détaillée.
        prix (Optional[float]): Prix du service (peut être None si non défini).
        icone (Optional[str]): Classe CSS de l'icône associée (ex: 'fa-solid fa-globe').
        actif (bool): Visibilité publique.
        ordre (int): Ordre d'affichage.
        id (Optional[int]): Identifiant technique (None avant persistance).

    Raises:
        ValueError: Si les contraintes métier sont violées.
    """

    nom: str
    description: str
    prix: Optional[float] = None
    icone: Optional[str] = None
    actif: bool = True
    ordre: int = 0
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation des champs après création."""
        # --- Nom ---
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du service est obligatoire.")
        nom_clean = self.nom.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom du service doit contenir au moins 2 caractères.")
        if len(nom_clean) > 150:
            raise ValueError("Le nom du service ne doit pas dépasser 150 caractères.")
        object.__setattr__(self, "nom", nom_clean)

        # --- Description ---
        if not self.description or not self.description.strip():
            raise ValueError("La description du service est obligatoire.")
        desc_clean = self.description.strip()
        if len(desc_clean) < 20:
            raise ValueError(
                "La description du service doit contenir au moins 20 caractères."
            )
        if len(desc_clean) > 500:
            raise ValueError(
                "La description du service ne doit pas dépasser 500 caractères."
            )
        object.__setattr__(self, "description", desc_clean)

        # --- Prix ---
        if self.prix is not None:
            if not isinstance(self.prix, (int, float)):
                raise ValueError("Le prix doit être un nombre.")
            if self.prix < 0:
                raise ValueError("Le prix ne peut pas être négatif.")
            # Stockage en float
            object.__setattr__(self, "prix", float(self.prix))
        # Si None, on laisse None

        # --- Icône ---
        if self.icone is not None:
            icone_clean = self.icone.strip()
            if not icone_clean:
                object.__setattr__(self, "icone", None)
            else:
                object.__setattr__(self, "icone", icone_clean)
        # Si None, on laisse None

        # --- Ordre ---
        if not isinstance(self.ordre, int) or self.ordre < 0:
            raise ValueError("L'ordre doit être un entier positif ou zéro.")
        object.__setattr__(self, "ordre", self.ordre)

        # Actif est déjà booléen, pas de validation supplémentaire.

    def mettre_a_jour(
        self,
        nom: Optional[str] = None,
        description: Optional[str] = None,
        prix: Optional[float] = None,
        icone: Optional[str] = None,
        actif: Optional[bool] = None,
        ordre: Optional[int] = None,
    ) -> "Service":
        """
        Retourne une nouvelle instance avec les champs modifiés (validation complète).

        Args:
            nom: Nouveau nom.
            description: Nouvelle description.
            prix: Nouveau prix.
            icone: Nouvelle icône.
            actif: Visibilité.
            ordre: Ordre d'affichage.

        Returns:
            Service: Nouvelle instance mise à jour.
        """
        return Service(
            nom=nom if nom is not None else self.nom,
            description=description if description is not None else self.description,
            prix=prix if prix is not None else self.prix,
            icone=icone if icone is not None else self.icone,
            actif=actif if actif is not None else self.actif,
            ordre=ordre if ordre is not None else self.ordre,
            id=self.id,
        )

    def to_dict(self) -> dict:
        """
        Convertit l'entité en dictionnaire pour sérialisation.

        Returns:
            dict: Données du service.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "prix": self.prix,
            "icone": self.icone,
            "actif": self.actif,
            "ordre": self.ordre,
        }

    def __repr__(self) -> str:
        return (
            f"Service(id={self.id}, nom='{self.nom}', prix={self.prix}, actif={self.actif})"
        )