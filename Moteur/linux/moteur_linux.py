#!/usr/bin/env python3

import subprocess
from Moteur.base.moteur_base import MoteurBase


class MoteurLinux(MoteurBase):
    def obtenir_hostname(self) -> str:
        with open("/etc/hostname") as f:
            return f.read().strip()

    def obtenir_ram(self) -> str:
        with open("/proc/meminfo") as f:
            for ligne in f:
                if "MemTotal" in ligne:
                    return ligne.strip()
        return "Inconnu"

    def obtenir_cpu(self) -> str:
        with open("/proc/cpuinfo", "r") as f:
            for ligne in f:
                if "model name" in ligne:
                    return ligne.split(":")[1].strip()
        return "Inconnu"

    def obtenir_processus(self) -> str:
        cmd = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_arborescence(self, chemin: str, profondeur: int = 2) -> str:
        cmd = subprocess.run(
            ["tree", "-L", str(profondeur), chemin],
            capture_output=True,
            text=True
        )
        return cmd.stdout

    def obtenir_ports_ouverts(self) -> str:
        cmd = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_sudoers(self) -> str:
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("sudo:"):
                    return ligne.strip()
        return "Aucun"

    def obtenir_stockage(self) -> str:
        cmd = subprocess.run(["df", "-h"], capture_output=True, text=True)
        return cmd.stdout

    def obtenir_uptime(self) -> str:
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load average:")
        return parties[0].strip().rstrip(",") if len(parties) > 0 else "Inconnu"

    def obtenir_load_average(self) -> str:
        cmd = subprocess.run(["uptime"], capture_output=True, text=True)
        uptime_raw = cmd.stdout.strip()
        parties = uptime_raw.split("load average:")
        return parties[1].strip() if len(parties) > 1 else "Inconnu"
