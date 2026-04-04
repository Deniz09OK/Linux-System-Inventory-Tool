#!/usr/bin/env python3
import argparse
import json
import os
import threading
import logging
from flask import Flask, render_template, jsonify
from moteur_base import choisir_moteur

dossier_script = os.path.dirname(os.path.realpath(__file__))
chemin_changelog = os.path.join(dossier_script, "CHANGELOG.md")

version_lsit = "LSIT (version inconnue)"
try:
    with open(chemin_changelog, "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("## v"):
                version_brute = ligne.replace("##", "").strip()
                version_lsit = f"LSIT {version_brute}"
                break
except FileNotFoundError:
    pass

parser = argparse.ArgumentParser(description="LSIT - Linux System Inventory Tool : Cartographie l'infrastructure locale.")
parser.add_argument("-v", "--version", action="version", version=version_lsit)
parser.add_argument("--format", choices=["txt", "json"], help="Génère directement un rapport sans passer par le menu")
parser.add_argument("--serve", action="store_true", help="Lance directement le tableau de bord web sur le port 8080")
args = parser.parse_args()

# Auto-détection de l'OS et initialisation du moteur approprié
moteur_actif = choisir_moteur()


def afficher_menu():
    print("\n===================================")
    print(f"   {version_lsit}")
    print("===================================")
    print("  1. Générer un rapport TXT")
    print("  2. Générer un rapport JSON")
    print("  3. Lancer le tableau de bord web")
    print("  4. Retour au menu principal")
    print("===================================")


def mode_txt(donnees: dict) -> None:
    with open("rapport_lsit.txt", "a") as f:
        f.write(f"Date de l'audit : {donnees['date']}\n")
        f.write(f"La cible a été identifiée. Nom de la machine : {donnees['machine']}\n")
        f.write(f"Mémoire totale : {donnees['ram']}\n")
        f.write(f"Modèle du CPU : {donnees['cpu']}\n")

        f.write("\n===================================\n")
        f.write("        PROCESSUS ACTIFS           \n")
        f.write("===================================\n")
        f.write(donnees["processus"])

        f.write("\n===================================\n")
        f.write("      ARBORESCENCE DOSSIERS        \n")
        f.write("===================================\n")
        f.write(donnees["arborescence"])

        f.write("\n===================================\n")
        f.write("       AUDIT DE SÉCURITÉ           \n")
        f.write("===================================\n")
        f.write(f"Groupe Sudo : {donnees['securite_sudoers']}\n\n")
        f.write("Ports ouverts :\n")
        f.write(donnees["securite_ports"])

    print("Rapport TXT généré avec succès !")
    input("Appuyez sur Entrée pour revenir au menu...")


def mode_json(donnees: dict) -> None:
    with open("rapport_lsit.json", "w") as f:
        json.dump(donnees, f, indent=4)

    print("Rapport JSON généré avec succès !")
    input("Appuyez sur Entrée pour revenir au menu...")


def mode_serve() -> None:
    app = Flask(__name__, template_folder=os.path.join(dossier_script, "templates"),
                          static_folder=os.path.join(dossier_script, "static"))

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/')
    def dashboard():
        donnees = moteur_actif.collecter_donnees()
        return render_template('dashboard.html',
                               date_audit=donnees["date"],
                               hostname=donnees["machine"],
                               cpu_info=donnees["cpu"],
                               ram_info=donnees["ram"],
                               utilisateurs_sudo=donnees["securite_sudoers"],
                               ports_ouverts=donnees["securite_ports"],
                               arborescence=donnees["arborescence"],
                               processus_actifs=donnees["processus"],
                               stockage=donnees["stockage"],
                               uptime=donnees["uptime"],
                               load_average=donnees["load_average"],
                               version_lsit=version_lsit)

    @app.route('/api/donnees')
    def api_donnees():
        donnees = moteur_actif.collecter_donnees()
        donnees["version_lsit"] = version_lsit
        return jsonify(donnees)

    PORT = 8080
    print(f"\nTableau de bord Flask disponible sur : http://localhost:{PORT}")
    print('Tapez "exit" ou "end" pour arrêter le serveur et revenir au menu.\n')

    thread_serveur = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': PORT, 'use_reloader': False})
    thread_serveur.daemon = True
    thread_serveur.start()

    while True:
        commande = input("> ").strip().lower()
        if commande in ("exit", "end"):
            print("Serveur arrêté. (Appuyez sur Entrée pour continuer)")
            break


def main():
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip().lower()

        if choix in ("exit", "end", "4"):
            break
        elif choix == "1":
            print("\nCollecte des données en cours...")
            donnees = moteur_actif.collecter_donnees()
            mode_txt(donnees)
        elif choix == "2":
            print("\nCollecte des données en cours...")
            donnees = moteur_actif.collecter_donnees()
            mode_json(donnees)
        elif choix == "3":
            print("\nDémarrage du serveur web...")
            mode_serve()
        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")


if args.format or args.serve:
    if args.serve:
        mode_serve()
    else:
        donnees = moteur_actif.collecter_donnees()
        if args.format == "json":
            mode_json(donnees)
        else:
            mode_txt(donnees)
else:
    main()
