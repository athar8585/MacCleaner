# MacCleaner Pro - Instructions pour Agents IA

## Architecture du Projet

**MacCleaner Pro** est un utilitaire de nettoyage Mac avec deux interfaces principales :
- `mac_cleaner.py` : Interface graphique Python/Tkinter complète
- `quick_clean.sh` : Script shell pour nettoyage rapide en ligne de commande

### Structure des Composants
```
MacCleaner/
├── mac_cleaner.py          # Application principale GUI
├── quick_clean.sh          # Nettoyage rapide CLI  
├── run_cleaner.sh          # Lanceur avec env virtuel
├── create_app.sh           # Générateur d'app macOS
├── MacCleaner Pro.app/     # Application macOS native
└── venv/                   # Environnement Python isolé
```

## Workflows de Développement

### Lancement de l'Application
```bash
./run_cleaner.sh           # Interface graphique complète
./quick_clean.sh           # Nettoyage rapide terminal
open "MacCleaner Pro.app"  # Application macOS native
```

### Environnement Python
- **Toujours utiliser** `venv/` pour les dépendances
- **Activer avec** `source venv/bin/activate`
- **Dépendance critique** : `psutil` pour monitoring système

### Test et Debug
```bash
source venv/bin/activate
python -c "import psutil; print('RAM:', psutil.virtual_memory().percent, '%')"
```

## Conventions du Projet

### Gestion des Chemins de Nettoyage
Les chemins sont organisés par **catégories** dans `cleanup_paths` dict :
```python
'System Caches': ['~/Library/Caches', '/Library/Caches'],
'Browser Data': ['~/Library/Safari/History.db']
```

### Sécurité et Sauvegardes
- **Toujours créer backup** avant nettoyage (`create_backup()`)
- **Validation des chemins** avec `os.path.exists()` 
- **Logs détaillés** via `log_message()` pour traçabilité

### Threading Pattern
```python
# UI non-bloquante pour opérations longues
threading.Thread(target=self._cleaning_thread, daemon=True).start()
```

## Intégrations Système macOS

### Commandes sudo Critiques
```bash
sudo purge                    # Purge mémoire
sudo dscacheutil -flushcache  # Cache DNS  
sudo periodic daily           # Maintenance
```

### Permissions et Sécurité
- **Jamais lancer avec sudo** (vérification `os.geteuid()`)
- **Gérer les permissions refusées** gracieusement
- **Interface admin** pour optimisations avancées

### Monitoring Système Temps Réel
```python
psutil.virtual_memory()      # État RAM
psutil.disk_usage('/')       # Espace disque
psutil.cpu_percent()         # Charge CPU
```

## Patterns de Nettoyage Spécifiques

### Nettoyage Sécurisé
```python
# Vider dossier sans le supprimer
for item in os.listdir(path):
    if os.path.isfile(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)
```

### Calcul d'Espace Libéré
- **Mesurer avant/après** chaque opération
- **Affichage temps réel** de l'espace récupéré
- **Estimation préalable** par catégorie

### Gestion des Wildcards
```python
import glob
matching_paths = glob.glob(pattern)  # Support ~/Library/*/Caches
```

## Optimisations Avancées

### Services Système
- **Spotlight rebuild** : `sudo mdutil -E /`
- **Finder restart** : `killall Finder`
- **Permissions repair** : `diskutil resetUserPermissions`

### Performance UI
- **Progress bars** avec calcul précis des étapes
- **Logs en temps réel** sans bloquer l'interface
- **Estimation intelligente** des durées

## Fichiers de Configuration Clés

- `requirements.txt` : Dépendances Python minimales
- `Info.plist` : Métadonnées application macOS  
- `venv/` : Isolement des dépendances système

## Debugging et Troubleshooting

### Problèmes Fréquents
- **"externally-managed-environment"** → Utiliser `venv/`
- **Permission denied** → Vérifier droits sudo pour optimisations
- **tkinter import error** → Installer Python avec support GUI

### Logs et Monitoring
- Tous les nettoyages sont **tracés** avec timestamps
- **Sauvegardes automatiques** dans `~/Desktop/MacCleaner_Backup/`
- **Validation post-nettoyage** des chemins critiques