from sqlalchemy.orm import Session
from domain.entities.article import Article
from application.interfaces.repositories.article_repo import ArticleRepository
from infrastructure.database.models import ArticleModel

class ArticleRepositoryImpl(ArticleRepository):
    def __init__(self, db: Session): self.db = db

    def recuperer_tous(self, actif_seulement=False):
        q = self.db.query(ArticleModel)
        if actif_seulement: q = q.filter(ArticleModel.actif == True)
        return [self._to_entity(a) for a in q.order_by(ArticleModel.created_at.desc()).all()]

    def recuperer_par_id(self, id):
        a = self.db.query(ArticleModel).filter(ArticleModel.id == id).first()
        return self._to_entity(a) if a else None

    def recuperer_par_slug(self, slug):
        a = self.db.query(ArticleModel).filter(ArticleModel.slug == slug).first()
        return self._to_entity(a) if a else None

    def ajouter(self, article):
        m = ArticleModel(titre=article.titre, slug=article.slug, contenu=article.contenu, image_url=article.image_url, actif=article.actif)
        self.db.add(m); self.db.commit(); self.db.refresh(m)
        return self._to_entity(m)

    def mettre_a_jour(self, article):
        m = self.db.query(ArticleModel).filter(ArticleModel.id == article.id).first()
        if not m: raise ValueError("Article introuvable")
        m.titre=article.titre; m.slug=article.slug; m.contenu=article.contenu; m.image_url=article.image_url; m.actif=article.actif
        self.db.commit(); self.db.refresh(m)
        return self._to_entity(m)

    def supprimer(self, id):
        m = self.db.query(ArticleModel).filter(ArticleModel.id == id).first()
        if m: self.db.delete(m); self.db.commit()

    def basculer_actif(self, id):
        m = self.db.query(ArticleModel).filter(ArticleModel.id == id).first()
        if not m: return None
        m.actif = not m.actif; self.db.commit(); self.db.refresh(m)
        return self._to_entity(m)

    def _to_entity(self, m): return Article(titre=m.titre, slug=m.slug, contenu=m.contenu, image_url=m.image_url, actif=m.actif, id=m.id)