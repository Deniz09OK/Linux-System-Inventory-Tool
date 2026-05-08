#!/usr/bin/env python3

from Moteur.linux.moteur_linux import MoteurLinux


class MoteurRocky(MoteurLinux):
    """
    Moteur pour Rocky Linux / RHEL / AlmaLinux.
    Identique au moteur Linux, seul le groupe sudo diffère : wheel au lieu de sudo.
    """

    def obtenir_sudoers(self) -> str:
        """Lit le groupe wheel depuis /etc/group (RHEL utilise wheel, pas sudo)."""
        with open("/etc/group", "r") as f:
            for ligne in f:
                if ligne.startswith("wheel:"):
                    return ligne.strip()
        return "Aucun"
