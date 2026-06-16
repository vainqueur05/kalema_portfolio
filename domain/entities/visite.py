"""
Entité : Visite
===============
Représente une visite enregistrée sur la partie publique du portfolio.
Fait partie du domaine métier (Clean Architecture).

Règles métier :
- page : obligatoire, chemin relatif de la page visitée.
- ip : obligatoire, adresse IP (IPv4 ou IPv6).
- user_agent : optionnel, chaîne brute du navigateur.
- referrer : optionnel, URL du référent.
- pays, ville : optionnels, issus de la géolocalisation.
- navigateur, os, appareil : optionnels, extraits du user_agent.
- date : géré par l'infrastructure, NON inclus dans l'entité.
"""

from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class Visite:
    """
    Entité représentant une visite.

    Attributes:
        page (str): Page visitée (ex: '/').
        ip (str): Adresse IP.
        user_agent (Optional[str]): User-Agent HTTP.
        referrer (Optional[str]): Référent.
        pays (Optional[str]): Pays détecté.
        ville (Optional[str]): Ville détectée.
        navigateur (Optional[str]): Navigateur extrait.
        os (Optional[str]): Système d'exploitation extrait.
        appareil (Optional[str]): Type d'appareil (mobile, desktop).
        id (Optional[int]): Identifiant technique.
    """

    page: str
    ip: str
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    pays: Optional[str] = None
    ville: Optional[str] = None
    navigateur: Optional[str] = None
    os: Optional[str] = None
    appareil: Optional[str] = None
    id: Optional[int] = field(default=None, repr=True)

    def __post_init__(self):
        """Validation des champs."""
        # --- Page ---
        if not self.page or not self.page.strip():
            raise ValueError("Le chemin de la page est obligatoire.")
        page_clean = self.page.strip()
        if not page_clean.startswith("/"):
            raise ValueError("Le chemin de la page doit commencer par '/'.")
        if len(page_clean) > 500:
            raise ValueError("Le chemin de la page ne doit pas dépasser 500 caractères.")
        object.__setattr__(self, "page", page_clean)

        # --- IP ---
        if not self.ip or not self.ip.strip():
            raise ValueError("L'adresse IP est obligatoire.")
        ip_clean = self.ip.strip()
        # Validation IPv4 ou IPv6 simple
        if not (self._is_valid_ipv4(ip_clean) or self._is_valid_ipv6(ip_clean)):
            raise ValueError(f"Adresse IP invalide : {ip_clean}")
        object.__setattr__(self, "ip", ip_clean)

        # --- User-Agent ---
        if self.user_agent is not None:
            ua_clean = self.user_agent.strip()
            object.__setattr__(self, "user_agent", ua_clean if ua_clean else None)

        # --- Referrer ---
        if self.referrer is not None:
            ref_clean = self.referrer.strip()
            if ref_clean and not (
                ref_clean.startswith("http://") or ref_clean.startswith("https://")
            ):
                raise ValueError("Le référent doit être une URL valide (http/https).")
            object.__setattr__(self, "referrer", ref_clean if ref_clean else None)

        # --- Pays, Ville ---
        for attr_name in ("pays", "ville"):
            value = getattr(self, attr_name)
            if value is not None:
                clean = value.strip()
                if clean and len(clean) > 100:
                    raise ValueError(f"Le champ '{attr_name}' ne doit pas dépasser 100 caractères.")
                object.__setattr__(self, attr_name, clean if clean else None)

        # --- Navigateur, OS, Appareil ---
        for attr_name in ("navigateur", "os", "appareil"):
            value = getattr(self, attr_name)
            if value is not None:
                clean = value.strip()
                if clean and len(clean) > 100:
                    raise ValueError(f"Le champ '{attr_name}' ne doit pas dépasser 100 caractères.")
                object.__setattr__(self, attr_name, clean if clean else None)

    @staticmethod
    def _is_valid_ipv4(ip: str) -> bool:
        """Vérifie si l'IP est une IPv4 valide."""
        pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(pattern, ip)
        if not match:
            return False
        return all(0 <= int(part) <= 255 for part in match.groups())

    @staticmethod
    def _is_valid_ipv6(ip: str) -> bool:
        """Vérifie si l'IP est une IPv6 valide (forme simplifiée)."""
        # Accepte les IPv6 complètes ou compressées
        pattern = r"^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$"
        return re.match(pattern, ip) is not None

    def to_dict(self) -> dict:
        """Sérialise l'entité en dictionnaire."""
        return {
            "id": self.id,
            "page": self.page,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "referrer": self.referrer,
            "pays": self.pays,
            "ville": self.ville,
            "navigateur": self.navigateur,
            "os": self.os,
            "appareil": self.appareil,
        }

    def __repr__(self) -> str:
        return f"Visite(id={self.id}, page='{self.page}', ip='{self.ip}')"