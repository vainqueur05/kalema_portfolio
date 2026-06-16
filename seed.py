"""Script de seed pour données de test."""
from infrastructure.database.session import SessionLocal, init_db
from infrastructure.repositories.profil_repo_impl import ProfilRepositoryImpl
from infrastructure.repositories.projet_repo_impl import ProjetRepositoryImpl
from infrastructure.repositories.service_repo_impl import ServiceRepositoryImpl
from infrastructure.repositories.lien_contact_repo_impl import LienContactRepositoryImpl
from infrastructure.repositories.temoignage_repo_impl import TemoignageRepositoryImpl
from infrastructure.repositories.about_repo_impl import AboutRepositoryImpl
from domain.entities.profil import Profil
from domain.entities.projet import Projet
from domain.entities.service import Service
from domain.entities.lien_contact import LienContact
from domain.entities.temoignage import Temoignage
from domain.entities.about import About

init_db()
db = SessionLocal()

# Profil
profil_repo = ProfilRepositoryImpl(db)
profil_repo.sauvegarder(Profil(
    nom_complet="Vainqueur Kalema",
    titre="Développeur Fullstack Web & Consultant Numérique",
    bio="Passionné par la création de solutions web innovantes, je construis des ponts entre l'Afrique et le monde numérique.",
    photo_url="/static/uploads/profil.jpg"
))

# Projets (description_longue >= 50 caractères)
projet_repo = ProjetRepositoryImpl(db)
projets_data = [
    (
        "Bridge Afrika",
        "Plateforme de mise en relation pour les entrepreneurs africains",
        "Solution complète de gestion de projets collaboratifs intégrant chat, visioconférence et suivi budgétaire en temps réel.",
        "Né d'un besoin sur le terrain lors d'une mission humanitaire au Cameroun."
    ),
    (
        "E-Shop Pro",
        "Boutique en ligne clé en main avec paiement mobile intégré",
        "Système e-commerce robuste avec gestion de stock avancée, facturation automatique et support de multiples passerelles de paiement africaines.",
        ""
    ),
    (
        "AfriHealth",
        "Dossier patient numérique interopérable pour hôpitaux ruraux",
        "Application médicale permettant la centralisation des données patients, la télémédecine et l'analyse épidémiologique, même en zone de faible connectivité.",
        "Durant la pandémie, j'ai vu le besoin crucial d'un outil simple et accessible pour les dispensaires isolés."
    ),
]
for i, (titre, desc_c, desc_l, histoire) in enumerate(projets_data):
    projet_repo.ajouter(Projet(
        titre=titre, description_courte=desc_c, description_longue=desc_l, histoire=histoire, ordre=i
    ))

# Services (inchangés)
service_repo = ServiceRepositoryImpl(db)
services_data = [
    ("Développement Web", "Création de sites vitrines et applicatifs sur mesure.", 1500, "fa-solid fa-code"),
    ("API & Backend", "Conception d'APIs robustes avec FastAPI.", 2000, "fa-solid fa-server"),
    ("Conseil Technique", "Audit et accompagnement technologique.", 800, "fa-solid fa-lightbulb"),
]
for nom, desc, prix, icone in services_data:
    service_repo.ajouter(Service(nom=nom, description=desc, prix=prix, icone=icone, ordre=0))

# Liens de contact (inchangés)
lien_repo = LienContactRepositoryImpl(db)
liens_data = [
    ("WhatsApp", "https://wa.me/+243895288981", "fa-brands fa-whatsapp"),
    ("LinkedIn", "https://linkedin.com/in/vainqueur", "fa-brands fa-linkedin"),
    ("Email", "mailto:vainqueurkalema035@gmail.com", "fa-solid fa-envelope"),
]
for nom, url, icone in liens_data:
    lien_repo.ajouter(LienContact(nom=nom, url=url, icone=icone, ordre=0))

# Témoignages (inchangés)
temoignage_repo = TemoignageRepositoryImpl(db)
temoignages_data = [
    ("Alice", "Un travail remarquable, professionnel et efficace.", "Startup Manager"),
    ("Bob", "Vainqueur a su comprendre nos besoins et livrer au-delà de nos attentes.", "Fondateur TechCo"),
    ("Charlie", "Je recommande vivement pour tout projet web.", "Designer freelance"),
]
for nom, texte, entreprise in temoignages_data:
    temoignage_repo.ajouter(Temoignage(nom=nom, texte=texte, entreprise=entreprise))

# About
about_repo = AboutRepositoryImpl(db)
about_repo.sauvegarder(About(contenu="""
## Mon parcours

Développeur fullstack depuis plus de 5 ans, j'ai accompagné des startups et des ONG dans leur transformation numérique.

Mes valeurs : **innovation**, **rigueur**, **impact social**.
"""))

db.close()
print("✅ Données de test insérées.")