"""
Application Principale – Bridge Afrika Portfolio
=================================================
Point d'entrée FastAPI qui assemble toutes les couches
et démarre le serveur.

Architecture :
- La base de données est initialisée au démarrage.
- Les middlewares gèrent CORS, mode maintenance et tracking.
- Les routers sont montés (public, admin, API).
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from infrastructure.database.session import engine, init_db, SessionLocal
from infrastructure.database.models import Base
from infrastructure.services.maintenance_service_impl import MaintenanceServiceImpl
from presentation.public.routes import router as public_router
from presentation.admin.routes import router as admin_router
from presentation.api.admin_api import router as admin_api_router
from presentation.api.tracking_api import router as tracking_api_router


# Création de l'application FastAPI
app = FastAPI(
    title="Bridge Afrika Portfolio",
    description="Portfolio personnel de Vainqueur Kalema – Développeur Fullstack Web",
    version="1.0.0",
)

# --- Fichiers statiques ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À modifier pour la production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware Maintenance (AJOUTÉ - sans toucher au reste) ---
@app.middleware("http")
async def maintenance_middleware(request: Request, call_next):
    # Ne pas bloquer la page maintenance elle-même
    if request.url.path == "/maintenance":
        return await call_next(request)
    # Ne pas bloquer les fichiers statiques
    if request.url.path.startswith("/static"):
        return await call_next(request)
    # Ne pas bloquer l'admin (pour pouvoir désactiver)
    if request.url.path.startswith("/admin"):
        return await call_next(request)
    # Ne pas bloquer les API
    if request.url.path.startswith("/api"):
        return await call_next(request)
    # Ne pas bloquer le health check
    if request.url.path == "/health":
        return await call_next(request)

    # Vérifier la maintenance
    db = SessionLocal()
    try:
        service = MaintenanceServiceImpl(db)
        if service.est_actif():
            return RedirectResponse("/maintenance", status_code=302)
    finally:
        db.close()

    return await call_next(request)

# --- Événements de démarrage ---
@app.on_event("startup")
def startup():
    """
    Initialise la base de données au démarrage.
    """
    init_db()
    print("✅ Base de données initialisée.")


# --- Inclusion des routers ---

# Routes publiques (vitrine)
app.include_router(public_router, tags=["Public"])

# Routes admin (protégées par authentification)
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# API admin (pour les appels asynchrones éventuels)
app.include_router(admin_api_router, prefix="/api/admin", tags=["API Admin"])

# API tracking (enregistrement des visites et heatmap)
app.include_router(tracking_api_router, prefix="/api/tracking", tags=["Tracking"])


from fastapi.responses import PlainTextResponse

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return """User-agent: *
Allow: /
Disallow: /admin
Disallow: /api

Sitemap: https://kalema-vainqueur.onrender.com/sitemap.xml"""

from fastapi.responses import FileResponse

@app.get("/sitemap.xml")
def sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml")

# --- Route racine (vérification rapide) ---

@app.get("/health")
def health_check():
    """Endpoint de vérification de l'état du serveur."""
    return {"status": "ok", "app": "Bridge Afrika Portfolio"}


# --- Démarrage direct ---

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)