# LSIT - Linux System Inventory Tool

LSIT est un outil d'inventaire et de cartographie d'infrastructure système développé en Python. Il permet d'auditer rapidement une machine Linux, d'extraire ses métriques vitales et de générer un rapport structuré ou de visualiser les données via un tableau de bord web.

Ce projet met en pratique les concepts d'Infrastructure as Code (IaC) et de développement d'outils d'administration en ligne de commande (CLI).

## Fonctionnalités (v0.3.0)

- **Auto-détection** : Récupération du nom d'hôte, de la RAM totale et du modèle de CPU.
- **Audit d'activité** : Capture des processus actifs et cartographie de l'arborescence.
- **Audit de sécurité** : Détection des ports réseau en écoute (`ss -tuln`) et identification des utilisateurs avec privilèges sudo.
- **Interopérabilité** : Exportation des rapports au format texte brut (`.txt`) ou structuré (`.json`).
- **Tableau de bord web** : Visualisation des données en temps réel via un serveur HTTP intégré (port 8080), lancé en arrière-plan grâce au multithreading.
- **Menu interactif SSH** : Interface de navigation accessible directement depuis la session SSH.
- **Horodatage** : Traçabilité précise de l'heure de l'audit.
- **Version dynamique** : La version est lue automatiquement depuis le `CHANGELOG.md`.

## Prérequis

Pour déployer le laboratoire d'environnement isolé, vous devez avoir installé sur votre machine hôte :

- [Vagrant](https://developer.hashicorp.com/vagrant)
- [VirtualBox](https://www.virtualbox.org/)
- [Git](https://git-scm.com/)

## Installation et Déploiement

L'environnement est entièrement automatisé. L'outil s'installe globalement sur la machine cible lors du provisionnement.

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/Deniz09OK/Linux-System-Inventory-Tool
   cd Linux-System-Inventory-Tool
   ```

2. Démarrez l'infrastructure (Debian 12) :

   ```bash
   vagrant up
   ```

3. Connectez-vous au serveur :

   ```bash
   vagrant ssh
   ```

## Utilisation

Une fois connecté en SSH, la commande `lsit` est disponible globalement sur le système.

```bash
# Lancer le menu interactif (défaut)
lsit

# Générer directement un rapport texte
lsit --format txt

# Générer directement un rapport JSON structuré
lsit --format json

# Lancer directement le tableau de bord web sur le port 8080
lsit --serve

# Afficher la version
lsit -v
```

### Menu interactif

```text
===================================
   LSIT v0.3.0 - 2026-03-25
===================================
  1. Générer un rapport TXT
  2. Générer un rapport JSON
  3. Lancer le tableau de bord web
  4. Retour au menu principal
===================================
```

## Format des rapports

### TXT (`rapport_lsit.txt`)

```text
Date de l'audit : 2026-03-25 10:30:00
La cible a été identifiée. Nom de la machine : debian-vm
Mémoire totale : MemTotal: 2048000 kB
Modèle du CPU : Intel(R) Core(TM) i7-...

===================================
        PROCESSUS ACTIFS
===================================
...

===================================
      ARBORESCENCE DOSSIERS
===================================
...

===================================
       AUDIT DE SÉCURITÉ
===================================
Groupe Sudo : sudo:x:27:vagrant

Ports ouverts :
Netid  State   Local Address:Port  ...
```

### JSON (`rapport_lsit.json`)

```json
{
  "date": "2026-03-25 10:30:00",
  "machine": "debian-vm",
  "ram": "MemTotal: 2048000 kB",
  "cpu": "Intel(R) Core(TM) i7-...",
  "processus": "...",
  "arborescence": "...",
  "securite_ports": "Netid  State   Local Address:Port  ...",
  "securite_sudoers": "sudo:x:27:vagrant"
}
```

## Structure du projet

```text
Linux-System-Inventory-Tool/
├── lsit.py                  # Script principal
├── Vagrantfile              # Configuration de la VM Debian 12
├── CHANGELOG.md             # Historique des versions
├── templates/
│   ├── dashboard.html       # Template du tableau de bord web
│   └── dashboard.css        # Styles du tableau de bord
└── .gitignore
```
