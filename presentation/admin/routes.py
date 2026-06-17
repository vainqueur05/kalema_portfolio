"""
Routes Admin – Bridge Afrika Portfolio
=======================================
Toutes les routes protégées du tableau de bord.
Authentification JWT obligatoire.
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid

from infrastructure.database.session import get_db
from infrastructure.repositories.profil_repo_impl import ProfilRepositoryImpl
from infrastructure.repositories.projet_repo_impl import ProjetRepositoryImpl
from infrastructure.repositories.service_repo_impl import ServiceRepositoryImpl
from infrastructure.repositories.lien_contact_repo_impl import LienContactRepositoryImpl
from infrastructure.repositories.temoignage_repo_impl import TemoignageRepositoryImpl
from infrastructure.repositories.about_repo_impl import AboutRepositoryImpl
from infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
from infrastructure.repositories.visite_repo_impl import VisiteRepositoryImpl
from infrastructure.repositories.snapshot_repo_impl import SnapshotRepositoryImpl
from infrastructure.services.maintenance_service_impl import MaintenanceServiceImpl
from infrastructure.auth.auth_handler import AuthHandler
from infrastructure.auth.password_service import PasswordService
from infrastructure.database.models import UserModel

from application.use_cases.profil_service import ProfilService
from application.use_cases.projet_service import ProjetService
from application.use_cases.service_service import ServiceService
from application.use_cases.lien_contact_service import LienContactService
from application.use_cases.temoignage_service import TemoignageService
from application.use_cases.about_service import AboutService
from application.use_cases.contact_service import ContactService
from application.use_cases.visite_service import VisiteService
from application.use_cases.snapshot_service import SnapshotService
from datetime import datetime, timedelta


router = APIRouter()
templates = Jinja2Templates(directory="presentation/admin/templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Services (dépendances)
# ------------------------------------------------------------------
def get_profil_service(db: Session = Depends(get_db)) -> ProfilService:
    return ProfilService(ProfilRepositoryImpl(db))

def get_projet_service(db: Session = Depends(get_db)) -> ProjetService:
    return ProjetService(ProjetRepositoryImpl(db))

def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    return ServiceService(ServiceRepositoryImpl(db))

def get_lien_service(db: Session = Depends(get_db)) -> LienContactService:
    return LienContactService(LienContactRepositoryImpl(db))

def get_temoignage_service(db: Session = Depends(get_db)) -> TemoignageService:
    return TemoignageService(TemoignageRepositoryImpl(db))

def get_about_service(db: Session = Depends(get_db)) -> AboutService:
    return AboutService(AboutRepositoryImpl(db))

def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(ContactRepositoryImpl(db))

def get_visite_service(db: Session = Depends(get_db)) -> VisiteService:
    from infrastructure.services.geo_service_impl import GeoServiceImpl
    return VisiteService(VisiteRepositoryImpl(db), GeoServiceImpl())

def get_snapshot_service(db: Session = Depends(get_db)) -> SnapshotService:
    return SnapshotService(
        SnapshotRepositoryImpl(db),
        ProfilRepositoryImpl(db),
        ProjetRepositoryImpl(db),
        ServiceRepositoryImpl(db),
        LienContactRepositoryImpl(db),
        TemoignageRepositoryImpl(db),
        AboutRepositoryImpl(db),
    )

def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceServiceImpl:
    return MaintenanceServiceImpl(db)

# ------------------------------------------------------------------
# Authentification (cookie + redirection)
# ------------------------------------------------------------------
def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[UserModel]:
    token = request.cookies.get("admin_token")
    if not token:
        return None
    payload = AuthHandler.verifier_token(token)
    if not payload:
        return None
    user_id = int(payload.get("sub"))
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def admin_required(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/admin/login", status_code=302)
    return user

# ------------------------------------------------------------------
# LOGIN / LOGOUT (inchangés)
# ------------------------------------------------------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})
# Journal de sécurité (stocké en mémoire)
security_log = []

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), 
           code_2fa: Optional[str] = Form(None), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    # Vérification identifiants
    if not user or not PasswordService.verifier(password, user.password_hash):
        security_log.append({
            "timestamp": datetime.now(), "ip": request.client.host,
            "username": username, "status": "ÉCHEC", "detail": "Mot de passe incorrect"
        })
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Identifiants incorrects."
        }, status_code=401)
    
    # Si pas de code 2FA fourni, afficher le champ 2FA
    if not code_2fa:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "show_2fa": True,
            "username": username,
            "password": password
        })
    
    # Vérification 2FA
    if code_2fa != "00Kale":
        security_log.append({
            "timestamp": datetime.now(), "ip": request.client.host,
            "username": username, "status": "ÉCHEC", "detail": "Code 2FA incorrect"
        })
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Code de sécurité incorrect.",
            "show_2fa": True,
            "username": username,
            "password": password
        }, status_code=401)
    
    # Connexion réussie
    security_log.append({
        "timestamp": datetime.now(), "ip": request.client.host,
        "username": username, "status": "SUCCÈS", "detail": "Connexion réussie avec 2FA"
    })
    
    token = AuthHandler.creer_token(user.id, user.username)
    response = RedirectResponse("/admin", status_code=302)
    response.set_cookie(key="admin_token", value=token, httponly=True, samesite="strict")
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/admin/login", status_code=302)
    response.delete_cookie("admin_token")
    return response

# ------------------------------------------------------------------
# JOURNAL DE SÉCURITÉ
# ------------------------------------------------------------------
@router.get("/security", response_class=HTMLResponse)
def security_dashboard(request: Request, user: UserModel = Depends(admin_required)):
    """Affiche le journal de sécurité des 24 dernières heures."""
    recent = [entry for entry in security_log 
              if entry["timestamp"] > datetime.now() - timedelta(hours=24)]
    return templates.TemplateResponse("security_log.html", {
        "request": request,
        "logs": recent[::-1]
    })


# ------------------------------------------------------------------
# DASHBOARD (inchangé)
# ------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: UserModel = Depends(admin_required),
              profil_service: ProfilService = Depends(get_profil_service),
              projet_service: ProjetService = Depends(get_projet_service),
              service_service: ServiceService = Depends(get_service_service),
              temoignage_service: TemoignageService = Depends(get_temoignage_service),
              contact_service: ContactService = Depends(get_contact_service),
              visite_service: VisiteService = Depends(get_visite_service)):
    profil = profil_service.recuperer_profil()
    projets = projet_service.lister_projets()
    services = service_service.lister_services()
    temoignages = temoignage_service.lister_temoignages()
    
    # RÉCUPÉRATION DE TOUS LES CONTACTS (liste)
    contacts = contact_service.lister_messages()  # retourne une liste d'entités Contact
    
    # Vérification de sécurité (optionnelle mais recommandée)
    if not isinstance(contacts, list):
        contacts = list(contacts)
    
    nb_nouveaux = len([c for c in contacts if c.statut == "Nouveau"])
    stats = visite_service.obtenir_statistiques()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "profil": profil,
        "nb_projets": len(projets),
        "nb_services": len(services),
        "nb_temoignages": len(temoignages),
        "nb_nouveaux_contacts": nb_nouveaux,
        "projets": projets,
        "services": services,
        "temoignages": temoignages,
        "contacts": contacts,          # <-- BIEN PASSÉE
        "stats": stats,
    })
# ------------------------------------------------------------------
# PROFIL (unique)
# ------------------------------------------------------------------
@router.get("/profil", response_class=HTMLResponse)
def edit_profil(request: Request, user: UserModel = Depends(admin_required),
                profil_service: ProfilService = Depends(get_profil_service)):
    profil = profil_service.recuperer_profil()
    return templates.TemplateResponse("profil_edit.html", {"request": request, "profil": profil})

@router.post("/profil")
def save_profil(request: Request, nom_complet: str = Form(...), titre: str = Form(...),
                bio: str = Form(...), photo_url: Optional[str] = Form(None),
                user: UserModel = Depends(admin_required),
                profil_service: ProfilService = Depends(get_profil_service)):
    try:
        profil_service.mettre_a_jour_profil(nom_complet=nom_complet, titre=titre, bio=bio, photo_url=photo_url)
        return RedirectResponse("/admin/profil?success=1", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("profil_edit.html", {"request": request, "error": str(e)})

# ------------------------------------------------------------------
# PROJETS (CRUD)
# ------------------------------------------------------------------
@router.get("/projets", response_class=HTMLResponse)
def list_projets(request: Request, user: UserModel = Depends(admin_required),
                 projet_service: ProjetService = Depends(get_projet_service)):
    projets = projet_service.lister_projets()
    return templates.TemplateResponse("projets_list.html", {"request": request, "projets": projets})

@router.get("/projets/ajouter", response_class=HTMLResponse)
def add_projet_form(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("projet_form.html", {"request": request, "projet": None})

@router.post("/projets/ajouter")
def add_projet(request: Request, titre: str = Form(...), description_courte: str = Form(...),
               description_longue: str = Form(...), slug: Optional[str] = Form(None),
               histoire: str = Form(""), image: Optional[UploadFile] = File(None),
               actif: bool = Form(True), ordre: int = Form(0),
               user: UserModel = Depends(admin_required),
               projet_service: ProjetService = Depends(get_projet_service)):
    image_url = None
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1]
        unique = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        image_url = f"/static/uploads/{unique}"

    try:
        projet_service.creer_projet(titre=titre, description_courte=description_courte,
                                    description_longue=description_longue, slug=slug,
                                    histoire=histoire, image_url=image_url,
                                    actif=actif, ordre=ordre)
        return RedirectResponse("/admin/projets", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("projet_form.html", {"request": request, "error": str(e)})


@router.get("/projets/{id}/modifier", response_class=HTMLResponse)
def edit_projet(id: int, request: Request, user: UserModel = Depends(admin_required),
                projet_service: ProjetService = Depends(get_projet_service)):
    projet = projet_service.recuperer_projet(id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return templates.TemplateResponse("projet_form.html", {"request": request, "projet": projet})


@router.post("/projets/{id}/modifier")
def save_projet(id: int, request: Request, titre: str = Form(...), description_courte: str = Form(...),
                description_longue: str = Form(...), slug: Optional[str] = Form(None),
                histoire: str = Form(""), image: Optional[UploadFile] = File(None),
                actif: bool = Form(True), ordre: int = Form(0),
                user: UserModel = Depends(admin_required),
                projet_service: ProjetService = Depends(get_projet_service)):
    projet = projet_service.recuperer_projet(id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet introuvable")

    image_url = projet.image_url  # Garder l'ancienne si pas de nouvelle
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1]
        unique = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        image_url = f"/static/uploads/{unique}"

    try:
        projet_service.modifier_projet(id=id, titre=titre, description_courte=description_courte,
                                       description_longue=description_longue, slug=slug,
                                       histoire=histoire, image_url=image_url,
                                       actif=actif, ordre=ordre)
        return RedirectResponse("/admin/projets", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("projet_form.html", {"request": request, "error": str(e)})
    
@router.get("/projets/{id}/supprimer")
def delete_projet(id: int, user: UserModel = Depends(admin_required),
                  projet_service: ProjetService = Depends(get_projet_service)):
    projet_service.supprimer_projet(id)
    return RedirectResponse("/admin/projets", status_code=302)

@router.get("/projets/{id}/toggle")
def toggle_projet(id: int, user: UserModel = Depends(admin_required),
                  projet_service: ProjetService = Depends(get_projet_service)):
    projet_service.basculer_actif_projet(id)
    return RedirectResponse("/admin/projets", status_code=302)

# ------------------------------------------------------------------
# SERVICES (CRUD)
# ------------------------------------------------------------------
@router.get("/services", response_class=HTMLResponse)
def list_services(request: Request, user: UserModel = Depends(admin_required),
                  service_service: ServiceService = Depends(get_service_service)):
    services = service_service.lister_services()
    return templates.TemplateResponse("services_list.html", {"request": request, "services": services})

@router.get("/services/ajouter", response_class=HTMLResponse)
def add_service_form(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("service_form.html", {"request": request, "service": None})

@router.post("/services/ajouter")
def add_service(request: Request, nom: str = Form(...), description: str = Form(...),
                prix: Optional[float] = Form(None), icone: Optional[str] = Form(None),
                actif: bool = Form(True), ordre: int = Form(0),
                user: UserModel = Depends(admin_required),
                service_service: ServiceService = Depends(get_service_service)):
    try:
        service_service.creer_service(nom=nom, description=description, prix=prix, icone=icone,
                                      actif=actif, ordre=ordre)
        return RedirectResponse("/admin/services", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("service_form.html", {"request": request, "error": str(e)})

@router.get("/services/{id}/modifier", response_class=HTMLResponse)
def edit_service(id: int, request: Request, user: UserModel = Depends(admin_required),
                 service_service: ServiceService = Depends(get_service_service)):
    service = service_service.recuperer_service(id)
    if not service:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("service_form.html", {"request": request, "service": service})

@router.post("/services/{id}/modifier")
def save_service(id: int, request: Request, nom: str = Form(...), description: str = Form(...),
                 prix: Optional[float] = Form(None), icone: Optional[str] = Form(None),
                 actif: bool = Form(True), ordre: int = Form(0),
                 user: UserModel = Depends(admin_required),
                 service_service: ServiceService = Depends(get_service_service)):
    try:
        service_service.modifier_service(id=id, nom=nom, description=description, prix=prix,
                                         icone=icone, actif=actif, ordre=ordre)
        return RedirectResponse("/admin/services", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("service_form.html", {"request": request, "error": str(e)})

@router.get("/services/{id}/supprimer")
def delete_service(id: int, user: UserModel = Depends(admin_required),
                   service_service: ServiceService = Depends(get_service_service)):
    service_service.supprimer_service(id)
    return RedirectResponse("/admin/services", status_code=302)

@router.get("/services/{id}/toggle")
def toggle_service(id: int, user: UserModel = Depends(admin_required),
                   service_service: ServiceService = Depends(get_service_service)):
    service_service.basculer_actif_service(id)
    return RedirectResponse("/admin/services", status_code=302)

# ------------------------------------------------------------------
# LIENS DE CONTACT (CRUD)
# ------------------------------------------------------------------
@router.get("/liens", response_class=HTMLResponse)
def list_liens(request: Request, user: UserModel = Depends(admin_required),
               lien_service: LienContactService = Depends(get_lien_service)):
    liens = lien_service.lister_liens()
    return templates.TemplateResponse("liens_list.html", {"request": request, "liens": liens})

@router.get("/liens/ajouter", response_class=HTMLResponse)
def add_lien_form(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("lien_form.html", {"request": request, "lien": None})

@router.post("/liens/ajouter")
def add_lien(request: Request, nom: str = Form(...), url: str = Form(...),
             icone: str = Form(...), actif: bool = Form(True), ordre: int = Form(0),
             user: UserModel = Depends(admin_required),
             lien_service: LienContactService = Depends(get_lien_service)):
    try:
        lien_service.creer_lien(nom=nom, url=url, icone=icone, actif=actif, ordre=ordre)
        return RedirectResponse("/admin/liens", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("lien_form.html", {"request": request, "error": str(e)})

@router.get("/liens/{id}/modifier", response_class=HTMLResponse)
def edit_lien(id: int, request: Request, user: UserModel = Depends(admin_required),
              lien_service: LienContactService = Depends(get_lien_service)):
    lien = lien_service.recuperer_lien(id)
    if not lien:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("lien_form.html", {"request": request, "lien": lien})

@router.post("/liens/{id}/modifier")
def save_lien(id: int, request: Request, nom: str = Form(...), url: str = Form(...),
              icone: str = Form(...), actif: bool = Form(True), ordre: int = Form(0),
              user: UserModel = Depends(admin_required),
              lien_service: LienContactService = Depends(get_lien_service)):
    try:
        lien_service.modifier_lien(id=id, nom=nom, url=url, icone=icone, actif=actif, ordre=ordre)
        return RedirectResponse("/admin/liens", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("lien_form.html", {"request": request, "error": str(e)})

@router.get("/liens/{id}/supprimer")
def delete_lien(id: int, user: UserModel = Depends(admin_required),
                lien_service: LienContactService = Depends(get_lien_service)):
    lien_service.supprimer_lien(id)
    return RedirectResponse("/admin/liens", status_code=302)

@router.get("/liens/{id}/toggle")
def toggle_lien(id: int, user: UserModel = Depends(admin_required),
                lien_service: LienContactService = Depends(get_lien_service)):
    lien_service.basculer_actif_lien(id)
    return RedirectResponse("/admin/liens", status_code=302)

# ------------------------------------------------------------------
# TÉMOIGNAGES (CRUD)
# ------------------------------------------------------------------
@router.get("/temoignages", response_class=HTMLResponse)
def list_temoignages(request: Request, user: UserModel = Depends(admin_required),
                     temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    temoignages = temoignage_service.lister_temoignages()
    return templates.TemplateResponse("temoignages_list.html", {"request": request, "temoignages": temoignages})

@router.get("/temoignages/ajouter", response_class=HTMLResponse)
def add_temoignage_form(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("temoignage_form.html", {"request": request, "temoignage": None})

@router.post("/temoignages/ajouter")
def add_temoignage(request: Request, nom: str = Form(...), texte: str = Form(...),
                   photo_url: Optional[str] = Form(None), entreprise: Optional[str] = Form(None),
                   actif: bool = Form(True), ordre: int = Form(0),
                   user: UserModel = Depends(admin_required),
                   temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    try:
        temoignage_service.creer_temoignage(nom=nom, texte=texte, photo_url=photo_url,
                                            entreprise=entreprise, actif=actif, ordre=ordre)
        return RedirectResponse("/admin/temoignages", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("temoignage_form.html", {"request": request, "error": str(e)})

@router.get("/temoignages/{id}/modifier", response_class=HTMLResponse)
def edit_temoignage(id: int, request: Request, user: UserModel = Depends(admin_required),
                    temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    temoignage = temoignage_service.recuperer_temoignage(id)
    if not temoignage:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("temoignage_form.html", {"request": request, "temoignage": temoignage})

@router.post("/temoignages/{id}/modifier")
def save_temoignage(id: int, request: Request, nom: str = Form(...), texte: str = Form(...),
                    photo_url: Optional[str] = Form(None), entreprise: Optional[str] = Form(None),
                    actif: bool = Form(True), ordre: int = Form(0),
                    user: UserModel = Depends(admin_required),
                    temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    try:
        temoignage_service.modifier_temoignage(id=id, nom=nom, texte=texte, photo_url=photo_url,
                                               entreprise=entreprise, actif=actif, ordre=ordre)
        return RedirectResponse("/admin/temoignages", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("temoignage_form.html", {"request": request, "error": str(e)})

@router.get("/temoignages/{id}/supprimer")
def delete_temoignage(id: int, user: UserModel = Depends(admin_required),
                      temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    temoignage_service.supprimer_temoignage(id)
    return RedirectResponse("/admin/temoignages", status_code=302)

@router.get("/temoignages/{id}/toggle")
def toggle_temoignage(id: int, user: UserModel = Depends(admin_required),
                      temoignage_service: TemoignageService = Depends(get_temoignage_service)):
    temoignage_service.basculer_actif_temoignage(id)
    return RedirectResponse("/admin/temoignages", status_code=302)

# ------------------------------------------------------------------
# À PROPOS
# ------------------------------------------------------------------
@router.get("/about", response_class=HTMLResponse)
def edit_about(request: Request, user: UserModel = Depends(admin_required),
               about_service: AboutService = Depends(get_about_service)):
    about = about_service.recuperer_contenu()
    return templates.TemplateResponse("about_edit.html", {"request": request, "about": about})

@router.post("/about")
def save_about(request: Request, contenu: str = Form(...),
               user: UserModel = Depends(admin_required),
               about_service: AboutService = Depends(get_about_service)):
    try:
        about_service.mettre_a_jour_contenu(contenu)
        return RedirectResponse("/admin/about?success=1", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse("about_edit.html", {"request": request, "error": str(e)})

# ------------------------------------------------------------------
# CONTACTS (mini CRM)
# ------------------------------------------------------------------
@router.get("/contacts", response_class=HTMLResponse)
def list_contacts(request: Request, user: UserModel = Depends(admin_required),
                  contact_service: ContactService = Depends(get_contact_service)):
    contacts = contact_service.lister_messages()
    return templates.TemplateResponse("contacts_list.html", {"request": request, "contacts": contacts})

@router.get("/contacts/{id}", response_class=HTMLResponse)
def detail_contact(id: int, request: Request, user: UserModel = Depends(admin_required),
                   contact_service: ContactService = Depends(get_contact_service)):
    contact = contact_service.recuperer_message(id)
    if not contact:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("contact_detail.html", {"request": request, "contact": contact})

@router.post("/contacts/{id}/statut")
def update_contact_statut(id: int, statut: str = Form(...),
                          user: UserModel = Depends(admin_required),
                          contact_service: ContactService = Depends(get_contact_service)):
    contact_service.changer_statut(id, statut)
    return RedirectResponse(f"/admin/contacts/{id}", status_code=302)

@router.post("/contacts/{id}/note")
def update_contact_note(id: int, note_admin: str = Form(...),
                        user: UserModel = Depends(admin_required),
                        contact_service: ContactService = Depends(get_contact_service)):
    contact_service.ajouter_note_admin(id, note_admin)
    return RedirectResponse(f"/admin/contacts/{id}", status_code=302)

# ------------------------------------------------------------------
# VISITES
# ------------------------------------------------------------------
@router.get("/visites", response_class=HTMLResponse)
def visites_page(request: Request, user: UserModel = Depends(admin_required),
                 visite_service: VisiteService = Depends(get_visite_service)):
    visites = visite_service.lister_dernieres_visites(limite=50)
    stats = visite_service.obtenir_statistiques()
    return templates.TemplateResponse("visites.html", {"request": request, "visites": visites, "stats": stats})

# ------------------------------------------------------------------
# HEATMAP  ← AJOUTEZ CE BLOC ICI
# ------------------------------------------------------------------
@router.get("/heatmap", response_class=HTMLResponse)
def heatmap_page(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("heatmap.html", {"request": request})

# ------------------------------------------------------------------
# SANTÉ
# ------------------------------------------------------------------
@router.get("/sante", response_class=HTMLResponse)
def sante_page(request: Request, user: UserModel = Depends(admin_required)):
    """Affiche la page de santé du site."""
    return templates.TemplateResponse("sante.html", {"request": request})

# ------------------------------------------------------------------
# SNAPSHOTS
# ------------------------------------------------------------------
@router.get("/snapshots", response_class=HTMLResponse)
def list_snapshots(request: Request, user: UserModel = Depends(admin_required),
                   snapshot_service: SnapshotService = Depends(get_snapshot_service)):
    snapshots = snapshot_service.lister_snapshots()
    return templates.TemplateResponse("snapshots_list.html", {"request": request, "snapshots": snapshots})

@router.post("/snapshots/create")
def create_snapshot(request: Request, nom: str = Form(...),
                    user: UserModel = Depends(admin_required),
                    snapshot_service: SnapshotService = Depends(get_snapshot_service)):
    snapshot_service.creer_snapshot(nom)
    return RedirectResponse("/admin/snapshots", status_code=302)

@router.get("/snapshots/{id}/restore")
def restore_snapshot(id: int, user: UserModel = Depends(admin_required),
                     snapshot_service: SnapshotService = Depends(get_snapshot_service)):
    success = snapshot_service.restaurer_snapshot(id)
    return RedirectResponse("/admin/snapshots", status_code=302)

@router.get("/snapshots/{id}/delete")
def delete_snapshot(id: int, user: UserModel = Depends(admin_required),
                    snapshot_service: SnapshotService = Depends(get_snapshot_service)):
    snapshot_service.supprimer_snapshot(id)
    return RedirectResponse("/admin/snapshots", status_code=302)

# ------------------------------------------------------------------
# MAINTENANCE
# ------------------------------------------------------------------
@router.get("/maintenance", response_class=HTMLResponse)
def maintenance_page(request: Request, user: UserModel = Depends(admin_required),
                     maintenance_service: MaintenanceServiceImpl = Depends(get_maintenance_service)):
    actif = maintenance_service.est_actif()
    return templates.TemplateResponse("maintenance_admin.html", {"request": request, "maintenance_actif": actif})

@router.post("/maintenance")
def toggle_maintenance(request: Request, user: UserModel = Depends(admin_required),
                       maintenance_service: MaintenanceServiceImpl = Depends(get_maintenance_service)):
    if maintenance_service.est_actif():
        maintenance_service.desactiver()
    else:
        maintenance_service.activer()
    return RedirectResponse("/admin/maintenance", status_code=302)

# ------------------------------------------------------------------
# MÉDIAS (gallery simple)
# ------------------------------------------------------------------
@router.get("/media", response_class=HTMLResponse)
def media_page(request: Request, user: UserModel = Depends(admin_required)):
    # Lister les fichiers dans static/uploads
    files = os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else []
    files = [f for f in files if f.lower().endswith(('.png','.jpg','.jpeg','.gif','.webp'))]
    return templates.TemplateResponse("media.html", {"request": request, "files": files})

@router.post("/media/upload")
def upload_media(request: Request, file: UploadFile = File(...),
                 user: UserModel = Depends(admin_required)):
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return RedirectResponse("/admin/media", status_code=302)

from infrastructure.repositories.article_repo_impl import ArticleRepositoryImpl
from application.use_cases.article_service import ArticleService  # à créer (simple CRUD)

def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(ArticleRepositoryImpl(db))

# Liste
@router.get("/blog", response_class=HTMLResponse)
def admin_blog_list(request: Request, user: UserModel = Depends(admin_required),
                    article_service: ArticleService = Depends(get_article_service)):
    articles = article_service.lister_articles()
    return templates.TemplateResponse("blog_admin_list.html", {"request": request, "articles": articles})

# Ajouter
@router.get("/blog/ajouter", response_class=HTMLResponse)
def admin_blog_add_form(request: Request, user: UserModel = Depends(admin_required)):
    return templates.TemplateResponse("blog_admin_form.html", {"request": request, "article": None})

@router.post("/blog/ajouter")
def admin_blog_add(request: Request, titre: str = Form(...), contenu: str = Form(...),
                   image: Optional[UploadFile] = File(None),
                   user: UserModel = Depends(admin_required),
                   article_service: ArticleService = Depends(get_article_service)):
    image_url = None
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1]
        unique = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique)
        with open(file_path, "wb") as f: f.write(image.file.read())
        image_url = f"/static/uploads/{unique}"
    article_service.creer_article(titre=titre, contenu=contenu, image_url=image_url)
    return RedirectResponse("/admin/blog", status_code=302)

# Modifier
@router.get("/blog/{id}/modifier", response_class=HTMLResponse)
def admin_blog_edit_form(id: int, request: Request, user: UserModel = Depends(admin_required),
                         article_service: ArticleService = Depends(get_article_service)):
    article = article_service.recuperer_article(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return templates.TemplateResponse("blog_admin_form.html", {"request": request, "article": article})


@router.post("/blog/{id}/modifier")
def admin_blog_edit(id: int, request: Request, titre: str = Form(...), contenu: str = Form(...),
                    image: Optional[UploadFile] = File(None),
                    user: UserModel = Depends(admin_required),
                    article_service: ArticleService = Depends(get_article_service)):
    article = article_service.recuperer_article(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")

    image_url = article.image_url  # garder l'ancienne par défaut
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1]
        unique = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        image_url = f"/static/uploads/{unique}"

    article_service.modifier_article(
        id=id,
        titre=titre,
        contenu=contenu,
        image_url=image_url
    )
    return RedirectResponse("/admin/blog", status_code=302)


# Supprimer
@router.get("/blog/{id}/supprimer")
def admin_blog_delete(id: int, user: UserModel = Depends(admin_required),
                      article_service: ArticleService = Depends(get_article_service)):
    article_service.supprimer_article(id)
    return RedirectResponse("/admin/blog", status_code=302)


# Toggle actif/inactif
@router.get("/blog/{id}/toggle")
def admin_blog_toggle(id: int, user: UserModel = Depends(admin_required),
                      article_service: ArticleService = Depends(get_article_service)):
    article_service.basculer_actif(id)
    return RedirectResponse("/admin/blog", status_code=302)