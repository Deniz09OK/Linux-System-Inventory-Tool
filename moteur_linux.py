#!/usr/bin/env python3

import subprocess
from moteur_base import MoteurBase


class MoteurLinux(MoteurBase):
    """
    Moteur de collecte de données pour les systèmes Linux (Debian, Ubuntu, etc.).
    Utilise /proc, /etc et les commandes GNU/Linux.
    """

    def obtenir_hostname(self) -> str:
        """Lit le hostname depuis /etc/hostname (spécifique Linux)."""
        with open("/etc/hostname") as f:
            return f.read().strip()

    def obtenir_ram(self) -> str:
        """Lit la RAM depuis /proc/meminfo (spécifique Linux)."""
        with open("/proc/meminfo") as f:
            for ligne in f:
                if "MemTotal" in ligne:
                    return ligne.strip()
        return "Inconnu"

    def obtenir_cpu(self) -> str:
        """Lit le modèle CPU depuis /proc/cpuinfo (spécifique Linux)."""
        with open("/proc/cpuinfo", "r") as f:
            for ligne in f:
                if "model name" in ligne:
                    return ligne.split(":")[1].strip()
        return "Inconnu"

    def obtenir_processus(self) -> str:
        """Liste les processus avec ps aux (commande POSIX, fonctionne sur Linux)."""
        cmd = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        """Affiche l'arborescence avec tree (paquet à installer sur Linux)."""
        cmd = subprocess.run(
            ["tree", "-L", str(profondeur), chemin],
            capture_output=True,
            text=True
        )
        return cmd.stdout

    def obtenir_ports_ouverts(self) -> str:
        """Liste les ports ouverts avec ss (remplaçant de netstat sur Linux)."""
        cmd = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_sudoers(self) -> str:
        """Lit le groupe sudo depuis /etc/group (spécifique Linux)."""
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("sudo:"):
                    return ligne.strip()
        return "Aucun"

    def obtenir_stockage(self) -> str:
        """Affiche l'espace disque avec df -h (commande POSIX)."""
        cmd = subprocess.run(["df", "-h"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_uptime(self) -> str:
        """Récupère l'uptime via la commande uptime."""
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load average:")
        return parties[0].strip().rstrip(",") if len(parties) > 0 else "Inconnu"

    def obtenir_load_average(self) -> str:
        """Récupère le load average via la commande uptime."""
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load average:")
        return parties[1].strip() if len(parties) > 1 else "Inconnu"
