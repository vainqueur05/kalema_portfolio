"""
Implémentation du Repository Snapshot
======================================
Adaptateur concret entre le domaine et la persistance.
Implémente l'interface SnapshotRepository avec SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.snapshot import Snapshot
from application.interfaces.repositories.snapshot_repo import SnapshotRepository
from infrastructure.database.models import SnapshotModel


class SnapshotRepositoryImpl(SnapshotRepository):
    """
    Implémentation SQLAlchemy pour la gestion des snapshots.

    Attributes:
        db (Session): Session SQLAlchemy injectée.
    """

    def __init__(self, db: Session):
        self.db = db

    def recuperer_tous(self) -> List[Snapshot]:
        """Retourne tous les snapshots, du plus récent au plus ancien."""
        snapshots_db = (
            self.db.query(SnapshotModel)
            .order_by(SnapshotModel.created_at.desc())
            .all()
        )
        return [self._to_entity(s) for s in snapshots_db]

    def recuperer_par_id(self, id: int) -> Optional[Snapshot]:
        """Récupère un snapshot par son ID."""
        snapshot_db = self.db.query(SnapshotModel).filter(SnapshotModel.id == id).first()
        if not snapshot_db:
            return None
        return self._to_entity(snapshot_db)

    def sauvegarder(self, snapshot: Snapshot) -> Snapshot:
        """Crée un nouveau snapshot (pas de mise à jour)."""
        snapshot_db = SnapshotModel(
            nom=snapshot.nom,
            donnees_json=snapshot.donnees_json,
        )
        self.db.add(snapshot_db)
        self.db.commit()
        self.db.refresh(snapshot_db)
        return self._to_entity(snapshot_db)

    def supprimer(self, id: int) -> None:
        """Supprime un snapshot par son ID."""
        snapshot_db = self.db.query(SnapshotModel).filter(SnapshotModel.id == id).first()
        if snapshot_db:
            self.db.delete(snapshot_db)
            self.db.commit()

    def _to_entity(self, model: SnapshotModel) -> Snapshot:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        return Snapshot(
            id=model.id,
            nom=model.nom,
            donnees_json=model.donnees_json,
        )