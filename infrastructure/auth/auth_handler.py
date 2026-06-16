"""
Gestionnaire d'authentification
================================
Utilise JWT pour sécuriser les routes admin.
Les tokens sont signés avec une clé secrète (variable d'environnement).
"""

import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "changez-moi-en-prod")
ALGORITHM = "HS256"
DUREE_TOKEN = timedelta(hours=8)  # Durée de validité du token


class AuthHandler:
    """
    Gère la création et la vérification des tokens JWT.
    """

    @staticmethod
    def creer_token(user_id: int, username: str) -> str:
        """
        Crée un token JWT pour un utilisateur authentifié.

        Args:
            user_id: ID de l'utilisateur dans la base.
            username: Nom d'utilisateur.

        Returns:
            Token JWT encodé (str).
        """
        payload = {
            "sub": str(user_id),
            "username": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + DUREE_TOKEN,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verifier_token(token: str) -> Optional[dict]:
        """
        Vérifie la validité d'un token JWT.

        Args:
            token: Token JWT à vérifier.

        Returns:
            Le payload décodé si valide, sinon None.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def extraire_user_id(token: str) -> Optional[int]:
        """
        Extrait l'ID utilisateur du token s'il est valide.

        Args:
            token: Token JWT.

        Returns:
            ID utilisateur ou None si token invalide.
        """
        payload = AuthHandler.verifier_token(token)
        if payload:
            return int(payload.get("sub"))
        return None