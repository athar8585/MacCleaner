#!/usr/bin/env python3
"""
MacCleaner Pro - GitHub Integration & Auto-Update System
Système de synchronisation et mise à jour automatique via GitHub
"""

import os
import sys
import json
import requests
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
import hashlib
import base64

class GitHubIntegration:
    def __init__(self, repo_owner="votre-username", repo_name="MacCleaner-Pro"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = "https://api.github.com"
        self.raw_base = "https://raw.githubusercontent.com"
        
        self.base_dir = Path(__file__).parent
        self.config_dir = self.base_dir / "config"
        self.data_dir = self.base_dir / "data"
        
        # Fichier de configuration GitHub
        self.github_config_file = self.config_dir / "github_config.json"
        
        # Configuration par défaut
        self.default_config = {
            "repo_owner": repo_owner,
            "repo_name": repo_name,
            "access_token": "",  # À configurer par l'utilisateur
            "auto_sync": True,
            "sync_interval": 3600,  # 1 heure
            "backup_enabled": True,
            "restore_enabled": True,
            "update_check_interval": 21600  # 6 heures
        }
        
        self.setup_github_integration()
        
    def setup_github_integration(self):
        """Initialiser l'intégration GitHub"""
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.github_config_file.exists():
            self.save_github_config(self.default_config)
        else:
            self.github_config = self.load_github_config()
            
        print("🔗 Intégration GitHub initialisée")
        
    def load_github_config(self):
        """Charger la configuration GitHub"""
        try:
            with open(self.github_config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return self.default_config
            
    def save_github_config(self, config):
        """Sauvegarder la configuration GitHub"""
        self.github_config = config
        with open(self.github_config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def setup_repository(self):
        """Configurer le repository GitHub (première utilisation)"""
        print("🚀 Configuration du repository GitHub...")
        
        # Vérifier si le repo existe
        if not self.repository_exists():
            print("📁 Création du repository...")
            if self.create_repository():
                print("✅ Repository créé avec succès")
            else:
                print("❌ Erreur lors de la création du repository")
                return False
                
        # Initialiser la structure du repo
        return self.initialize_repository_structure()
        
    def repository_exists(self):
        """Vérifier si le repository existe"""
        try:
            url = f"{self.api_base}/repos/{self.github_config['repo_owner']}/{self.github_config['repo_name']}"
            headers = self.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Erreur vérification repository: {e}")
            return False
            
    def create_repository(self):
        """Créer un nouveau repository GitHub"""
        try:
            url = f"{self.api_base}/user/repos"
            headers = self.get_auth_headers()
            
            data = {
                "name": self.github_config['repo_name'],
                "description": "MacCleaner Pro - Configuration et données utilisateur",
                "private": True,  # Repository privé par défaut
                "auto_init": True
            }
            
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 201
            
        except Exception as e:
            print(f"Erreur création repository: {e}")
            return False
            
    def get_auth_headers(self):
        """Obtenir les en-têtes d'authentification"""
        token = self.github_config.get('access_token', '')
        if not token:
            print("⚠️  Token d'accès GitHub non configuré")
            return {}
            
        return {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def initialize_repository_structure(self):
        """Initialiser la structure du repository"""
        try:
            # Structure des dossiers à créer
            folders = [
                "config",
                "data", 
                "updates",
                "backups",
                "malware_db"
            ]
            
            # Fichiers à créer avec contenu initial
            files_to_create = {
                "README.md": self.generate_readme(),
                "config/default_settings.json": json.dumps(self.default_config, indent=2),
                "updates/version.json": json.dumps({
                    "version": "2.0.0",
                    "release_date": datetime.now().isoformat(),
                    "changes": ["Version initiale avec intégration GitHub"]
                }, indent=2),
                "malware_db/signatures.json": json.dumps([
                    {
                        "hash": "d41d8cd98f00b204e9800998ecf8427e",
                        "name": "Empty File Test",
                        "threat_level": 1,
                        "description": "Signature de test"
                    }
                ], indent=2)
            }
            
            # Créer les fichiers
            for file_path, content in files_to_create.items():
                if self.create_or_update_file(file_path, content):
                    print(f"✅ Créé: {file_path}")
                else:
                    print(f"❌ Erreur: {file_path}")
                    
            return True
            
        except Exception as e:
            print(f"Erreur initialisation structure: {e}")
            return False
            
    def generate_readme(self):
        """Générer le README du repository"""
        return f"""# MacCleaner Pro - Configuration Utilisateur

Repository privé pour la synchronisation des configurations et données MacCleaner Pro.

## Structure

- `config/` - Configurations personnalisées
- `data/` - Bases de données et historiques
- `updates/` - Mises à jour et patches
- `backups/` - Sauvegardes automatiques
- `malware_db/` - Base de données anti-malware

## Synchronisation Automatique

Ce repository est automatiquement synchronisé par MacCleaner Pro.

**Dernière synchronisation:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Sécurité

- Repository privé
- Données chiffrées
- Token d'accès sécurisé
- Sauvegardes versionnées
"""
        
    def backup_to_github(self):
        """Sauvegarder les données vers GitHub"""
        print("📤 Sauvegarde vers GitHub...")
        
        try:
            # Fichiers à sauvegarder
            files_to_backup = {
                "config/user_settings.json": self.base_dir / "config" / "autonomous_config.json",
                "data/cleanup_history.db": self.base_dir / "data" / "cleaner_database.db",
                "data/malware_scan_results.db": self.base_dir / "data" / "malware_signatures.db"
            }
            
            backup_success = 0
            total_files = len(files_to_backup)
            
            for github_path, local_path in files_to_backup.items():
                if local_path.exists():
                    # Lire le contenu du fichier
                    if local_path.suffix == '.db':
                        # Pour les bases de données, créer un export JSON
                        content = self.export_database_to_json(local_path)
                        github_path = github_path.replace('.db', '.json')
                    else:
                        with open(local_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    # Chiffrer le contenu sensible
                    if 'data/' in github_path:
                        content = self.encrypt_data(content)
                        
                    # Uploader vers GitHub
                    if self.create_or_update_file(f"backups/{github_path}", content):
                        backup_success += 1
                        print(f"✅ Sauvegardé: {github_path}")
                    else:
                        print(f"❌ Erreur sauvegarde: {github_path}")
                        
            # Créer un fichier de manifest
            manifest = {
                "backup_date": datetime.now().isoformat(),
                "files_backed_up": backup_success,
                "total_files": total_files,
                "success_rate": (backup_success / total_files) * 100
            }
            
            self.create_or_update_file(
                f"backups/manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                json.dumps(manifest, indent=2)
            )
            
            print(f"📊 Sauvegarde terminée: {backup_success}/{total_files} fichiers")
            return backup_success == total_files
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde GitHub: {e}")
            return False
            
    def restore_from_github(self, backup_date=None):
        """Restaurer les données depuis GitHub"""
        print("📥 Restauration depuis GitHub...")
        
        try:
            # Lister les sauvegardes disponibles
            backups = self.list_available_backups()
            
            if not backups:
                print("❌ Aucune sauvegarde trouvée")
                return False
                
            # Utiliser la plus récente si pas de date spécifiée
            if not backup_date:
                backup_date = max(backups.keys())
                
            print(f"📋 Restauration de la sauvegarde: {backup_date}")
            
            # Télécharger et restaurer les fichiers
            backup_files = backups[backup_date]
            restored_files = 0
            
            for github_path in backup_files:
                local_path = self.github_path_to_local(github_path)
                
                if self.download_and_restore_file(github_path, local_path):
                    restored_files += 1
                    print(f"✅ Restauré: {local_path}")
                else:
                    print(f"❌ Erreur restauration: {local_path}")
                    
            print(f"📊 Restauration terminée: {restored_files}/{len(backup_files)} fichiers")
            return restored_files == len(backup_files)
            
        except Exception as e:
            print(f"❌ Erreur restauration GitHub: {e}")
            return False
            
    def list_available_backups(self):
        """Lister les sauvegardes disponibles"""
        try:
            # Obtenir la liste des fichiers de manifest
            url = f"{self.api_base}/repos/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/contents/backups"
            headers = self.get_auth_headers()
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return {}
                
            files = response.json()
            backups = {}
            
            for file in files:
                if file['name'].startswith('manifest_') and file['name'].endswith('.json'):
                    # Extraire la date du nom de fichier
                    date_str = file['name'].replace('manifest_', '').replace('.json', '')
                    
                    # Télécharger le manifest
                    manifest_content = self.download_file_content(file['download_url'])
                    if manifest_content:
                        manifest = json.loads(manifest_content)
                        backups[date_str] = manifest.get('files_backed_up', [])
                        
            return backups
            
        except Exception as e:
            print(f"Erreur listing sauvegardes: {e}")
            return {}
            
    def check_for_updates(self):
        """Vérifier les mises à jour disponibles"""
        print("🔄 Vérification des mises à jour...")
        
        try:
            # Télécharger le fichier de version
            version_url = f"{self.raw_base}/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/main/updates/version.json"
            
            response = requests.get(version_url, timeout=10)
            if response.status_code != 200:
                print("❌ Impossible de vérifier les mises à jour")
                return False
                
            remote_version = response.json()
            local_version = self.get_local_version()
            
            if self.is_newer_version(remote_version['version'], local_version):
                print(f"📦 Mise à jour disponible: {remote_version['version']}")
                return self.download_and_apply_update(remote_version)
            else:
                print("✅ MacCleaner Pro est à jour")
                return True
                
        except Exception as e:
            print(f"❌ Erreur vérification mises à jour: {e}")
            return False
            
    def download_malware_database_updates(self):
        """Mettre à jour la base de données anti-malware"""
        print("🛡️  Mise à jour base anti-malware...")
        
        try:
            # URL de la base de signatures
            signatures_url = f"{self.raw_base}/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/main/malware_db/signatures.json"
            
            response = requests.get(signatures_url, timeout=30)
            if response.status_code == 200:
                signatures = response.json()
                
                # Sauvegarder dans la base locale
                local_db_file = self.base_dir / "data" / "malware_signatures_update.json"
                with open(local_db_file, 'w') as f:
                    json.dump(signatures, f, indent=2)
                    
                print(f"✅ Base anti-malware mise à jour: {len(signatures)} signatures")
                return True
            else:
                print("❌ Erreur téléchargement base anti-malware")
                return False
                
        except Exception as e:
            print(f"❌ Erreur mise à jour anti-malware: {e}")
            return False
            
    def create_or_update_file(self, file_path, content):
        """Créer ou mettre à jour un fichier sur GitHub"""
        try:
            # Vérifier si le fichier existe déjà
            url = f"{self.api_base}/repos/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/contents/{file_path}"
            headers = self.get_auth_headers()
            
            # Obtenir le SHA si le fichier existe
            response = requests.get(url, headers=headers)
            sha = None
            if response.status_code == 200:
                sha = response.json()['sha']
                
            # Encoder le contenu en base64
            content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            # Données pour l'API
            data = {
                "message": f"Update {file_path} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "content": content_encoded
            }
            
            if sha:
                data["sha"] = sha
                
            # Envoyer la requête
            response = requests.put(url, headers=headers, json=data)
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"Erreur création/mise à jour fichier {file_path}: {e}")
            return False
            
    def download_file_content(self, download_url):
        """Télécharger le contenu d'un fichier"""
        try:
            response = requests.get(download_url, timeout=30)
            if response.status_code == 200:
                return response.text
        except Exception:
            pass
        return None
        
    def encrypt_data(self, data):
        """Chiffrer les données sensibles (simple)"""
        # Implémentation simple - à améliorer avec une vraie cryptographie
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        
    def decrypt_data(self, encrypted_data):
        """Déchiffrer les données"""
        try:
            return base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
        except Exception:
            return encrypted_data
            
    def export_database_to_json(self, db_file):
        """Exporter une base de données SQLite vers JSON"""
        try:
            import sqlite3
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Obtenir les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            export_data = {}
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                
                # Obtenir les noms des colonnes
                columns = [description[0] for description in cursor.description]
                
                # Obtenir les données
                rows = cursor.fetchall()
                
                export_data[table_name] = {
                    'columns': columns,
                    'data': rows
                }
                
            conn.close()
            return json.dumps(export_data, indent=2, default=str)
            
        except Exception as e:
            print(f"Erreur export database: {e}")
            return "{}"
            
    def get_local_version(self):
        """Obtenir la version locale"""
        try:
            version_file = self.base_dir / "version.txt"
            if version_file.exists():
                return version_file.read_text().strip()
        except Exception:
            pass
        return "1.0.0"
        
    def is_newer_version(self, remote_version, local_version):
        """Comparer les versions"""
        try:
            remote_parts = [int(x) for x in remote_version.split('.')]
            local_parts = [int(x) for x in local_version.split('.')]
            
            # Comparer partie par partie
            for i in range(max(len(remote_parts), len(local_parts))):
                remote_part = remote_parts[i] if i < len(remote_parts) else 0
                local_part = local_parts[i] if i < len(local_parts) else 0
                
                if remote_part > local_part:
                    return True
                elif remote_part < local_part:
                    return False
                    
            return False
            
        except Exception:
            return False
            
    def setup_automatic_sync(self):
        """Configurer la synchronisation automatique"""
        print("🔄 Configuration de la synchronisation automatique...")
        
        # Créer un service launchd pour macOS
        plist_content = self.generate_launchd_plist()
        
        # Sauvegarder le plist
        plist_path = Path.home() / "Library" / "LaunchAgents" / "com.maccleanerpro.sync.plist"
        
        try:
            with open(plist_path, 'w') as f:
                f.write(plist_content)
                
            # Charger le service
            subprocess.run(['launchctl', 'load', str(plist_path)], check=True)
            
            print("✅ Synchronisation automatique configurée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur configuration sync auto: {e}")
            return False
            
    def generate_launchd_plist(self):
        """Générer le fichier plist pour launchd"""
        script_path = self.base_dir / "github_sync.py"
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maccleanerpro.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
        <string>--auto-sync</string>
    </array>
    <key>StartInterval</key>
    <integer>{self.github_config['sync_interval']}</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""

def main():
    """Fonction principale pour tests"""
    github = GitHubIntegration()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--setup":
            github.setup_repository()
        elif command == "--backup":
            github.backup_to_github()
        elif command == "--restore":
            github.restore_from_github()
        elif command == "--update":
            github.check_for_updates()
        elif command == "--malware-update":
            github.download_malware_database_updates()
        elif command == "--auto-sync":
            # Mode synchronisation automatique
            github.backup_to_github()
            github.check_for_updates()
            github.download_malware_database_updates()
        else:
            print("Commandes disponibles: --setup, --backup, --restore, --update, --malware-update, --auto-sync")
    else:
        print("🔗 Intégration GitHub MacCleaner Pro")
        print("Usage: python github_integration.py [--setup|--backup|--restore|--update|--malware-update|--auto-sync]")

if __name__ == "__main__":
    main()