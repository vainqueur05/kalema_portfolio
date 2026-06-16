"""
Service de mots de passe
=========================
Hashage et vérification avec bcrypt.
Indépendant du framework web.
"""

import bcrypt


class PasswordService:
    """
    Fournit des méthodes statiques pour hacher et vérifier les mots de passe.
    """

    @staticmethod
    def hacher(mot_de_passe: str) -> str:
        """
        Hash un mot de passe en utilisant bcrypt.

        Args:
            mot_de_passe: Mot de passe en clair.

        Returns:
            Le hash bcrypt (chaîne UTF-8).
        """
        # bcrypt nécessite des bytes
        pwd_bytes = mot_de_passe.encode("utf-8")
        # Génère un sel aléatoire et hash
        hash_bytes = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    @staticmethod
    def verifier(mot_de_passe: str, hash_stocke: str) -> bool:
        """
        Vérifie qu'un mot de passe correspond au hash stocké.

        Args:
            mot_de_passe: Le mot de passe en clair à vérifier.
            hash_stocke: Le hash bcrypt récupéré de la base.

        Returns:
            True si correspondance, False sinon.
        """
        pwd_bytes = mot_de_passe.encode("utf-8")
        hash_bytes = hash_stocke.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)