# LSIT - Linux System Inventory Tool

LSIT est un outil d'inventaire et de cartographie d'infrastructure système développé en Python. Il permet d'auditer rapidement une machine Linux ou FreeBSD, d'extraire ses métriques vitales et de générer un rapport structuré ou de visualiser les données via un tableau de bord web.

Ce projet met en pratique les concepts d'Infrastructure as Code (IaC), de développement d'outils d'administration en ligne de commande (CLI) et de conception orientée objet (Strategy Pattern multi-OS).

## Fonctionnalités (v0.6.0)

- **Support multi-OS** : Architecture à moteurs interchangeables (Strategy Pattern) — Debian/Linux et FreeBSD 14 supportés nativement.
- **Auto-détection** : Récupération du nom d'hôte, de la RAM totale et du modèle de CPU.
- **Métriques Système** : Collecte de l'espace disque (`df -h`), du temps d'activité (Uptime) et de la charge système (Load Average).
- **Audit d'activité** : Capture des processus actifs et cartographie de l'arborescence `/home/vagrant`.
- **Audit de sécurité** : Détection des ports réseau en écoute (`ss -tuln` sur Linux, `sockstat -l` sur FreeBSD) et identification des utilisateurs avec privilèges sudo/wheel.
- **Tableau de bord web "Live"** : Interface UI/UX moderne (thème Cybersec) avec rafraîchissement asynchrone (API REST / Fetch) en temps réel, propulsé par Flask (port 5000).
- **Interopérabilité** : Exportation des rapports au format texte brut (`.txt`) ou structuré (`.json`).
- **Menu interactif SSH** : Interface de navigation accessible directement depuis la session SSH.
- **Horodatage & Version dynamique** : Traçabilité de l'audit et lecture automatique de la version depuis le `CHANGELOG.md`.
- **Automatisation Cron** : Génération quotidienne automatique d'un rapport JSON à minuit.

## Prérequis

Pour déployer le laboratoire d'environnement isolé, vous devez avoir installé sur votre machine hôte :

- [Vagrant](https://developer.hashicorp.com/vagrant)
- [VirtualBox](https://www.virtualbox.org/)
- [Git](https://git-scm.com/)

## Installation et Déploiement

L'environnement est entièrement automatisé via un Vagrantfile multi-machines. L'outil s'installe globalement sur chaque machine cible lors du provisionnement.

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/Deniz09OK/Linux-System-Inventory-Tool
   cd Linux-System-Inventory-Tool
   ```

2. Démarrez l'infrastructure :

   ```bash
   # Démarrer toutes les VMs (Debian + FreeBSD)
   vagrant up

   # Ou démarrer une VM spécifique
   vagrant up debian
   vagrant up freebsd
   ```

3. Connectez-vous à la machine souhaitée :

   ```bash
   vagrant ssh debian
   vagrant ssh freebsd
   ```

**Ports redirigés :**

| Machine | Port interne | Port hôte |
| --- | --- | --- |
| Debian 12 | 5000 | 8081 |
| FreeBSD 14 | 5000 | 8082 |

## Utilisation

Une fois connecté en SSH, le menu interactif se lance automatiquement. La commande `lsit` est également disponible globalement sur le système.

```bash
# Lancer le menu interactif (défaut)
lsit

# Générer directement un rapport texte
lsit --format txt

# Générer directement un rapport JSON structuré
lsit --format json

# Lancer directement le tableau de bord web sur le port 5000
lsit --serve

# Afficher la version
lsit -v
```

### Menu interactif (Debian)

```text
===================================
   LSIT v0.6.0
===================================
  1. Générer un rapport TXT
  2. Générer un rapport JSON
  3. Lancer le tableau de bord web
  4. Retour au menu principal
===================================
```

### Menu d'accueil SSH (FreeBSD)

```text
  ╔══════════════════════════════════════════╗
  ║   LSIT - FreeBSD System Inventory Tool   ║
  ╚══════════════════════════════════════════╝

    [1]  Interface graphique  (port 8082)
    [2]  Rapport TXT
    [3]  Rapport JSON
    [4]  Shell uniquement
    [5]  Quitter
```

## Tableau de bord web

Le tableau de bord est accessible sur `http://localhost:8081` (Debian) ou `http://localhost:8082` (FreeBSD) après le lancement via `lsit --serve` ou l'option correspondante du menu.

L'interface s'actualise automatiquement et de manière asynchrone (sans rechargement de page) toutes les 5 secondes via une API interne. Elle affiche les informations suivantes :

| Section | Contenu |
| --- | --- |
| Machine | Nom d'hôte de la machine |
| Processeur | Modèle du CPU |
| Mémoire RAM | Quantité totale de RAM |
| Sudoers | Utilisateurs avec privilèges sudo (Linux) / groupe wheel (FreeBSD) |
| Stockage | Espace disque disponible sur les partitions (`df -h`) |
| Uptime | Temps depuis le dernier démarrage |
| Charge Système | Load Average sur 1, 5 et 15 minutes |
| Ports réseau en écoute | `ss -tuln` (Linux) ou `sockstat -l` (FreeBSD) |
| Arborescence /home/vagrant | Structure des dossiers (2 niveaux) |
| Processus actifs | Sortie de `ps aux` |

### API REST

L'endpoint `/api/donnees` retourne toutes les métriques au format JSON, permettant l'intégration avec d'autres outils de monitoring.

```bash
# Depuis Debian
curl http://localhost:8081/api/donnees

# Depuis FreeBSD
curl http://localhost:8082/api/donnees
```

Pour arrêter le serveur, tapez `exit` ou `end` dans le terminal.

## Format des rapports

### TXT (`rapport_lsit.txt`)

```text
Date de l'audit : 2026-05-08 10:30:00
La cible a été identifiée. Nom de la machine : freebsd-vm
Mémoire totale : MemTotal: 1024 MB (1.0 GB)
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
Groupe Sudo : wheel:*:0:root,vagrant

Ports ouverts :
USER     COMMAND    PID   FD PROTO  ...
```

### JSON (`rapport_lsit.json` ou sortie API)

```json
{
  "date": "2026-05-08 10:30:00",
  "machine": "freebsd-vm",
  "ram": "MemTotal: 1024 MB (1.0 GB)",
  "cpu": "Intel(R) Core(TM) i7-...",
  "uptime": "up 2 hours, 30 minutes",
  "load_average": "0.01, 0.05, 0.00",
  "stockage": "Filesystem      Size  Used Avail Use% Mounted on...",
  "processus": "...",
  "arborescence": "...",
  "securite_ports": "USER     COMMAND    PID   FD PROTO  ...",
  "securite_sudoers": "wheel:*:0:root,vagrant",
  "version_lsit": "LSIT v0.6.0"
}
```

## Architecture multi-moteurs

LSIT utilise un **Strategy Pattern** pour supporter plusieurs systèmes d'exploitation sans modifier le cœur de l'application. Chaque moteur est isolé dans son propre sous-dossier du package `Moteur/`.

```text
Moteur/
├── base/
│   └── moteur_base.py    ← Classe abstraite + routeur choisir_moteur()
├── linux/
│   └── moteur_linux.py   ← Implémentation Linux (/proc, ss, sudo)
└── freebsd/
    └── moteur_freebsd.py ← Implémentation FreeBSD (sysctl, sockstat, wheel)
```

La détection de l'OS est automatique au démarrage via `platform.system()`. Aucune configuration manuelle n'est nécessaire.

## CI/CD — Versioning automatique

Le projet utilise un workflow GitHub Actions (`versionning.yml`) pour gérer le versioning sémantique automatiquement à chaque push sur `main`.

| Préfixe de commit | Effet |
| --- | --- |
| `feat:` | Bump mineur (x.**Y**.0) |
| `fix:` / `perf:` / `refactor:` | Bump patch (x.y.**Z**) |
| `BREAKING CHANGE` / `!:` | Bump majeur (**X**.0.0) |
| `docs:` / autres | Pas de bump |

Le workflow génère et commit automatiquement le `CHANGELOG.md`, puis crée et pousse le tag Git correspondant. Un mode **dry-run** est disponible via `workflow_dispatch` pour prévisualiser les changements sans les appliquer.

## Structure du projet

```text
Linux-System-Inventory-Tool/
├── .github/
│   └── workflows/
│       └── versionning.yml       # Workflow CI/CD de versioning sémantique
├── Moteur/
│   ├── base/
│   │   └── moteur_base.py        # Classe abstraite + routeur choisir_moteur()
│   ├── linux/
│   │   └── moteur_linux.py       # Moteur Debian/Linux (/proc, ss, sudo)
│   └── freebsd/
│       └── moteur_freebsd.py     # Moteur FreeBSD 14 (sysctl, sockstat, wheel)
├── lsit.py                       # Script principal (CLI, menu, Flask)
├── Vagrantfile                   # Infrastructure multi-machines (Debian + FreeBSD)
├── CHANGELOG.md                  # Historique des versions (généré automatiquement)
├── templates/
│   └── dashboard.html            # Template du tableau de bord web (Jinja2/Flask)
├── static/
│   └── style.css                 # Styles du tableau de bord
└── .gitignore
```
