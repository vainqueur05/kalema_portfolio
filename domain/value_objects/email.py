"""
Value Object : Email
====================
Représente une adresse email valide dans le domaine métier.

Un Value Object est immuable (une fois créé, il ne change pas).
Si la valeur change, on crée une nouvelle instance.
Cela garantit l'intégrité des données dans toute l'application.

Respecte le principe de Clean Architecture :
- Aucune dépendance externe (pas de base de données, pas de framework).
- Contient uniquement la logique de validation métier.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)  # frozen=True rend l'objet immuable
class Email:
    """
    Value Object représentant une adresse email.

    Attributes:
        value (str): L'adresse email nettoyée et validée.

    Raises:
        ValueError: Si l'email fourni est invalide.

    Example:
        >>> email = Email("vainqueur@bridge-afrika.com")
        >>> str(email)
        'vainqueur@bridge-afrika.com'
    """

    value: str

    def __post_init__(self):
        """
        Méthode appelée automatiquement après l'initialisation.
        Nous l'utilisons pour valider l'email.
        Comme l'objet est frozen, nous devons utiliser object.__setattr__
        pour modifier les attributs (contournement du frozen pour la validation).
        """
        # Nettoyage : suppression des espaces en début et fin
        cleaned = self.value.strip().lower() if self.value else ""

        # Vérification : l'email ne doit pas être vide
        if not cleaned:
            raise ValueError("L'adresse email ne peut pas être vide.")

        # Vérification : format valide selon la norme simplifiée
        if not self._is_valid_email(cleaned):
            raise ValueError(
                f"L'adresse email '{cleaned}' n'est pas valide. "
                f"Format attendu : exemple@domaine.com"
            )

        # Comme l'objet est frozen, on force la modification de l'attribut
        object.__setattr__(self, "value", cleaned)

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Valide le format de l'email avec une expression régulière.

        Règles appliquées :
        - Partie locale (avant le @) : lettres, chiffres, points, tirets, underscores
        - Un @ obligatoire
        - Partie domaine : lettres, chiffres, tirets, points
        - Extension : au moins 2 lettres (ex: .com, .fr, .org)

        Args:
            email (str): L'email à valider.

        Returns:
            bool: True si l'email est valide, False sinon.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        """Retourne la valeur de l'email sous forme de chaîne."""
        return self.value

    def __repr__(self) -> str:
        """Représentation technique pour le débogage."""
        return f"Email('{self.value}')"

    @property
    def domaine(self) -> str:
        """
        Extrait le nom de domaine de l'email.

        Returns:
            str: La partie après le @ (ex: 'bridge-afrika.com')
        """
        return self.value.split("@")[1] if "@" in self.value else ""

    @property
    def masque(self) -> str:
        """
        Masque partiellement l'email pour l'affichage public.
        Utile pour protéger contre les robots spammeurs.

        Returns:
            str: Email masqué (ex: 'v*****r@bridge-afrika.com')
        """
        local, domaine = self.value.split("@")
        if len(local) > 2:
            masque_local = local[0] + "*" * (len(local) - 2) + local[-1]
        else:
            masque_local = local[0] + "*" * (len(local) - 1)
        return f"{masque_local}@{domaine}"