#!/usr/bin/env python3

import platform
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict


class MoteurBase(ABC):
    """
    Classe abstraite définissant le contrat que tout moteur OS doit respecter.
    Impossible à instancier directement - les enfants (Linux, FreeBSD) 
    DOIVENT implémenter toutes les méthodes @abstractmethod.
    """

    @abstractmethod
    def obtenir_hostname(self) -> str:
        """Retourne le nom de la machine."""
        pass

    @abstractmethod
    def obtenir_ram(self) -> str:
        """Retourne les informations sur la mémoire totale."""
        pass

    @abstractmethod
    def obtenir_cpu(self) -> str:
        """Retourne le modèle du processeur."""
        pass

    @abstractmethod
    def obtenir_processus(self) -> str:
        """Retourne la liste des processus actifs."""
        pass

    @abstractmethod
    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        """Retourne l'arborescence d'un dossier."""
        pass

    @abstractmethod
    def obtenir_ports_ouverts(self) -> str:
        """Retourne la liste des ports ouverts."""
        pass

    @abstractmethod
    def obtenir_sudoers(self) -> str:
        """Retourne les utilisateurs ayant des droits sudo/wheel."""
        pass

    @abstractmethod
    def obtenir_stockage(self) -> str:
        """Retourne l'espace disque."""
        pass

    @abstractmethod
    def obtenir_uptime(self) -> str:
        """Retourne le temps de fonctionnement."""
        pass

    @abstractmethod
    def obtenir_load_average(self) -> str:
        """Retourne la charge système."""
        pass

    # Méthode NON abstraite (commune à tous les OS)
    def obtenir_date_audit(self) -> str:
        """Retourne la date actuelle - identique sur tous les OS."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def collecter_donnees(self) -> Dict[str, str]:
        """Collecte toutes les données et retourne un dictionnaire."""
        return {
            "date": self.obtenir_date_audit(),
            "machine": self.obtenir_hostname(),
            "ram": self.obtenir_ram(),
            "cpu": self.obtenir_cpu(),
            "processus": self.obtenir_processus(),
            "arborescence": self.obtenir_arborescence("/home/vagrant"),
            "securite_ports": self.obtenir_ports_ouverts(),
            "securite_sudoers": self.obtenir_sudoers(),
            "stockage": self.obtenir_stockage(),
            "uptime": self.obtenir_uptime(),
            "load_average": self.obtenir_load_average()
        }


def choisir_moteur() -> MoteurBase:
    """
    Routeur intelligent qui détecte l'OS et retourne le moteur approprié.
    Utilise platform.system() qui renvoie "Linux", "FreeBSD", "Windows", etc.
    """
    systeme = platform.system()

    if systeme == "Linux":
        from moteur_linux import MoteurLinux
        return MoteurLinux()

    elif systeme == "FreeBSD":
        # TODO: À implémenter dans l'étape suivante
        # from moteur_freebsd import MoteurFreeBSD
        # return MoteurFreeBSD()
        raise NotImplementedError(
            f"Le moteur FreeBSD n'est pas encore implémenté. "
            f"OS détecté : {systeme}"
        )

    else:
        raise NotImplementedError(
            f"Système d'exploitation non supporté : {systeme}. "
            f"Seuls Linux et FreeBSD sont pris en charge."
        )
