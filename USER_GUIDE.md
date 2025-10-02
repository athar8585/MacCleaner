# 🚀 MacCleaner Pro v3.5+ - Guide Utilisateur

## 📋 Table des Matières
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Surveillance Heuristique](#surveillance-heuristique)
- [Profiling de Performance](#profiling-de-performance)
- [Tests et Qualité](#tests-et-qualité)
- [Dépannage](#dépannage)

## 🔧 Installation

### Prérequis
- **macOS 10.14+** (Mojave ou plus récent)
- **Python 3.8+** installé
- **pip3** pour la gestion des paquets

### Installation Automatique
```bash
# Téléchargez le projet et lancez :
chmod +x install.sh
./install.sh
```

### Installation Manuelle
```bash
# 1. Cloner/télécharger le projet
git clone https://github.com/athar8585/MacCleaner.git
cd MacCleaner

# 2. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python3 launch.py
```

## 🖥️ Utilisation

### Lancement
```bash
# Après installation automatique :
maccleaner

# Ou directement :
python3 launch.py
```

### Interface Principale
L'application dispose de 6 sections principales :

#### 1. **Informations Système**
- Affichage en temps réel de l'espace disque
- Statistiques mémoire et CPU
- Nombre de processus actifs

#### 2. **Options de Nettoyage**
- ✅ **System Caches** : Caches système (~/Library/Caches, /var/folders)
- ✅ **User Caches** : Caches utilisateur et navigateurs  
- ✅ **Logs & Diagnostics** : Journaux et rapports de diagnostic
- ✅ **Downloads & Trash** : Téléchargements et corbeille
- ✅ **Browser Data** : Données de navigation (historique, cookies)
- ✅ **System Temp** : Fichiers temporaires système

#### 3. **Zone de Progression**
- Log en temps réel des opérations
- Barre de progression pour les tâches longues
- Statistiques d'espace libéré

#### 4. **Boutons d'Action**
- 🧹 **Nettoyer** : Lancement du nettoyage standard
- 🛡️ **Scan Malware** : Détection de malware
- 📊 **Profiling** : Surveillance des performances
- 🔍 **Surveillance** : Scanner heuristique temps réel
- 🔔 **Test Notifs** : Test du système de notifications
- 🔄 **MAJ Complète** : Mise à jour complète

## ⚡ Fonctionnalités

### 🛡️ Protection iCloud
- **Détection automatique** des fichiers synchronisés iCloud
- **Protection par défaut** : évite la suppression accidentelle
- **Marquage visuel** dans les logs

### 🔄 Planificateur Automatique
- **Nettoyage programmé** : quotidien, hebdomadaire, mensuel
- **Conditions intelligentes** : batterie, activité utilisateur
- **Notifications** de fin de nettoyage

### 📊 Plugins Extensibles
Le système supporte 4 plugins intégrés :
- **node_modules** : Nettoyage des dépendances Node.js
- **homebrew** : Cache et fichiers temporaires Homebrew
- **docker** : Images et conteneurs Docker inutilisés
- **xcode** : Données Xcode (simulateurs, archives)

## 🔍 Surveillance Heuristique

### Activation
```python
# Cliquez sur "🔍 Surveillance" dans l'interface
# Ou programmez via l'API :
from utils.heuristic import HeuristicScanner
scanner = HeuristicScanner()
scanner.start_monitoring()
```

### Détections
- **Processus suspects** : Utilisation CPU > 80% pendant > 30s
- **Fichiers suspects** : Création dans dossiers sensibles (LaunchAgents, etc.)
- **Activité réseau** : Processus avec > 10 connexions simultanées
- **Noms suspects** : Patterns malware (keylog, backdoor, etc.)

### Alertes
```python
# Récupérer les alertes des dernières 24h
alerts = scanner.get_alerts(24)
for alert in alerts:
    print(f"{alert['type']}: {alert['message']}")

# Export des alertes
scanner.export_alerts('alerts_backup.json')
```

## 📈 Profiling de Performance

### Utilisation
```python
# Via l'interface : bouton "📊 Profiling"
# Ou API directe :
from utils.profiler import PerformanceProfiler
profiler = PerformanceProfiler()

profiler.start_profiling()
# ... opérations à mesurer
profiler.stop_profiling()

# Résumé des métriques
summary = profiler.get_summary()
print(summary)
```

### Métriques Collectées
- **CPU** : Pourcentage d'utilisation
- **Mémoire** : Consommation RAM (MB)
- **Disque** : Espace utilisé (GB)
- **Réseau** : Transferts sent/reçu (MB)
- **Processus** : Nombre de processus actifs
- **I/O** : Opérations lecture/écriture

### Export
```python
# Export CSV des métriques brutes
profiler.export_to_file('performance_report.csv')

# Rapport détaillé
detailed_report = profiler.get_detailed_report()
```

## 🧪 Tests et Qualité

### Suite de Tests
```bash
# Lancer tous les tests
python3 tests/run_tests.py

# Test spécifique
python3 tests/run_tests.py test_heuristic.TestHeuristicScanner.test_alert_creation

# Tests de distribution
python3 test_distribution.py
```

### Couverture Actuelle
- ✅ **27/27 tests** passent (100%)
- ✅ **4 modules** testés : heuristic, integrity, notifications, plugins
- ✅ **Tests d'intégration** complets

### Modules Testés
1. **test_heuristic.py** : Scanner de surveillance (8 tests)
2. **test_integrity.py** : Vérification d'intégrité (5 tests) 
3. **test_notifications.py** : Système de notifications (11 tests)
4. **test_plugins.py** : Gestionnaire de plugins (4 tests)

## 🔔 Notifications

### Configuration
```python
from utils.notifications import notify, notify_completion, notify_alert

# Notification de base
notify("Titre", "Message", sound=True, urgency='normal')

# Notification de fin de tâche
notify_completion("Nettoyage", "Terminé", stats="100MB libérés")

# Alerte critique
notify_alert("Sécurité", "Malware détecté", alert_type='warning')
```

### Types d'Urgence
- `normal` : Notification standard
- `critical` : Alerte critique (son fort)
- `low` : Notification discrète

## 🛠️ Dépannage

### Erreurs Communes

#### 1. **"ModuleNotFoundError: No module named 'psutil'"**
```bash
# Solution :
pip install -r requirements.txt
# Ou :
pip install psutil pync
```

#### 2. **"Permission denied" lors du nettoyage**
```bash
# Solution : Lancer avec permissions admin si nécessaire
sudo python3 launch.py
```

#### 3. **Notifications ne fonctionnent pas**
```bash
# Vérifier pync :
pip install pync
# Ou utiliser osascript (inclus dans macOS)
```

#### 4. **Tests échouent**
```bash
# Vérifier l'environnement virtuel
source venv/bin/activate
pip install -r requirements.txt
python3 tests/run_tests.py
```

### Logs de Debug
```python
# Activer logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Support
- **GitHub** : https://github.com/athar8585/MacCleaner/issues
- **Documentation** : README.md du projet
- **Tests** : `python3 test_distribution.py`

## 📊 Performances

### Benchmarks Typiques
- **Nettoyage complet** : 2-5 minutes
- **Scan malware** : 30 secondes - 2 minutes
- **Surveillance heuristique** : Temps réel (< 1% CPU)
- **Profiling** : Impact négligeable (< 0.5% CPU)

### Espace Libérable
- **Caches système** : 100MB - 2GB
- **Logs anciens** : 50MB - 500MB  
- **Fichiers temporaires** : 20MB - 200MB
- **Node modules** : 500MB - 5GB (si développement)
- **Docker** : 1GB - 10GB (si utilisé)

---

## 🎉 Félicitations !

Vous disposez maintenant d'un nettoyeur Mac professionnel avec :
- ✅ **Interface moderne** et intuitive
- ✅ **Surveillance temps réel** des menaces
- ✅ **Profiling de performance** avancé
- ✅ **27 tests unitaires** validés
- ✅ **4 plugins** de nettoyage spécialisés
- ✅ **Protection iCloud** automatique
- ✅ **Notifications** système intégrées

**Profitez d'un Mac plus propre et plus rapide ! 🚀**