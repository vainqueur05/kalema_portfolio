"""
Use Case : ArticleService
==========================
Orchestre la logique métier pour les articles de blog.
"""

from typing import List, Optional
from domain.entities.article import Article
from application.interfaces.repositories.article_repo import ArticleRepository


class ArticleService:
    def __init__(self, repo: ArticleRepository):
        self.repo = repo

    def lister_articles(self, actif_seulement: bool = False) -> List[Article]:
        return self.repo.recuperer_tous(actif_seulement=actif_seulement)

    def recuperer_article(self, id: int) -> Optional[Article]:
        return self.repo.recuperer_par_id(id)

    def recuperer_par_slug(self, slug: str) -> Optional[Article]:
        return self.repo.recuperer_par_slug(slug)

    def creer_article(self, titre: str, contenu: str, slug: Optional[str] = None, image_url: Optional[str] = None) -> Article:
        article = Article(titre=titre, contenu=contenu, slug=slug, image_url=image_url)
        return self.repo.ajouter(article)

    def modifier_article(self, id: int, **kwargs) -> Optional[Article]:
        article = self.repo.recuperer_par_id(id)
        if not article:
            return None
        article_modifie = article.mettre_a_jour(**kwargs)
        return self.repo.mettre_a_jour(article_modifie)

    def supprimer_article(self, id: int) -> bool:
        article = self.repo.recuperer_par_id(id)
        if not article:
            return False
        self.repo.supprimer(id)
        return True

    def basculer_actif(self, id: int) -> Optional[Article]:
        return self.repo.basculer_actif(id)