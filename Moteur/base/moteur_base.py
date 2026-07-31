#!/usr/bin/env python3

import platform
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict


class MoteurBase(ABC):
    @abstractmethod
    def obtenir_hostname(self) -> str:
        pass

    @abstractmethod
    def obtenir_ram(self) -> str:
        pass

    @abstractmethod
    def obtenir_cpu(self) -> str:
        pass

    @abstractmethod
    def obtenir_processus(self) -> str:
        pass

    @abstractmethod
    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        pass

    @abstractmethod
    def obtenir_ports_ouverts(self) -> str:
        pass

    @abstractmethod
    def obtenir_sudoers(self) -> str:
        pass

    @abstractmethod
    def obtenir_stockage(self) -> str:
        pass

    @abstractmethod
    def obtenir_uptime(self) -> str:
        pass

    @abstractmethod
    def obtenir_load_average(self) -> str:
        pass

    def obtenir_date_audit(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def collecter_donnees(self) -> Dict[str, str]:
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


def _detecter_distro() -> str:
    try:
        with open("/etc/os-release") as f:
            for ligne in f:
                if ligne.startswith("ID="):
                    return ligne.split("=")[1].strip().strip('"').lower()
    except FileNotFoundError:
        pass
    return "linux"


def choisir_moteur() -> MoteurBase:
    systeme = platform.system()

    if systeme == "Linux":
        distro = _detecter_distro()
        if distro in ("rocky", "rhel", "centos", "almalinux"):
            from Moteur.rocky.moteur_rocky import MoteurRocky
            return MoteurRocky()
        else:
            from Moteur.linux.moteur_linux import MoteurLinux
            return MoteurLinux()

    elif systeme == "FreeBSD":
        from Moteur.freebsd.moteur_freebsd import MoteurFreeBSD
        return MoteurFreeBSD()

    else:
        raise NotImplementedError(
            f"Système d'exploitation non supporté : {systeme}. "
            f"Seuls Linux, Rocky Linux et FreeBSD sont pris en charge."
        )
