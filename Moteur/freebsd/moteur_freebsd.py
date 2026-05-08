#!/usr/bin/env python3

import subprocess
from Moteur.base.moteur_base import MoteurBase


class MoteurFreeBSD(MoteurBase):
    """
    Moteur de collecte de données pour les systèmes FreeBSD.
    Utilise sysctl, sockstat et les commandes BSD à la place de /proc et ss.
    """

    def obtenir_hostname(self) -> str:
        """Récupère le hostname via la commande hostname (pas de /etc/hostname sur FreeBSD)."""
        cmd = subprocess.run(["hostname"], capture_output=True, text=True)
        return cmd.stdout.strip() or "Inconnu"

    def obtenir_ram(self) -> str:
        """Lit la RAM physique via sysctl hw.physmem (remplace /proc/meminfo)."""
        cmd = subprocess.run(["sysctl", "-n", "hw.physmem"], capture_output=True, text=True)
        try:
            ram_octets = int(cmd.stdout.strip())
            ram_mo = ram_octets // (1024 * 1024)
            ram_go = ram_mo / 1024
            return f"MemTotal: {ram_mo} MB ({ram_go:.1f} GB)"
        except ValueError:
            return "Inconnu"

    def obtenir_cpu(self) -> str:
        """Lit le modèle CPU via sysctl hw.model (remplace /proc/cpuinfo)."""
        cmd = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True)
        return cmd.stdout.strip() or "Inconnu"

    def obtenir_processus(self) -> str:
        """Liste les processus avec ps aux (commande POSIX, identique à Linux)."""
        cmd = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        """Affiche l'arborescence avec tree (pkg install tree)."""
        cmd = subprocess.run(
            ["tree", "-L", str(profondeur), chemin],
            capture_output=True,
            text=True
        )
        if cmd.returncode != 0:
            return "(tree non disponible — installer avec : pkg install tree)"
        return cmd.stdout

    def obtenir_ports_ouverts(self) -> str:
        """Liste les sockets en écoute avec sockstat -l (équivalent BSD de ss -tuln)."""
        cmd = subprocess.run(["sockstat", "-l"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_sudoers(self) -> str:
        """Lit le groupe wheel depuis /etc/group (équivalent BSD du groupe sudo)."""
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("wheel:"):
                    return ligne.strip()
        return "Aucun"

    def obtenir_stockage(self) -> str:
        """Affiche l'espace disque avec df -h (commande POSIX, identique à Linux)."""
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
