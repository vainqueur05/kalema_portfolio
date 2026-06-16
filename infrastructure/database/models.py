"""
Modèles SQLAlchemy – Bridge Afrika Portfolio
=============================================
Définit les tables de la base de données utilisées pour persister
les entités du domaine. Ces modèles sont indépendants de la logique
métier et servent uniquement à l'infrastructure de persistance.

Chaque modèle correspond à une table du cahier des charges (section 5.2).
"""

from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ProfilModel(Base):
    """
    Table unique pour le profil du développeur.
    Une seule ligne modifiable.
    """
    __tablename__ = "profil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_url = Column(String(500), nullable=True)
    nom_complet = Column(String(150), nullable=False)
    titre = Column(String(200), nullable=False)
    bio = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Profil {self.nom_complet}>"


class ProjetModel(Base):
    """
    Projets du portfolio.
    """
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    description_courte = Column(String(300), nullable=False)
    description_longue = Column(Text, nullable=False)
    histoire = Column(Text, default="")
    image_url = Column(String(500), nullable=True)
    actif = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Projet {self.titre}>"


class ServiceModel(Base):
    """
    Services proposés.
    """
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)
    prix = Column(Float, nullable=True)
    icone = Column(String(100), nullable=True)
    actif = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)

    def __repr__(self):
        return f"<Service {self.nom}>"


class LienContactModel(Base):
    """
    Liens de contact (réseaux sociaux, email, etc.).
    """
    __tablename__ = "liens_contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    url = Column(String(2000), nullable=False)
    icone = Column(String(100), nullable=False)
    actif = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)

    def __repr__(self):
        return f"<LienContact {self.nom}>"


class TemoignageModel(Base):
    """
    Témoignages clients.
    """
    __tablename__ = "temoignages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    texte = Column(Text, nullable=False)
    photo_url = Column(String(500), nullable=True)
    entreprise = Column(String(200), nullable=True)
    actif = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)

    def __repr__(self):
        return f"<Temoignage {self.nom}>"


class AboutModel(Base):
    """
    Contenu de la page "À propos" (une seule ligne).
    """
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contenu = Column(Text, nullable=False)

    def __repr__(self):
        return "<About>"


class ContactModel(Base):
    """
    Messages reçus via le formulaire de contact.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(320), nullable=False)  # Email stocké comme chaîne
    telephone = Column(String(30), nullable=True)
    message = Column(Text, nullable=False)
    statut = Column(String(20), default="Nouveau")  # Nouveau, Lu, Répondu
    note_admin = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.nom} - {self.statut}>"


class VisiteModel(Base):
    """
    Visites enregistrées sur le site public.
    """
    __tablename__ = "visites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    page = Column(String(500), nullable=False)
    ip = Column(String(45), nullable=False)  # IPv6 max 45 chars
    user_agent = Column(Text, nullable=True)
    referrer = Column(String(2000), nullable=True)
    pays = Column(String(100), nullable=True)
    ville = Column(String(100), nullable=True)
    navigateur = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    appareil = Column(String(100), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Visite {self.page} - {self.date}>"


class SnapshotModel(Base):
    """
    Sauvegardes instantanées du contenu.
    """
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(200), nullable=False)
    donnees_json = Column(JSON, nullable=False)  # Stockage natif JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Snapshot {self.nom}>"


class UserModel(Base):
    """
    Utilisateurs pour l'authentification admin.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class SettingModel(Base):
    """
    Stockage clé/valeur pour les paramètres (ex: maintenance_mode).
    """
    __tablename__ = "settings"

    cle = Column(String(50), primary_key=True)
    valeur = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<Setting {self.cle}={self.valeur}>"

class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    contenu = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)