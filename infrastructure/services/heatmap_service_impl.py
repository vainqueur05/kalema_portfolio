"""
Implémentation du service de carte de chaleur.
Pour l'instant, une implémentation minimale en mémoire.
Évoluera vers une table dédiée ou Redis selon les besoins.
Respecte l'interface HeatmapService.
"""

from typing import Any, Dict, List
from collections import defaultdict
from application.interfaces.services.heatmap_service import HeatmapService


class HeatmapServiceImpl(HeatmapService):
    """
    Service de carte de chaleur avec stockage en mémoire (démonstration).
    À remplacer par une solution persistante pour la production.
    """

    def __init__(self):
        # Structure : { page: [ {x, y, type, timestamp}, ... ] }
        self._stockage: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def enregistrer_evenement(self, evenement: Dict[str, Any]) -> None:
        page = evenement.get("page", "/")
        self._stockage[page].append(evenement)

    def recuperer_donnees(self, page: str = None) -> List[Dict[str, Any]]:
        if page:
            return self._stockage.get(page, [])
        # Toutes pages confondues
        tous = []
        for events in self._stockage.values():
            tous.extend(events)
        return tous