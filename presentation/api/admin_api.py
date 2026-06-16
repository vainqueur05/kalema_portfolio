"""
API Admin – Bridge Afrika Portfolio
=====================================
Endpoints REST réservés au tableau de bord admin.
Fournit des données brutes (JSON) pour les widgets dynamiques.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from infrastructure.database.session import get_db
from infrastructure.repositories.visite_repo_impl import VisiteRepositoryImpl
from infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
from infrastructure.services.geo_service_impl import GeoServiceImpl
from infrastructure.services.maintenance_service_impl import MaintenanceServiceImpl
from infrastructure.auth.auth_handler import AuthHandler
from infrastructure.database.models import UserModel

from application.use_cases.visite_service import VisiteService
from application.use_cases.contact_service import ContactService

router = APIRouter()

# ------------------------------------------------------------------
# Services
# ------------------------------------------------------------------
def get_visite_service(db: Session = Depends(get_db)) -> VisiteService:
    return VisiteService(VisiteRepositoryImpl(db), GeoServiceImpl())

def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(ContactRepositoryImpl(db))

def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceServiceImpl:
    return MaintenanceServiceImpl(db)

# ------------------------------------------------------------------
# Authentification admin
# ------------------------------------------------------------------
def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[UserModel]:
    token = request.cookies.get("admin_token")
    if not token:
        raise HTTPException(status_code=401, detail="Non authentifié")
    payload = AuthHandler.verifier_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide")
    return db.query(UserModel).filter(UserModel.id == int(payload.get("sub"))).first()

# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@router.get("/stats/live")
def get_live_stats(
    request: Request,
    user: UserModel = Depends(get_current_user),
    visite_service: VisiteService = Depends(get_visite_service),
    contact_service: ContactService = Depends(get_contact_service),
    maintenance_service: MaintenanceServiceImpl = Depends(get_maintenance_service)
):
    """
    Retourne les statistiques en temps réel pour le dashboard.
    """
    stats = visite_service.obtenir_statistiques()
    nouveaux_contacts = len(contact_service.lister_messages(statut="Nouveau"))
    maintenance_actif = maintenance_service.est_actif()

    return {
        "total_visites": stats["total_visites"],
        "par_pays": stats["par_pays"],
        "par_page": stats["par_page"],
        "par_appareil": stats["par_appareil"],
        "nouveaux_contacts": nouveaux_contacts,
        "maintenance": maintenance_actif
    }

@router.get("/contacts/latest")
def get_latest_contacts(
    limit: int = 5,
    request: Request = None,
    user: UserModel = Depends(get_current_user),
    contact_service: ContactService = Depends(get_contact_service)
):
    """
    Retourne les derniers messages reçus.
    """
    contacts = contact_service.lister_messages()
    latest = contacts[:limit]
    return [c.to_dict() for c in latest]