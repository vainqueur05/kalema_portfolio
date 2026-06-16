"""
Implémentation du service de mode maintenance.
Utilise la table settings (clé 'maintenance_mode') pour persister l'état.
Respecte l'interface MaintenanceService.
"""

from sqlalchemy.orm import Session
from application.interfaces.services.maintenance_service import MaintenanceService
from infrastructure.database.models import SettingModel
from typing import Optional

class MaintenanceServiceImpl(MaintenanceService):
    """
    Service de maintenance s'appuyant sur la base de données.
    """

    def __init__(self, db: Session):
        self.db = db

    def _get_setting(self) -> Optional[SettingModel]:
        return self.db.query(SettingModel).filter_by(cle="maintenance_mode").first()

    def est_actif(self) -> bool:
        setting = self._get_setting()
        return setting is not None and setting.valeur == "1"

    def activer(self) -> None:
        setting = self._get_setting()
        if setting:
            setting.valeur = "1"
        else:
            setting = SettingModel(cle="maintenance_mode", valeur="1")
            self.db.add(setting)
        self.db.commit()

    def desactiver(self) -> None:
        setting = self._get_setting()
        if setting:
            setting.valeur = "0"
            self.db.commit()