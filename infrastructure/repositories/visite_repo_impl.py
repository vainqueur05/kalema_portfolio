"""
Implémentation du Repository Visite
====================================
Adaptateur concret entre le domaine et la persistance SQLAlchemy.
Implémente l'interface VisiteRepository.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from domain.entities.visite import Visite
from application.interfaces.repositories.visite_repo import VisiteRepository
from infrastructure.database.models import VisiteModel


class VisiteRepositoryImpl(VisiteRepository):
    """
    Implémentation SQLAlchemy pour l'enregistrement et la consultation des visites.

    Attributes:
        db (Session): Session de base de données injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def enregistrer(self, visite: Visite) -> Visite:
        """
        Persiste une nouvelle visite en base.

        Args:
            visite: L'entité Visite à enregistrer.

        Returns:
            Visite: L'entité persistée avec un id généré.
        """
        visite_db = VisiteModel(
            page=visite.page,
            ip=visite.ip,
            user_agent=visite.user_agent,
            referrer=visite.referrer,
            pays=visite.pays,
            ville=visite.ville,
            navigateur=visite.navigateur,
            os=visite.os,
            appareil=visite.appareil,
        )
        self.db.add(visite_db)
        self.db.commit()
        self.db.refresh(visite_db)
        return self._to_entity(visite_db)

    def recuperer_toutes(self, limite: int = 100) -> List[Visite]:
        """
        Retourne les dernières visites enregistrées.

        Args:
            limite: Nombre maximum d'enregistrements à retourner.

        Returns:
            Liste des visites (de la plus récente à la plus ancienne).
        """
        visites_db = (
            self.db.query(VisiteModel)
            .order_by(VisiteModel.date.desc())
            .limit(limite)
            .all()
        )
        return [self._to_entity(v) for v in visites_db]

    def statistiques(self) -> Dict[str, Any]:
        """
        Calcule des statistiques agrégées pour le dashboard admin.

        Returns:
            Un dictionnaire contenant :
            - total_visites: nombre total de visites
            - par_pays: liste de dicts {pays, nombre}
            - par_page: liste de dicts {page, nombre}
            - par_appareil: liste de dicts {appareil, nombre}
        """
        total = self.db.query(func.count(VisiteModel.id)).scalar()

        # Par pays (top 10)
        par_pays = (
            self.db.query(
                VisiteModel.pays,
                func.count(VisiteModel.id).label("nombre")
            )
            .filter(VisiteModel.pays.isnot(None))
            .group_by(VisiteModel.pays)
            .order_by(func.count(VisiteModel.id).desc())
            .limit(10)
            .all()
        )

        # Par page
        par_page = (
            self.db.query(
                VisiteModel.page,
                func.count(VisiteModel.id).label("nombre")
            )
            .group_by(VisiteModel.page)
            .order_by(func.count(VisiteModel.id).desc())
            .all()
        )

        # Par appareil
        par_appareil = (
            self.db.query(
                VisiteModel.appareil,
                func.count(VisiteModel.id).label("nombre")
            )
            .filter(VisiteModel.appareil.isnot(None))
            .group_by(VisiteModel.appareil)
            .order_by(func.count(VisiteModel.id).desc())
            .all()
        )

        return {
            "total_visites": total or 0,
            "par_pays": [{"pays": p, "nombre": n} for p, n in par_pays],
            "par_page": [{"page": p, "nombre": n} for p, n in par_page],
            "par_appareil": [{"appareil": a, "nombre": n} for a, n in par_appareil],
        }

    def _to_entity(self, model: VisiteModel) -> Visite:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        return Visite(
            id=model.id,
            page=model.page,
            ip=model.ip,
            user_agent=model.user_agent,
            referrer=model.referrer,
            pays=model.pays,
            ville=model.ville,
            navigateur=model.navigateur,
            os=model.os,
            appareil=model.appareil,
        )