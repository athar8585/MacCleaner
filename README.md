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

## 🛡️ Sécurité

- **Sauvegarde Automatique** : Création d'un backup avant nettoyage
- **Vérifications Sécurité** : Validation des chemins avant suppression
- **Logs Complets** : Traçabilité de toutes les opérations
- **Restauration** : Possibilité de restaurer les sauvegardes

## ⚡ Performances Attendues

### Espace Libéré (typique)
- **Léger** : 500MB - 2GB
- **Moyen** : 2GB - 5GB  
- **Lourd** : 5GB - 20GB+

### Améliorations
- ⚡ **Démarrage** : 20-40% plus rapide
- 🧠 **RAM** : 10-30% de mémoire libérée
- 💾 **Disque** : Accès plus rapide
- 🌐 **Réseau** : DNS plus réactif

## 🔍 Que Nettoie l'Application

### Dossiers Système
```
~/Library/Caches/              # Caches utilisateur
/Library/Caches/               # Caches système
/System/Library/Caches/        # Caches macOS
/var/folders/                  # Dossiers temporaires
/tmp/                          # Fichiers temporaires
/var/log/                      # Logs système
~/Library/Logs/                # Logs utilisateur
```

### Applications Spécifiques
```
Safari: LocalStorage, Databases, History
Chrome: Default/History, Cache
Firefox: Profiles/*/places.sqlite
Système: DiagnosticReports, CrashReporter
```

## ⚠️ Attention

- **Fermer les applications** avant nettoyage
- **Vérifier les téléchargements** importants
- **Sauvegarder** les données critiques
- **Redémarrer** après optimisations majeures

## 🆘 Dépannage

### Erreurs Communes
- **Permission refusée** → Relancer avec les droits admin
- **Fichier en cours d'utilisation** → Fermer l'application concernée
- **Espace insuffisant** → Libérer de l'espace manuellement d'abord

### Support
- Logs détaillés dans l'interface
- Sauvegardes dans `~/Desktop/MacCleaner_Backup/`
- Restauration possible via le bouton "↩️ Restaurer"

---

**⚡ MacCleaner Pro - Votre Mac comme neuf en un clic ! ⚡**