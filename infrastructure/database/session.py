"""
Session de base de données – Bridge Afrika Portfolio
=====================================================
Configure le moteur SQLAlchemy et fournit les sessions
utilisées par les repositories.

Utilisation :
    from infrastructure.database.session import get_db, SessionLocal, engine, Base
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# URL de la base de données (priorité à la variable d'environnement)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./bridge_afrika.db"  # Valeur par défaut : SQLite locale
)

# Création du moteur SQLAlchemy
# connect_args nécessaires uniquement pour SQLite (accès multi-thread)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,  # Mettre True pour voir les requêtes SQL
    )
else:
    # PostgreSQL ou autre
    engine = create_engine(DATABASE_URL, echo=False)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Fournit une session de base de données.
    À utiliser comme dépendance dans les routes (FastAPI) ou manuellement.

    Yields:
        Session: Une session SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Crée toutes les tables définies dans les modèles.
    À appeler au démarrage de l'application.
    """
    from infrastructure.database.models import Base
    Base.metadata.create_all(bind=engine)