"""
Application Principale – Bridge Afrika Portfolio
=================================================
Point d'entrée FastAPI qui assemble toutes les couches
et démarre le serveur.

Architecture :
- La base de données est initialisée au démarrage.
- L'administrateur par défaut est créé automatiquement.
- Les middlewares gèrent CORS, mode maintenance et tracking.
- Les routers sont montés (public, admin, API).
"""

import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from infrastructure.database.session import engine, init_db, SessionLocal
from infrastructure.database.models import Base, UserModel
from infrastructure.services.maintenance_service_impl import MaintenanceServiceImpl
from infrastructure.auth.password_service import PasswordService
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware Maintenance ---
@app.middleware("http")
async def maintenance_middleware(request: Request, call_next):
    if request.url.path == "/maintenance":
        return await call_next(request)
    if request.url.path.startswith("/static"):
        return await call_next(request)
    if request.url.path.startswith("/admin"):
        return await call_next(request)
    if request.url.path.startswith("/api"):
        return await call_next(request)
    if request.url.path == "/health":
        return await call_next(request)
    if request.url.path == "/sitemap.xml":
        return await call_next(request)
    if request.url.path == "/robots.txt":
        return await call_next(request)
    if request.url.path.startswith("/google"):
        return await call_next(request)

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
    Initialise la base de données et crée l'administrateur par défaut.
    """
    # 1. Créer toutes les tables
    init_db()
    print("✅ Base de données initialisée.")

    # 2. Créer l'admin par défaut si aucun utilisateur n'existe
    db = SessionLocal()
    try:
        # Vérifier s'il y a déjà un utilisateur
        admin_exists = db.query(UserModel).first()
        if not admin_exists:
            admin_username = os.getenv("ADMIN_USERNAME", "vainqueur")
            admin_password = os.getenv("ADMIN_PASSWORD", "00Kalema")
            admin = UserModel(
                username=admin_username,
                password_hash=PasswordService.hacher(admin_password)
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin créé : {admin_username}")
        else:
            print("ℹ️  Un administrateur existe déjà.")
    except Exception as e:
        print(f"⚠️  Erreur lors de la création de l'admin : {e}")
    finally:
        db.close()

# --- Inclusion des routers ---
app.include_router(public_router, tags=["Public"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(admin_api_router, prefix="/api/admin", tags=["API Admin"])
app.include_router(tracking_api_router, prefix="/api/tracking", tags=["Tracking"])

# --- Route robots.txt ---
@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return """User-agent: *
Allow: /
Disallow: /admin
Disallow: /api

Sitemap: https://kalema-vainqueur.onrender.com/sitemap.xml"""

# --- Route vérification Google ---
@app.get("/google94b89e364e3eabb4.html", response_class=HTMLResponse)
def google_verify():
    return "google-site-verification: google94b89e364e3eabb4.html"

# --- Route health check ---
@app.get("/health")
def health_check():
    """Endpoint de vérification de l'état du serveur."""
    return {"status": "ok", "app": "Bridge Afrika Portfolio"}

# --- Route sitemap dynamique ---
@app.get("/sitemap.xml")
def sitemap():
    """Génère un sitemap dynamique avec les projets et articles."""
    from infrastructure.repositories.projet_repo_impl import ProjetRepositoryImpl
    from infrastructure.repositories.article_repo_impl import ArticleRepositoryImpl
    from application.use_cases.projet_service import ProjetService
    from application.use_cases.article_service import ArticleService

    db = SessionLocal()
    try:
        projet_service = ProjetService(ProjetRepositoryImpl(db))
        article_service = ArticleService(ArticleRepositoryImpl(db))
        projets = projet_service.lister_projets(actif_seulement=True)
        articles = article_service.lister_articles(actif_seulement=True)
    finally:
        db.close()

    projets_xml = ""
    for projet in projets:
        projets_xml += f"""
    <url>
        <loc>https://kalema-vainqueur.onrender.com/projet/{projet.slug}</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>"""

    articles_xml = ""
    for article in articles:
        articles_xml += f"""
    <url>
        <loc>https://kalema-vainqueur.onrender.com/blog/{article.slug}</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>"""

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://kalema-vainqueur.onrender.com/</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://kalema-vainqueur.onrender.com/services</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://kalema-vainqueur.onrender.com/a-propos</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://kalema-vainqueur.onrender.com/contact</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://kalema-vainqueur.onrender.com/blog</loc>
        <lastmod>2026-06-17</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    {projets_xml}
    {articles_xml}
</urlset>"""

    return Response(content=xml_content, media_type="application/xml")


# --- Démarrage direct ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)