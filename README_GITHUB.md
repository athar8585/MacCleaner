# MacCleaner Pro 🧹

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](./tests/)
[![Version](https://img.shields.io/badge/version-3.5-blue.svg)](#)
[![macOS](https://img.shields.io/badge/macOS-10.12+-lightgrey.svg)](#)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](#)

**Nettoyeur Mac Ultra-Complet et Professionnel** avec surveillance temps réel, détection heuristique et profiling performance.

## 🚀 Installation Rapide

```bash
# Installation one-liner
curl -fsSL https://raw.githubusercontent.com/VOTRE_USERNAME/MacCleaner/main/install.sh | bash

# Ou manuel
git clone https://github.com/VOTRE_USERNAME/MacCleaner.git
cd MacCleaner
./run_cleaner.sh
```

## ✨ Fonctionnalités Principales

- 🔒 **Protection iCloud** : Détection et protection automatique
- 🧠 **Nettoyage Intelligent** : 10+ catégories avec analyse prédictive  
- 🛡️ **Scanner Anti-Malware** : Signatures + quarantaine automatique
- 🤖 **Automatisation** : Planificateur avec seuils intelligents
- 🔍 **Surveillance Heuristique** : Détection comportements suspects
- 📊 **Profiling Performance** : Métriques temps réel (CPU/RAM/disque)
- 🧩 **Système de Plugins** : Docker, Xcode, Homebrew, node_modules
- 📱 **Interface Native** : Style iOS moderne + notifications
- 🧪 **Tests Complets** : Framework unitaire + vérification intégrité

## 📊 Performance

Résultats typiques sur MacBook Pro 2023 :
- **Espace libéré** : 2-15 GB selon utilisation
- **Temps d'exécution** : 15-45 secondes  
- **RAM récupérée** : 500MB-2GB (purge forcée)
- **Fichiers traités** : 10k-100k selon caches

## 🛡️ Sécurité

- ✅ **Protection iCloud** : Aucun fichier cloud supprimé
- ✅ **Vérification intégrité** : Hash SHA-256 de 21 fichiers critiques
- ✅ **Mode dry-run** : Test complet sans suppression
- ✅ **Quarantaine malware** : Isolation fichiers suspects
- ✅ **Sauvegarde auto** : Avant chaque nettoyage

## 🔧 Utilisation

### Interface Graphique
```bash
./run_cleaner.sh
```

### Ligne de Commande
```bash
# Vérification intégrité
./verify_integrity.py

# Tests complets
./tests/run_tests.py

# Mode analyse seule
python3 mac_cleaner.py --dry-run

# Mode daemon
python3 mac_cleaner.py --daemon
```

## 🧩 Plugins Inclus

| Plugin | Description | Gain Typique |
|--------|-------------|--------------|
| **docker_cleanup** | `docker system prune` + mesure | 500MB-5GB |
| **xcode_cleanup** | DerivedData + Archives | 1-10GB |
| **homebrew_cleanup** | `brew cleanup -s` | 100-500MB |
| **node_modules_cleanup** | Dossiers anciens >30j | 500MB-2GB |

## 📈 Monitoring

### Profiling Temps Réel
- CPU utilisation avant/après
- Mémoire libérée (RAM + swap)  
- I/O disque (lectures/écritures)
- Processus actifs
- Export JSON automatique

### Détection Heuristique
- Surveillance processus CPU >80%
- Monitoring fichiers LaunchAgents/Daemons
- Patterns suspects (keylog, backdoor, etc.)
- Alertes temps réel + export

## 🧪 Tests & Qualité

```bash
# Tous les tests
./tests/run_tests.py

# Test spécifique
./tests/run_tests.py test_integrity

# Couverture
python3 -m pytest tests/ --cov=utils --cov=plugins
```

Framework inclut :
- Tests unitaires modules critiques
- Vérification intégrité (21 fichiers)
- Tests système plugins
- Simulation erreurs/pannes

## 📦 Build & Distribution

```bash
# App native macOS
./build_app.sh

# DMG distribution
./build_dmg.sh

# Signature + Release
./sign_and_release.sh

# Release GitHub
./release_github.sh v3.5.0
```

## 🤝 Contribution

1. Fork le projet
2. Créer branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add: AmazingFeature'`)
4. Tests (`./tests/run_tests.py`)
5. Push branche (`git push origin feature/AmazingFeature`)
6. Ouvrir Pull Request

## 📋 Roadmap

- [ ] Interface Menu Bar native (SwiftUI)
- [ ] Sync cloud config (GitHub Gist)
- [ ] Détection ML comportements anormaux  
- [ ] Plugin marketplace
- [ ] Support macOS Sequoia nouvelles APIs

## 📄 Licence

MIT License - voir [LICENSE](LICENSE) pour détails.

## 🙏 Remerciements

- Communauté macOS pour feedback
- Contributeurs plugins
- Apple pour HIG et APIs natives

---

**⭐ Star ce repo si MacCleaner Pro vous aide !**