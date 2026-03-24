# LSIT - Linux System Inventory Tool 🐧🔍

LSIT est un outil d'inventaire et de cartographie d'infrastructure système développé en Python. Il permet d'auditer rapidement une machine Linux, d'extraire ses métriques vitales et de générer un rapport structuré.

Ce projet met en pratique les concepts d'Infrastructure as Code (IaC) et de développement d'outils d'administration en ligne de commande (CLI).

## 🚀 Fonctionnalités (V1.0)

- **Auto-détection** : Récupération du nom d'hôte, de la RAM totale et du modèle de CPU.
- **Audit d'activité** : Capture des processus actifs et cartographie de l'arborescence.
- **Interopérabilité** : Exportation des rapports au format texte brut (`.txt`) ou structuré (`.json`).
- **Horodatage** : Traçabilité précise de l'heure de l'audit.

## 🛠️ Prérequis

Pour déployer le laboratoire d'environnement isolé, vous devez avoir installé sur votre machine hôte :

- [Vagrant](https://developer.hashicorp.com/vagrant)
- [VirtualBox](https://www.virtualbox.org/)
- Git

## 📦 Installation et Déploiement

L'environnement est entièrement automatisé. L'outil s'installe globalement sur la machine cible lors du provisionnement.

1. Clonez ce dépôt :

   ```bash
   git clone <URL_DU_DEPOT>
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

## 💻 Utilisation

Une fois connecté en SSH, la commande `lsit` est disponible globalement sur le système.

```bash
# Afficher l'aide
lsit --help

# Générer un rapport texte (défaut)
lsit

# Générer un rapport JSON structuré
lsit --format json

# Afficher la version
lsit -v
```

## 📄 Format des rapports

### TXT (`rapport_lsit.txt`)

```text
=== Audit LSIT - 2024-01-15 10:30:00 ===
Hostname : debian-vm
RAM totale : MemTotal: 2048000 kB
CPU : Intel(R) Core(TM) i7-...
--- Processus actifs ---
...
--- Arborescence /home/vagrant ---
...
```

### JSON (`rapport_lsit.json`)

```json
{
  "date": "2024-01-15 10:30:00",
  "hostname": "debian-vm",
  "ram": "MemTotal: 2048000 kB",
  "cpu": "Intel(R) Core(TM) i7-...",
  "processus": "...",
  "arborescence": "..."
}
```

## 🗂️ Structure du projet

```text
Linux-System-Inventory-Tool/
├── lsit.py         # Script principal
├── Vagrantfile     # Configuration de la VM Debian 12
└── .gitignore
```
