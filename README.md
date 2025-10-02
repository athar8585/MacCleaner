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

1. **Cloner ou télécharger** le projet
2. **Rendre exécutable** le script de lancement :
   ```bash
   chmod +x run_cleaner.sh
   ```
3. **Lancer** l'application :
   ```bash
   ./run_cleaner.sh
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

## 🛡️ Sécurité & Anti-Malware (Nouveau v3.0)
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
| Version | Fonctionnalité | Détail |
|---------|----------------|--------|
| 3.1 | Mise à jour auto | Téléchargement signatures + manifest |
| 3.2 | Sandboxing | Exécution isolée scans risqués |
| 3.3 | Analyse heuristique | Détection comportements CPU / réseau anormaux |
| 3.4 | Interface SwiftUI | App .app native complète (menu bar) |
| 3.5 | Notif Centre | Intégration native macOS notifications |
| 3.6 | Plugin System | Ajout modules (ex: Docker prune, Xcode cache) |
| 4.0 | Cloud Sync | Sync config & stats via GitHub Gist |

## 🧠 Idées Futures (Plus Avancé)
- Détection anomalies: baseline des profils CPU / I/O
- Gestion énergie: nettoyage déclenché sur secteur uniquement
- Mode silencieux horaire (ne pas lancer pendant meetings)
- Intégration Spotlight API pour indexer / exclure proprement
- Export PDF rapports
- Tableau de bord Web local (Flask) optionnel

## 🔐 Recommandations Sécurité
- Ne jamais exécuter tout le programme en root; utiliser sudo uniquement pour opérations ciblées
- Ajouter signature de code (codesign) pour distribution
- Ajouter hash manifest pour vérifier intégrité MAJ

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
Boutons UI: Vérifier MAJ / MAJ Signatures

---
**MacCleaner Pro v3.0** – Automatisé, Sécurisé, Moderne.