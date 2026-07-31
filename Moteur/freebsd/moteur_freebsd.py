#!/usr/bin/env python3

import subprocess
from Moteur.base.moteur_base import MoteurBase


class MoteurFreeBSD(MoteurBase):
    def obtenir_hostname(self) -> str:
        cmd = subprocess.run(["hostname"], capture_output=True, text=True)
        return cmd.stdout.strip() or "Inconnu"

    def obtenir_ram(self) -> str:
        cmd = subprocess.run(["sysctl", "-n", "hw.physmem"], capture_output=True, text=True)
        try:
            ram_octets = int(cmd.stdout.strip())
            ram_mo = ram_octets // (1024 * 1024)
            ram_go = ram_mo / 1024
            return f"MemTotal: {ram_mo} MB ({ram_go:.1f} GB)"
        except ValueError:
            return "Inconnu"

    def obtenir_cpu(self) -> str:
        cmd = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True)
        return cmd.stdout.strip() or "Inconnu"

    def obtenir_processus(self) -> str:
        cmd = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        cmd = subprocess.run(
            ["tree", "-L", str(profondeur), chemin],
            capture_output=True,
            text=True
        )
        if cmd.returncode != 0:
            return "(tree non disponible — installer avec : pkg install tree)"
        return cmd.stdout

    def obtenir_ports_ouverts(self) -> str:
        cmd = subprocess.run(["sockstat", "-l"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_sudoers(self) -> str:
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("wheel:"):
                    return ligne.strip()
        return "Aucun"

    def obtenir_stockage(self) -> str:
        cmd = subprocess.run(["df", "-h"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_uptime(self) -> str:
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load averages:")
        return parties[0].strip().rstrip(",") if len(parties) > 0 else "Inconnu"

    def obtenir_load_average(self) -> str:
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load averages:")
        return parties[1].strip() if len(parties) > 1 else "Inconnu"
