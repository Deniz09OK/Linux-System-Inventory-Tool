# LSIT - Linux System Inventory Tool

LSIT est un outil d'inventaire et de cartographie d'infrastructure système développé en Python. Il permet d'auditer rapidement une machine Linux, d'extraire ses métriques vitales et de générer un rapport structuré ou de visualiser les données via un tableau de bord web.

Ce projet met en pratique les concepts d'Infrastructure as Code (IaC) et de développement d'outils d'administration en ligne de commande (CLI).

## Fonctionnalités (v0.3.1)

- **Auto-détection** : Récupération du nom d'hôte, de la RAM totale et du modèle de CPU.
- **Audit d'activité** : Capture des processus actifs et cartographie de l'arborescence `/home/vagrant`.
- **Audit de sécurité** : Détection des ports réseau en écoute (`ss -tuln`) et identification des utilisateurs avec privilèges sudo.
- **Interopérabilité** : Exportation des rapports au format texte brut (`.txt`) ou structuré (`.json`).
- **Tableau de bord web** : Visualisation des données en temps réel via un serveur Flask intégré (port 8080), lancé en arrière-plan grâce au multithreading.
- **Menu interactif SSH** : Interface de navigation accessible directement depuis la session SSH.
- **Horodatage** : Traçabilité précise de l'heure de l'audit.
- **Version dynamique** : La version est lue automatiquement depuis le `CHANGELOG.md`.
- **Automatisation Cron** : Génération quotidienne automatique d'un rapport JSON à minuit.

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

> Le port `8080` de la VM est automatiquement redirigé vers le port `8081` de la machine hôte.

## Utilisation

Une fois connecté en SSH, le menu interactif se lance automatiquement. La commande `lsit` est également disponible globalement sur le système.

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
   LSIT v0.3.1 - 2026-03-26
===================================
  1. Générer un rapport TXT
  2. Générer un rapport JSON
  3. Lancer le tableau de bord web
  4. Retour au menu principal
===================================
```

## Tableau de bord web

Le tableau de bord web est accessible sur `http://localhost:8081` (port forwardé depuis la VM) après le lancement via `lsit --serve` ou l'option 3 du menu interactif.

Il affiche en temps réel les informations suivantes :

| Section | Contenu |
| --- | --- |
| Machine | Nom d'hôte de la machine |
| Processeur | Modèle du CPU |
| Mémoire RAM | Quantité totale de RAM |
| Sudoers | Utilisateurs avec privilèges sudo |
| Ports réseau en écoute | Sortie de `ss -tuln` |
| Arborescence /home/vagrant | Structure des dossiers (2 niveaux) |
| Processus actifs | Sortie de `ps aux` |

Pour arrêter le serveur, tapez `exit` ou `end` dans le terminal.

## Format des rapports

### TXT (`rapport_lsit.txt`)

```text
Date de l'audit : 2026-03-26 10:30:00
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
  "date": "2026-03-26 10:30:00",
  "machine": "debian-vm",
  "ram": "MemTotal: 2048000 kB",
  "cpu": "Intel(R) Core(TM) i7-...",
  "processus": "...",
  "arborescence": "...",
  "securite_ports": "Netid  State   Local Address:Port  ...",
  "securite_sudoers": "sudo:x:27:vagrant"
}
```

## CI/CD — Versioning automatique

Le projet utilise un workflow GitHub Actions (`versionning.yml`) pour gérer le versioning sémantique automatiquement à chaque push sur `main`.

| Préfixe de commit | Effet |
| --- | --- |
| `feat:` / `✨` / `🚀` | Bump mineur (x.**Y**.0) |
| `fix:` / `🐛` / `perf:` / `refactor:` | Bump patch (x.y.**Z**) |
| `BREAKING CHANGE` / `!:` | Bump majeur (**X**.0.0) |
| `docs:` / autres | Pas de bump |

Le workflow génère et commit automatiquement le `CHANGELOG.md`, puis crée et pousse le tag Git correspondant. Un mode **dry-run** est disponible via `workflow_dispatch` pour prévisualiser les changements sans les appliquer.

## Structure du projet

```text
Linux-System-Inventory-Tool/
├── .github/
│   └── workflows/
│       └── versionning.yml  # Workflow CI/CD de versioning sémantique
├── lsit.py                  # Script principal
├── Vagrantfile              # Configuration de la VM Debian 12
├── CHANGELOG.md             # Historique des versions
├── templates/
│   └── dashboard.html       # Template du tableau de bord web (Flask)
├── static/
│   └── dashboard.css        # Styles du tableau de bord
└── .gitignore
```