# MacCleaner Pro 🧹

**Nettoyeur Mac Ultra-Complet et Professionnel**

## 🎯 Fonctionnalités

### Nettoyage Intelligent et Protégé
- **🔒 Protection iCloud** : Détection automatique et protection des fichiers synchronisés
- **📊 Mode Analyse** : Analyser sans supprimer pour évaluer l'impact
- **🧠 Détection Intelligente** : Reconnaissance des fichiers importants et récents
- **Caches Système** : Tous les caches macOS, applications, navigateurs
- **Fichiers Temporaires** : /tmp, /var/tmp, dossiers temporaires
- **Logs & Diagnostics** : Logs système, rapports de crash, diagnostics
- **Données Navigateur** : Historique, cookies, cache Safari/Chrome/Firefox
- **Downloads & Corbeille** : Ancien téléchargements, corbeille système
- **Fichiers Volumineux** : Détection automatique des gros fichiers

### Protection Avancée des Données
- **☁️ Fichiers iCloud** : Protection automatique des fichiers synchronisés
- **📁 Fichiers Importants** : Documents, images, vidéos, projets récents
- **⏰ Fichiers Récents** : Protection des fichiers modifiés récemment (7 jours)
- **🎯 Extensions Critiques** : .docx, .pdf, .jpg, .mp4, .py, etc.
- **📊 Analyse Détaillée** : Rapports complets avant nettoyage

### Optimisations Avancées
- **🚀 Purge Mémoire** : Libération forcée de la RAM
- **🔍 Reconstruction Spotlight** : Réindexation complète
- **🔧 Réparation Permissions** : Correction des droits d'accès
- **🌐 Cache DNS** : Vidage complet du cache réseau
- **🔄 Redémarrage Services** : Finder et services système
- **⚙️ Maintenance Système** : Scripts daily/weekly/monthly

### Interface Intelligente
- **☁️ Analyseur iCloud** : Détection et protection automatique des fichiers cloud
- **🔍 Mode Analyse Seule** : Prévisualisation sans suppression
- **📊 Rapports Détaillés** : Analyse complète avec export des résultats
- **Scanner Système** : Détection automatique des problèmes
- **Estimation Espace** : Calcul en temps réel de l'espace récupérable
- **Logs Détaillés** : Suivi complet des opérations
- **Sauvegarde Auto** : Protection des données importantes
- **Progression Visuelle** : Barres de progression et statistiques

## 🚀 Installation

### Méthode Ultra Rapide (one‑liner)
```bash
curl -fsSL https://raw.githubusercontent.com/VOTRE_USER/MacCleaner/main/install.sh | bash
```

### Méthode Manuelle
1. **Cloner ou télécharger** le projet
2. **Rendre exécutable** le script de lancement :
   ```bash
   chmod +x run_cleaner.sh
   ```
3. **Lancer** l'application :
   ```bash
   ./run_cleaner.sh
   ```
4. (Optionnel) Construire l'app .app :
   ```bash
   ./build_app.sh && open "dist/MacCleaner Pro.app"
   ```

## 📋 Prérequis

- **macOS 10.12+** (Sierra ou plus récent)
- **Python 3.6+** (installé par défaut sur macOS récents)
- **Permissions administrateur** (pour certaines optimisations)

## 🔧 Utilisation

### Démarrage Rapide
1. Lancer `./run_cleaner.sh`
2. Cliquer sur "☁️ Analyser iCloud" (recommandé)
3. Cliquer sur "🔍 Scanner le Système"
4. **Activer "🔒 Protéger les fichiers iCloud"** (par défaut)
5. Optionnel : Activer "🔍 Mode analyse seulement" pour tester
6. Sélectionner les options de nettoyage
7. Cliquer sur "🧹 Nettoyer Maintenant"

### Protection des Données
- ✅ **🔒 Protéger les fichiers iCloud** - FORTEMENT RECOMMANDÉ
- ✅ **🔍 Mode analyse seulement** - Pour tester sans risque
- ✅ **📊 Rapport détaillé** - Voir ce qui sera nettoyé

### Commandes Rapides
```bash
# Analyse iCloud seule
./analyze_icloud.sh

# Nettoyage express protégé
./quick_clean.sh

# Interface complète
./run_cleaner.sh
```

### Options Recommandées
- ✅ **System Caches** - Toujours activé
- ✅ **User Caches** - Recommandé
- ✅ **Logs & Diagnostics** - Sûr
- ⚠️ **Browser Data** - Attention (supprime historique)
- ✅ **Downloads & Trash** - Vérifier avant
- ✅ **System Temp** - Toujours sûr

### Optimisations Avancées
- ✅ **Purger la mémoire** - Recommandé
- ⚠️ **Reconstruire Spotlight** - Long (30min+)
- ✅ **Réparer permissions** - Recommandé
- ✅ **Vider cache DNS** - Sûr
- ⚠️ **Redémarrer Finder** - Ferme toutes les fenêtres
- ✅ **Scripts maintenance** - Recommandé

## 🛡️ Sécurité & Anti-Malware (v3.x)
- Scan signatures (hash + patterns) via `malware_scanner/`
- Quarantaine automatique (`malware_scanner/quarantine/`)
- Mise à jour distante (préparer URL dans `config/settings.json`)
- Bouton: "🛡️ Scan Malware"

## 🤖 Automatisation Intelligente
- Planificateur autonome (`scheduler/auto_runner.py`)
- Déclencheur selon seuils disque / RAM
- Bouton bascule: "🤖 Auto Nettoyage: ON/OFF"
- Mode auto enregistré en base (`database/mac_cleaner.db`)

## 🗄️ Base de Données & Statistiques
- Suivi des sessions de nettoyage (temps, espace libéré, catégories)
- Journalisation des détections malware
- Récap en barre de statut (sessions | espace total | malware)

## 🎨 Interface Style iOS 26
- Thème sombre inspiré SF Symbols & Human Interface Guidelines
- Accent dynamique (#007AFF)
- Layout modulaire (`ui/theme.py`)

## 📦 Structure Étendue
```
config/loader.py              # Chargement & fusion settings
config/settings.json          # Configuration utilisateur
malware_scanner/              # Scanner + signatures
scheduler/auto_runner.py      # Planification intelligente
ui/theme.py                   # Thème moderne
database/db.py                # SQLite + schema
logs/                         # (futur) logs persistants
updates/                      # Manifeste de mise à jour
```

## ☁️ Sauvegarde sur GitHub
1. Créer un dépôt: `MacCleanerPro`
2. Initialiser Git dans ce dossier:
```bash
git init
git remote add origin git@github.com:VOTRE_USER/MacCleanerPro.git
git add .
git commit -m "feat: initial release v3.0 with scheduler & malware scan"
git branch -M main
git push -u origin main
```
3. Mettre à jour `config/settings.json` (champs `update_url`, `database_url`).

## 🔄 Mises à Jour Distantes (Concept)
- Publier `updates/latest.json` sur GitHub avec:
```json
{
  "version": "3.1.0",
  "min_app": "3.0.0",
  "signatures_url": "https://raw.githubusercontent.com/VOTRE_USER/MacCleanerPro/main/malware_scanner/signatures_min.json"
}
```
- Ajouter futur code: vérifier version actuelle > proposer update.

## 🧪 Roadmap Proposée
| Version | Fonctionnalité | Détail | État |
|---------|----------------|--------|------|
| 3.1 | Mise à jour auto | Téléchargement signatures + manifest | FAIT |
| 3.2 | Tests unitaires | Framework pytest + CI/CD | FAIT |
| 3.3 | Profiling performance | Mesure CPU/disque avant/après | FAIT |
| 3.4 | Notifications améliorées | pync + types avancés | FAIT |
| 3.5 | Détection heuristique | Surveillance processus + fichiers | FAIT |
| 3.6 | Plugin System | Docker, Xcode, Homebrew, node_modules | FAIT |
| 3.7 | Intégrité & Hash | Manifest + vérification UI | FAIT |
| 3.8 | Menu Bar interface | SwiftUI/pyobjc app native | À FAIRE |
| 4.0 | Cloud Sync | Sync config & stats via Gist | À FAIRE |

## 🧪 Tests & Qualité (Nouveauté v3.2+)
Structure complète de tests unitaires avec couverture des modules critiques:

```bash
# Lancer tous les tests
./tests/run_tests.py

# Test spécifique
./tests/run_tests.py test_integrity.TestIntegrity.test_hash_file

# Vérification intégrité (standalone)
./verify_integrity.py
```

Tests inclus:
- `test_integrity.py` : Module de vérification d'intégrité
- `test_plugins.py` : Système de plugins et chargement dynamique
- `run_tests.py` : Runner unifié avec rapport détaillé

## 📊 Profiling Performance (Nouveauté v3.3+)
Mesure en temps réel des métriques système avant/après nettoyage:

Métriques collectées:
- **CPU** : Utilisation % + fréquence
- **Mémoire** : RAM libérée + pourcentage
- **Disque** : Espace libéré + I/O opérations
- **Processus** : Nombre de processus actifs
- **Réseau** : Activité bytes envoyés/reçus

Utilisation:
1. Cliquer "📊 Profiling" pour activer
2. Lancer nettoyage normal
3. Rapport détaillé automatique + export JSON

## 🔍 Détection Heuristique (Nouveauté v3.5+)
Surveillance intelligente de comportements suspects:

Surveillance:
- **Processus CPU** : Détection utilisation excessive (>80% pendant >30s)
- **Fichiers sensibles** : Monitoring `LaunchAgents`, `LaunchDaemons` 
- **Créations suspectes** : Fichiers .plist, .app, patterns suspects
- **Activité réseau** : Processus avec beaucoup de connexions

Utilisation:
1. Cliquer "🔍 Surveillance" pour démarrer monitoring
2. Alertes temps réel dans logs + notifications macOS
3. Export alertes vers JSON pour analyse

## 🔔 Notifications Avancées (Nouveauté v3.4+)
Système de notifications robuste avec support pync:

Types disponibles:
- **Simples** : Titre + message basique
- **Progression** : Avec pourcentage et stats
- **Complétion** : Résumé avec métriques (MB libérés, durée, etc.)
- **Alertes** : Warning/Error/Critical avec sons différenciés

Fallback automatique osascript → pync selon disponibilité.

Test: Bouton "🔔 Test Notifs" pour voir tous les types.

## 🧠 Idées Futures (Plus Avancé)
- Détection anomalies: baseline des profils CPU / I/O
- Gestion énergie: nettoyage déclenché sur secteur uniquement
- Mode silencieux horaire (ne pas lancer pendant meetings)
- Intégration Spotlight API pour indexer / exclure proprement
- Export PDF rapports
- Tableau de bord Web local (Flask) optionnel

## 🔐 Recommandations Sécurité
- Ne jamais exécuter tout le programme en root; utiliser sudo uniquement pour opérations ciblées
- Signature de code (script `sign_and_release.sh`)
- Hash manifest (`utils/integrity.py`) pour vérifier fichiers critiques
- Quarantaine séparée pour malware isolés

### Vérification d'Intégrité
Bouton UI: "Vérifier intégrité" calcule SHA-256 des fichiers critiques et alerte si différence.
Générer manifeste (exemple):
```bash
python -c "from utils.integrity import generate_manifest; generate_manifest(['mac_cleaner.py','config/settings.json','malware_scanner/signatures_min.json','plugins/plugin_loader.py'])"
```

## ✅ Qualité & Tests (Prochaines étapes)
- Tests unitaires: modules `scanner`, `db`, `scheduler`
- Mode dry-run global (--dry-run) pour script CLI
- Bench: mesure temps / catégorie + histogramme

## 🧪 Modes Spéciaux
- `--dry-run` : Aucune suppression (analyse + rapport)
- `--daemon` : Mode agent discret (tâches périodiques + auto + mini scan malware)

### Exemple
```bash
python mac_cleaner.py --dry-run
python mac_cleaner.py --daemon &
```

## ⚙️ LaunchAgent
- Installation / suppression via bouton "⚙️ Agent: ON/OFF"
- Fichier : `~/Library/LaunchAgents/com.maccleaner.pro.autorun.plist`

## 🔔 Notifications
- macOS Notification Center + son de confirmation
- Fin de nettoyage + nouvelle version

## 🔄 Mises à Jour (Manifest)
Fichier local: `updates/latest.json` (copier sur GitHub raw)
Boutons UI: Vérifier MAJ / MAJ Signatures / Vérifier intégrité

## 🧩 Plugins (Système d'Extension)
Répertoire: `plugins/`
Chargement dynamique via `plugin_loader.py` (pattern *_cleanup.py)

Plugins inclus :
- `docker_cleanup.py` : Prune complet + calcul espace libéré (avant/après)
- `xcode_cleanup.py` : Suppression DerivedData / Archives
- `homebrew_cleanup.py` : `brew cleanup -s` + mesure gain caches

Ajouter un plugin : créer `plugins/monplugin_cleanup.py` exposant `run(log)` retournant octets libérés.

## 📄 Rapports HTML & PDF
Après nettoyage ou sur clic "Rapport HTML" un fichier HTML détaillé est généré dans `exports/`.
Export PDF via bouton "Export PDF" (utilise `wkhtmltopdf` si dispo sinon conversion basique texte → PDF).

---
**MacCleaner Pro v3.0** – Automatisé, Sécurisé, Moderne.