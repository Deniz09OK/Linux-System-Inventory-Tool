#!/usr/bin/env python3

from Moteur.linux.moteur_linux import MoteurLinux


class MoteurRocky(MoteurLinux):
    def obtenir_sudoers(self) -> str:
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("wheel:"):
                    return ligne.strip()
        return "Aucun"
