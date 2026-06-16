"""
Routes Publiques – Bridge Afrika Portfolio
===========================================
Gère toutes les pages de la vitrine publique.
Injection des services métier via dépendances FastAPI.
Inclut le tracking de visite et la vérification du mode maintenance.
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from infrastructure.database.session import get_db
from infrastructure.repositories.profil_repo_impl import ProfilRepositoryImpl
from infrastructure.repositories.projet_repo_impl import ProjetRepositoryImpl
from infrastructure.repositories.service_repo_impl import ServiceRepositoryImpl
from infrastructure.repositories.lien_contact_repo_impl import LienContactRepositoryImpl
from infrastructure.repositories.temoignage_repo_impl import TemoignageRepositoryImpl
from infrastructure.repositories.about_repo_impl import AboutRepositoryImpl
from infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
from infrastructure.repositories.visite_repo_impl import VisiteRepositoryImpl
from infrastructure.repositories.article_repo_impl import ArticleRepositoryImpl
from infrastructure.services.geo_service_impl import GeoServiceImpl
from infrastructure.services.maintenance_service_impl import MaintenanceServiceImpl

from application.use_cases.profil_service import ProfilService
from application.use_cases.projet_service import ProjetService
from application.use_cases.service_service import ServiceService
from application.use_cases.lien_contact_service import LienContactService
from application.use_cases.temoignage_service import TemoignageService
from application.use_cases.about_service import AboutService
from application.use_cases.contact_service import ContactService
from application.use_cases.visite_service import VisiteService
from application.use_cases.article_service import ArticleService

router = APIRouter()
templates = Jinja2Templates(directory="presentation/public/templates")


# ------------------------------------------------------------------
# Fonctions utilitaires de dépendances
# ------------------------------------------------------------------

def get_profil_service(db: Session = Depends(get_db)) -> ProfilService:
    return ProfilService(ProfilRepositoryImpl(db))


def get_projet_service(db: Session = Depends(get_db)) -> ProjetService:
    return ProjetService(ProjetRepositoryImpl(db))


def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    return ServiceService(ServiceRepositoryImpl(db))


def get_lien_contact_service(db: Session = Depends(get_db)) -> LienContactService:
    return LienContactService(LienContactRepositoryImpl(db))


def get_temoignage_service(db: Session = Depends(get_db)) -> TemoignageService:
    return TemoignageService(TemoignageRepositoryImpl(db))


def get_about_service(db: Session = Depends(get_db)) -> AboutService:
    return AboutService(AboutRepositoryImpl(db))


def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(ContactRepositoryImpl(db))


def get_visite_service(db: Session = Depends(get_db)) -> VisiteService:
    return VisiteService(
        VisiteRepositoryImpl(db),
        GeoServiceImpl()
    )


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(ArticleRepositoryImpl(db))


def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceServiceImpl:
    return MaintenanceServiceImpl(db)


# ------------------------------------------------------------------
# Dépendance de vérification du mode maintenance
# ------------------------------------------------------------------

def check_maintenance(request: Request, maintenance_service: MaintenanceServiceImpl = Depends(get_maintenance_service)):
    # Ne pas rediriger la page maintenance elle-même
    if request.url.path == "/maintenance":
        return True
    # Ne pas rediriger les fichiers statiques
    if request.url.path.startswith("/static"):
        return True
    # Si maintenance active, rediriger
    if maintenance_service.est_actif():
        return RedirectResponse("/maintenance", status_code=302)
    return True


# ------------------------------------------------------------------
# Dépendance d'enregistrement de visite
# ------------------------------------------------------------------

def track_visite(
    request: Request,
    visite_service: VisiteService = Depends(get_visite_service),
    maintenance_service: MaintenanceServiceImpl = Depends(get_maintenance_service)
):
    # Ne pas tracker si maintenance (évite visites inutiles)
    if maintenance_service.est_actif():
        return
    visite_service.enregistrer_visite(
        page=request.url.path,
        ip=request.client.host if request.client else "inconnue",
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer"),
    )
    return True


# ------------------------------------------------------------------
# Route : maintenance
# ------------------------------------------------------------------

@router.get("/maintenance", response_class=HTMLResponse)
def page_maintenance(request: Request):
    """Affiche la page de maintenance."""
    return templates.TemplateResponse("maintenance.html", {"request": request})


# ------------------------------------------------------------------
# Route : Accueil (SPA)
# ------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def accueil(
    request: Request,
    profil_service: ProfilService = Depends(get_profil_service),
    projet_service: ProjetService = Depends(get_projet_service),
    service_service: ServiceService = Depends(get_service_service),
    temoignage_service: TemoignageService = Depends(get_temoignage_service),
    lien_service: LienContactService = Depends(get_lien_contact_service),
    about_service: AboutService = Depends(get_about_service),
    article_service: ArticleService = Depends(get_article_service),
):
    """
    Page d'accueil immersive avec toutes les sections.
    Les données sont récupérées depuis les services métier.
    """
    profil = profil_service.recuperer_profil()
    projets = projet_service.lister_projets(actif_seulement=True)
    services = service_service.lister_services(actif_seulement=True)
    temoignages = temoignage_service.lister_temoignages(actif_seulement=True)
    liens = lien_service.lister_liens(actif_seulement=True)
    about = about_service.recuperer_contenu()
    articles = article_service.lister_articles(actif_seulement=True)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "profil": profil,
        "projets": projets,
        "services": services,
        "temoignages": temoignages,
        "liens": liens,
        "about": about,
        "articles": articles,
    })


# ------------------------------------------------------------------
# Route : Détail d'un projet
# ------------------------------------------------------------------

@router.get("/projet/{slug}", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def detail_projet(
    slug: str,
    request: Request,
    projet_service: ProjetService = Depends(get_projet_service),
):
    """Affiche la page de détail d'un projet."""
    projet = projet_service.recuperer_projet_par_slug(slug)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return templates.TemplateResponse("projet_detail.html", {
        "request": request,
        "projet": projet,
    })


# ------------------------------------------------------------------
# Route : Services
# ------------------------------------------------------------------

@router.get("/services", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def liste_services(
    request: Request,
    service_service: ServiceService = Depends(get_service_service),
):
    """Affiche la liste des services avec prix."""
    services = service_service.lister_services(actif_seulement=True)
    return templates.TemplateResponse("services.html", {
        "request": request,
        "services": services,
    })


# ------------------------------------------------------------------
# Route : À propos
# ------------------------------------------------------------------

@router.get("/a-propos", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def a_propos(
    request: Request,
    about_service: AboutService = Depends(get_about_service),
):
    """Affiche la page À propos complète."""
    about = about_service.recuperer_contenu()
    return templates.TemplateResponse("a_propos.html", {
        "request": request,
        "about": about,
    })


# ------------------------------------------------------------------
# Route : Contact (GET + POST)
# ------------------------------------------------------------------

@router.get("/contact", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def formulaire_contact(
    request: Request,
    lien_service: LienContactService = Depends(get_lien_contact_service),
):
    """Affiche le formulaire de contact et les liens."""
    liens = lien_service.lister_liens(actif_seulement=True)
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "liens": liens,
    })


@router.post("/contact", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def soumettre_contact(
    request: Request,
    nom: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    telephone: str = Form(None),
    contact_service: ContactService = Depends(get_contact_service),
    lien_service: LienContactService = Depends(get_lien_contact_service),
):
    """Réceptionne un message depuis le formulaire public."""
    try:
        contact_service.envoyer_message(
            nom=nom, email=email, message=message, telephone=telephone
        )
        success = "Votre message a été envoyé avec succès !"
    except ValueError as e:
        success = None
        erreur = str(e)
    else:
        erreur = None

    liens = lien_service.lister_liens(actif_seulement=True)
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "liens": liens,
        "success": success,
        "erreur": erreur,
        "nom": nom,
        "email": email,
        "message": message,
        "telephone": telephone,
    })


# ------------------------------------------------------------------
# Route : Blog (liste)
# ------------------------------------------------------------------

@router.get("/blog", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def blog_list(
    request: Request,
    article_service: ArticleService = Depends(get_article_service),
):
    """Affiche la liste des articles de blog."""
    articles = article_service.lister_articles(actif_seulement=True)
    return templates.TemplateResponse("blog_list.html", {
        "request": request,
        "articles": articles,
    })


# ------------------------------------------------------------------
# Route : Blog (détail)
# ------------------------------------------------------------------

@router.get("/blog/{slug}", response_class=HTMLResponse, dependencies=[Depends(check_maintenance), Depends(track_visite)])
def blog_detail(
    slug: str,
    request: Request,
    article_service: ArticleService = Depends(get_article_service),
):
    """Affiche un article de blog."""
    article = article_service.recuperer_par_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return templates.TemplateResponse("blog_detail.html", {
        "request": request,
        "article": article,
    })