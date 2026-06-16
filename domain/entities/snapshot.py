"""
Entité : Snapshot
==================
Représente une sauvegarde de l'état complet ou partiel du contenu du portfolio.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- nom : obligatoire, 2 à 200 caractères (libellé de la sauvegarde).
- donnees_json : obligatoire, dict sérialisable en JSON (structure libre,
  mais typiquement un snapshot des tables de contenu).
- created_at : NON inclus, géré par la couche infrastructure.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json


@dataclass
class Snapshot:
    """
    Entité représentant un snapshot de données.

    Attributes:
        nom (str): Nom descriptif du snapshot.
        donnees_json (Dict[str, Any]): Données sauvegardées (doit être sérialisable).
        id (Optional[int]): Identifiant technique.
    """

    nom: str
    donnees_json: Dict[str, Any]
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation."""
        # --- Nom ---
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du snapshot est obligatoire.")
        nom_clean = self.nom.strip()
        if len(nom_clean) < 2:
            raise ValueError("Le nom du snapshot doit contenir au moins 2 caractères.")
        if len(nom_clean) > 200:
            raise ValueError("Le nom du snapshot ne doit pas dépasser 200 caractères.")
        object.__setattr__(self, "nom", nom_clean)

        # --- Données JSON ---
        if not isinstance(self.donnees_json, dict):
            raise ValueError("Les données du snapshot doivent être un dictionnaire.")
        # Vérifier que c'est sérialisable en JSON (sans lever d'exception)
        try:
            json.dumps(self.donnees_json, default=str)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Les données du snapshot ne sont pas sérialisables : {e}")
        # On ne modifie pas, on garde le dict tel quel
        # (éviter de réassigner pour frozen-like)

    def to_dict(self) -> dict:
        """
        Sérialise l'entité en dictionnaire.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "donnees_json": self.donnees_json,
        }

    def __repr__(self) -> str:
        return f"Snapshot(id={self.id}, nom='{self.nom}')"