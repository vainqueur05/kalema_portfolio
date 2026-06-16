"""
API Tracking – Bridge Afrika Portfolio
=======================================
Endpoints publics pour enregistrer les visites et les interactions
(heatmap, réactions, temps de lecture...).
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from infrastructure.database.session import get_db
from infrastructure.repositories.visite_repo_impl import VisiteRepositoryImpl
from infrastructure.services.geo_service_impl import GeoServiceImpl
from infrastructure.services.heatmap_service_impl import HeatmapServiceImpl
from application.use_cases.visite_service import VisiteService

router = APIRouter()

# ------------------------------------------------------------------
# Services
# ------------------------------------------------------------------
def get_visite_service(db: Session = Depends(get_db)) -> VisiteService:
    return VisiteService(VisiteRepositoryImpl(db), GeoServiceImpl())

def get_heatmap_service() -> HeatmapServiceImpl:
    # Pas de persistance pour l'instant, service en mémoire
    return HeatmapServiceImpl()

# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@router.post("/visit")
async def track_visit(
    request: Request,
    page: str = "/",
    referrer: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Enregistre une visite sur une page publique.
    Appelé par le middleware ou par un script JS côté client.
    """
    visite_service = VisiteService(VisiteRepositoryImpl(db), GeoServiceImpl())
    ip = request.client.host if request.client else "inconnue"
    user_agent = request.headers.get("user-agent")
    try:
        visite_service.enregistrer_visite(
            page=page,
            ip=ip,
            user_agent=user_agent,
            referrer=referrer
        )
        return {"status": "ok"}
    except Exception as e:
        # Ne pas bloquer la navigation si l'enregistrement échoue
        return {"status": "error", "detail": str(e)}

@router.post("/heatmap")
async def track_heatmap(
    request: Request,
    heatmap_service: HeatmapServiceImpl = Depends(get_heatmap_service)
):
    """
    Enregistre un événement de heatmap (clic, scroll).
    """
    data = await request.json()
    heatmap_service.enregistrer_evenement(data)
    return {"status": "ok"}

@router.get("/heatmap/data")
async def get_heatmap_data(
    page: Optional[str] = None,
    heatmap_service: HeatmapServiceImpl = Depends(get_heatmap_service)
):
    """
    Retourne les données de heatmap pour l'admin.
    """
    return {"data": heatmap_service.recuperer_donnees(page=page)}