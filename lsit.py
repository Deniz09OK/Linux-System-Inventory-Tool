#!/usr/bin/env python3
import subprocess
import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser(description="LSIT - Linux System Inventory Tool : Cartographie l'infrastructure locale.")
parser.add_argument("-v", "--version", action="version", version="LSIT v1.0")
parser.add_argument("--format", choices=["txt", "json"], default="txt", help="Format de sortie du rapport")
args = parser.parse_args()

with open("/etc/hostname") as f:
    hostname = f.read().strip()

print(f"La cible a été identifiée. Nom de la machine : {hostname}")

ram_info = ""
with open("/proc/meminfo") as f:
    for ligne in f:
        if "MemTotal" in ligne:
            ram_info = ligne.strip()

print(f"Mémoire totale : {ram_info}")

cpu_info = "Inconnu"
with open("/proc/cpuinfo", "r") as f:
    for ligne in f:
        if "model name" in ligne:
            cpu_info = ligne.split(":")[1].strip()
            break

cmd_ps = subprocess.run(["ps", "aux"], capture_output=True, text=True)
processus_actifs = cmd_ps.stdout

cmd_tree = subprocess.run(["tree", "-L", "2", "/home/vagrant"], capture_output=True, text=True)
arborescence = cmd_tree.stdout

# Audit de sécurité : Ports réseau en écoute
cmd_ports = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
ports_ouverts = cmd_ports.stdout

# Audit de sécurité : Utilisateurs avec privilèges sudo
utilisateurs_sudo = "Aucun"
with open("/etc/group", "r") as f:
    for ligne in f:
        if ligne.startswith("sudo:"):
            utilisateurs_sudo = ligne.strip()
            break

date_audit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if args.format == "json":
    donnees_audit = {
        "date": date_audit,
        "machine": hostname,
        "ram": ram_info,
        "cpu": cpu_info,
        "processus": processus_actifs,
        "arborescence": arborescence,
        "securite_ports": ports_ouverts,
        "securite_sudoers": utilisateurs_sudo
    }

    with open("rapport_lsit.json", "w") as f:
        json.dump(donnees_audit, f, indent=4)

    print("Rapport JSON généré avec succès !")

else:
    with open("rapport_lsit.txt", "a") as f:
        f.write(f"Date de l'audit : {date_audit}\n")
        f.write(f"La cible a été identifiée. Nom de la machine : {hostname}\n")
        f.write(f"Mémoire totale : {ram_info}\n")
        f.write(f"Modèle du CPU : {cpu_info}\n")

        f.write("\n===================================\n")
        f.write("        PROCESSUS ACTIFS           \n")
        f.write("===================================\n")
        f.write(processus_actifs)

        f.write("\n===================================\n")
        f.write("      ARBORESCENCE DOSSIERS        \n")
        f.write("===================================\n")
        f.write(arborescence)

        f.write("\n===================================\n")
        f.write("       AUDIT DE SÉCURITÉ           \n")
        f.write("===================================\n")
        f.write(f"Groupe Sudo : {utilisateurs_sudo}\n\n")
        f.write("Ports ouverts :\n")
        f.write(ports_ouverts)

    print("Rapport TXT généré avec succès !")
