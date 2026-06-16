"""
Use Case : SnapshotService
===========================
Orchestre la logique métier pour les snapshots de contenu.
Dépend de SnapshotRepository et des repositories de contenu à sauvegarder.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities.snapshot import Snapshot
from application.interfaces.repositories.snapshot_repo import SnapshotRepository
from application.interfaces.repositories.profil_repo import ProfilRepository
from application.interfaces.repositories.projet_repo import ProjetRepository
from application.interfaces.repositories.service_repo import ServiceRepository
from application.interfaces.repositories.lien_contact_repo import LienContactRepository
from application.interfaces.repositories.temoignage_repo import TemoignageRepository
from application.interfaces.repositories.about_repo import AboutRepository


class SnapshotService:
    """
    Service applicatif pour créer, lister, restaurer et supprimer des snapshots.

    Un snapshot capture l'état de tous les contenus (profil, projets, services,
    liens, témoignages, about) dans un dictionnaire sérialisable.
    """

    def __init__(
        self,
        snapshot_repo: SnapshotRepository,
        profil_repo: ProfilRepository,
        projet_repo: ProjetRepository,
        service_repo: ServiceRepository,
        lien_repo: LienContactRepository,
        temoignage_repo: TemoignageRepository,
        about_repo: AboutRepository,
    ):
        self.snapshot_repo = snapshot_repo
        self.profil_repo = profil_repo
        self.projet_repo = projet_repo
        self.service_repo = service_repo
        self.lien_repo = lien_repo
        self.temoignage_repo = temoignage_repo
        self.about_repo = about_repo

    def lister_snapshots(self) -> List[Snapshot]:
        """Retourne tous les snapshots."""
        return self.snapshot_repo.recuperer_tous()

    def recuperer_snapshot(self, id: int) -> Optional[Snapshot]:
        """Retourne un snapshot par ID."""
        return self.snapshot_repo.recuperer_par_id(id)

    def creer_snapshot(self, nom: str) -> Snapshot:
        """
        Capture l'état complet des contenus et crée un snapshot.

        Args:
            nom: Nom descriptif du snapshot.

        Returns:
            Le snapshot créé.
        """
        donnees = {
            "profil": self.profil_repo.recuperer().to_dict() if self.profil_repo.recuperer() else None,
            "projets": [p.to_dict() for p in self.projet_repo.recuperer_tous()],
            "services": [s.to_dict() for s in self.service_repo.recuperer_tous()],
            "liens": [l.to_dict() for l in self.lien_repo.recuperer_tous()],
            "temoignages": [t.to_dict() for t in self.temoignage_repo.recuperer_tous()],
            "about": self.about_repo.recuperer().to_dict() if self.about_repo.recuperer() else None,
        }
        snapshot = Snapshot(nom=nom, donnees_json=donnees)
        return self.snapshot_repo.sauvegarder(snapshot)

    def restaurer_snapshot(self, id: int) -> bool:
        """
        Restaure l'état des contenus à partir d'un snapshot existant.
        Supprime toutes les données actuelles avant restauration pour éviter les conflits.
        """
        snapshot = self.snapshot_repo.recuperer_par_id(id)
        if not snapshot:
            return False

        donnees = snapshot.donnees_json

        # 1. SUPPRIMER tous les projets existants (pour éviter conflit de slug)
        projets_existants = self.projet_repo.recuperer_tous()
        for p in projets_existants:
            self.projet_repo.supprimer(p.id)

        # 2. SUPPRIMER tous les services existants
        services_existants = self.service_repo.recuperer_tous()
        for s in services_existants:
            self.service_repo.supprimer(s.id)

        # 3. SUPPRIMER tous les liens existants
        liens_existants = self.lien_repo.recuperer_tous()
        for l in liens_existants:
            self.lien_repo.supprimer(l.id)

        # 4. SUPPRIMER tous les témoignages existants
        temoignages_existants = self.temoignage_repo.recuperer_tous()
        for t in temoignages_existants:
            self.temoignage_repo.supprimer(t.id)

        # 5. Restauration du profil (sauvegarde écrase l'existant)
        if donnees.get("profil"):
            from domain.entities.profil import Profil
            p = donnees["profil"]
            self.profil_repo.sauvegarder(Profil(
                nom_complet=p["nom_complet"],
                titre=p["titre"],
                bio=p["bio"],
                photo_url=p.get("photo_url"),
            ))

        # 6. Restauration des projets (base vidée, pas de conflit)
        if "projets" in donnees:
            for p_data in donnees["projets"]:
                from domain.entities.projet import Projet
                projet = Projet(
                    titre=p_data["titre"],
                    description_courte=p_data["description_courte"],
                    description_longue=p_data["description_longue"],
                    slug=p_data.get("slug"),
                    histoire=p_data.get("histoire", ""),
                    image_url=p_data.get("image_url"),
                    actif=p_data.get("actif", True),
                    ordre=p_data.get("ordre", 0),
                )
                self.projet_repo.ajouter(projet)

        # 7. Restauration des services
        if "services" in donnees:
            for s_data in donnees["services"]:
                from domain.entities.service import Service
                service = Service(
                    nom=s_data["nom"],
                    description=s_data["description"],
                    prix=s_data.get("prix"),
                    icone=s_data.get("icone"),
                    actif=s_data.get("actif", True),
                    ordre=s_data.get("ordre", 0),
                )
                self.service_repo.ajouter(service)

        # 8. Restauration des liens
        if "liens" in donnees:
            for l_data in donnees["liens"]:
                from domain.entities.lien_contact import LienContact
                lien = LienContact(
                    nom=l_data["nom"],
                    url=l_data["url"],
                    icone=l_data["icone"],
                    actif=l_data.get("actif", True),
                    ordre=l_data.get("ordre", 0),
                )
                self.lien_repo.ajouter(lien)

        # 9. Restauration des témoignages
        if "temoignages" in donnees:
            for t_data in donnees["temoignages"]:
                from domain.entities.temoignage import Temoignage
                temoignage = Temoignage(
                    nom=t_data["nom"],
                    texte=t_data["texte"],
                    photo_url=t_data.get("photo_url"),
                    entreprise=t_data.get("entreprise"),
                    actif=t_data.get("actif", True),
                    ordre=t_data.get("ordre", 0),
                )
                self.temoignage_repo.ajouter(temoignage)

        # 10. Restauration du contenu about
        if donnees.get("about"):
            from domain.entities.about import About
            a = donnees["about"]
            self.about_repo.sauvegarder(About(contenu=a["contenu"]))

        return True

    def supprimer_snapshot(self, id: int) -> bool:
        """
        Supprime un snapshot par ID.

        Returns:
            True si supprimé, False si non trouvé.
        """
        snapshot = self.snapshot_repo.recuperer_par_id(id)
        if not snapshot:
            return False
        self.snapshot_repo.supprimer(id)
        return True