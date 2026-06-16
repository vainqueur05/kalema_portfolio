"""
Implémentation du Repository Service
=====================================
Adaptateur concret entre le domaine métier et la persistance.
Implémente l'interface ServiceRepository avec SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.service import Service
from application.interfaces.repositories.service_repo import ServiceRepository
from infrastructure.database.models import ServiceModel


class ServiceRepositoryImpl(ServiceRepository):
    """
    Implémentation SQLAlchemy pour la gestion des services.

    Attributes:
        db (Session): Session de base de données injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self, actif_seulement: bool = False) -> List[Service]:
        """Retourne tous les services, triés par ordre."""
        query = self.db.query(ServiceModel)
        if actif_seulement:
            query = query.filter(ServiceModel.actif == True)
        services_db = query.order_by(ServiceModel.ordre.asc()).all()
        return [self._to_entity(s) for s in services_db]

    def recuperer_par_id(self, id: int) -> Optional[Service]:
        """Récupère un service par son ID."""
        service_db = self.db.query(ServiceModel).filter(ServiceModel.id == id).first()
        if not service_db:
            return None
        return self._to_entity(service_db)

    def ajouter(self, service: Service) -> Service:
        """Ajoute un nouveau service."""
        service_db = ServiceModel(
            nom=service.nom,
            description=service.description,
            prix=service.prix,
            icone=service.icone,
            actif=service.actif,
            ordre=service.ordre,
        )
        self.db.add(service_db)
        self.db.commit()
        self.db.refresh(service_db)
        return self._to_entity(service_db)

    def mettre_a_jour(self, service: Service) -> Service:
        """Met à jour un service existant."""
        service_db = self.db.query(ServiceModel).filter(ServiceModel.id == service.id).first()
        if not service_db:
            raise ValueError(f"Service avec id {service.id} introuvable.")
        service_db.nom = service.nom
        service_db.description = service.description
        service_db.prix = service.prix
        service_db.icone = service.icone
        service_db.actif = service.actif
        service_db.ordre = service.ordre
        self.db.commit()
        self.db.refresh(service_db)
        return self._to_entity(service_db)

    def supprimer(self, id: int) -> None:
        """Supprime un service par son ID."""
        service_db = self.db.query(ServiceModel).filter(ServiceModel.id == id).first()
        if service_db:
            self.db.delete(service_db)
            self.db.commit()

    def basculer_actif(self, id: int) -> Optional[Service]:
        """Inverse l'état actif/inactif."""
        service_db = self.db.query(ServiceModel).filter(ServiceModel.id == id).first()
        if not service_db:
            return None
        service_db.actif = not service_db.actif
        self.db.commit()
        self.db.refresh(service_db)
        return self._to_entity(service_db)

    def _to_entity(self, model: ServiceModel) -> Service:
        """Mappe le modèle SQLAlchemy vers l'entité domaine."""
        return Service(
            id=model.id,
            nom=model.nom,
            description=model.description,
            prix=model.prix,
            icone=model.icone,
            actif=model.actif,
            ordre=model.ordre,
        )