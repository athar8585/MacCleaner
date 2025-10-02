#!/usr/bin/env python3
"""
Intégration GitHub pour MacCleaner Pro
Synchronisation automatique avec votre repository GitHub
"""

import os
import subprocess
import json
import requests
from datetime import datetime

class GitHubIntegration:
    def __init__(self):
        self.project_dir = os.path.dirname(__file__)
        self.config_file = os.path.join(self.project_dir, '.github_config.json')
        self.config = self.load_config()
        
    def load_config(self):
        """Charger la configuration GitHub"""
        default_config = {
            'repository': '',
            'username': '',
            'token': '',
            'auto_sync': False,
            'sync_interval_hours': 24
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception:
                pass
                
        return default_config
        
    def save_config(self):
        """Sauvegarder la configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")
            
    def setup_github_repo(self, username, repo_name, token=None):
        """Configurer le repository GitHub"""
        self.config['username'] = username
        self.config['repository'] = repo_name
        if token:
            self.config['token'] = token
            
        self.save_config()
        
        # Configurer Git si pas déjà fait
        try:
            subprocess.run(['git', 'config', 'user.name', username], 
                         cwd=self.project_dir, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', f'{username}@users.noreply.github.com'], 
                         cwd=self.project_dir, capture_output=True)
        except Exception:
            pass
            
    def create_github_repo(self, repo_name, description="MacCleaner Pro - Nettoyeur Mac Intelligent", private=False):
        """Créer un nouveau repository sur GitHub"""
        if not self.config.get('token'):
            print("❌ Token GitHub requis pour créer un repository")
            return False
            
        url = "https://api.github.com/user/repos"
        headers = {
            'Authorization': f"token {self.config['token']}",
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'name': repo_name,
            'description': description,
            'private': private,
            'auto_init': False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                repo_info = response.json()
                print(f"✅ Repository créé: {repo_info['html_url']}")
                
                # Ajouter le remote origin
                self.add_remote_origin(repo_info['clone_url'])
                return True
            else:
                print(f"❌ Erreur création repository: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Erreur requête GitHub: {e}")
            return False
            
    def add_remote_origin(self, repo_url):
        """Ajouter le remote origin"""
        try:
            # Supprimer l'origin existant si présent
            subprocess.run(['git', 'remote', 'remove', 'origin'], 
                         cwd=self.project_dir, capture_output=True)
            
            # Ajouter le nouveau remote
            result = subprocess.run(['git', 'remote', 'add', 'origin', repo_url], 
                                  cwd=self.project_dir, capture_output=True)
            
            if result.returncode == 0:
                print(f"✅ Remote origin ajouté: {repo_url}")
                return True
            else:
                print(f"❌ Erreur ajout remote: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur remote: {e}")
            return False
            
    def push_to_github(self):
        """Pousser les changements vers GitHub"""
        try:
            # Push vers GitHub
            result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                                  cwd=self.project_dir, capture_output=True)
            
            if result.returncode == 0:
                print("✅ Code poussé vers GitHub avec succès")
                return True
            else:
                print(f"❌ Erreur push: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur push: {e}")
            return False
            
    def sync_with_github(self):
        """Synchroniser avec GitHub"""
        try:
            # Pull les derniers changements
            subprocess.run(['git', 'pull', 'origin', 'main'], 
                         cwd=self.project_dir, capture_output=True)
            
            # Vérifier s'il y a des changements à pousser
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.project_dir, capture_output=True, text=True)
            
            if result.stdout.strip():
                # Il y a des changements
                self.commit_and_push("🔄 Synchronisation automatique MacCleaner Pro")
                
            print("✅ Synchronisation GitHub terminée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur synchronisation: {e}")
            return False
            
    def commit_and_push(self, message="📝 Mise à jour MacCleaner Pro"):
        """Commit et push automatique"""
        try:
            # Add tous les fichiers
            subprocess.run(['git', 'add', '.'], cwd=self.project_dir)
            
            # Commit avec message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"{message}\n\nMise à jour automatique: {timestamp}"
            
            subprocess.run(['git', 'commit', '-m', full_message], 
                         cwd=self.project_dir, capture_output=True)
            
            # Push
            return self.push_to_github()
            
        except Exception as e:
            print(f"❌ Erreur commit/push: {e}")
            return False
            
    def setup_automatic_sync(self):
        """Configurer la synchronisation automatique"""
        # Créer un script de synchronisation
        sync_script = f"""#!/bin/bash
# Synchronisation automatique MacCleaner Pro

cd "{self.project_dir}"
python3 -c "
from github_integration import GitHubIntegration
gh = GitHubIntegration()
gh.sync_with_github()
"
"""
        
        sync_script_path = os.path.join(self.project_dir, 'auto_sync.sh')
        with open(sync_script_path, 'w') as f:
            f.write(sync_script)
            
        os.chmod(sync_script_path, 0o755)
        
        print(f"✅ Script de synchronisation créé: {sync_script_path}")
        print("💡 Ajoutez à votre crontab pour sync automatique:")
        print(f"0 */6 * * * {sync_script_path}")
        
    def get_repository_info(self):
        """Obtenir les informations du repository"""
        if not self.config.get('token') or not self.config.get('repository'):
            return None
            
        url = f"https://api.github.com/repos/{self.config['username']}/{self.config['repository']}"
        headers = {
            'Authorization': f"token {self.config['token']}",
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception:
            return None

def main():
    """Interface de configuration GitHub"""
    gh = GitHubIntegration()
    
    print("🐙 Configuration GitHub pour MacCleaner Pro")
    print("=" * 50)
    
    # Vérifier si déjà configuré
    if gh.config.get('repository'):
        print(f"Repository actuel: {gh.config['username']}/{gh.config['repository']}")
        
        choice = input("Voulez-vous reconfigurer ? (y/N): ").lower()
        if choice != 'y':
            return
            
    # Configuration
    username = input("Nom d'utilisateur GitHub: ").strip()
    repo_name = input("Nom du repository (ex: MacCleaner-Pro): ").strip()
    
    if not repo_name:
        repo_name = "MacCleaner-Pro"
        
    # Token optionnel pour création de repo
    print("\n💡 Token GitHub (optionnel, pour créer automatiquement le repo):")
    print("   Créez un token sur: https://github.com/settings/tokens")
    print("   Permissions requises: repo, user")
    token = input("Token (ou Enter pour ignorer): ").strip()
    
    # Configuration
    gh.setup_github_repo(username, repo_name, token)
    
    # Créer le repo si token fourni
    if token:
        create_repo = input("Créer le repository sur GitHub ? (Y/n): ").lower()
        if create_repo != 'n':
            private = input("Repository privé ? (y/N): ").lower() == 'y'
            if gh.create_github_repo(repo_name, private=private):
                print("🚀 Repository créé avec succès !")
            
    # Push initial
    if not token:
        print(f"\n📝 Créez manuellement le repository sur GitHub:")
        print(f"   https://github.com/new")
        print(f"   Nom: {repo_name}")
        
        input("Appuyez sur Enter une fois le repository créé...")
        
        repo_url = f"https://github.com/{username}/{repo_name}.git"
        gh.add_remote_origin(repo_url)
        
    # Push du code
    push_code = input("Pousser le code vers GitHub maintenant ? (Y/n): ").lower()
    if push_code != 'n':
        if gh.push_to_github():
            print("🎉 MacCleaner Pro est maintenant sur GitHub !")
            print(f"🔗 URL: https://github.com/{username}/{repo_name}")
            
    # Synchronisation automatique
    auto_sync = input("Configurer la synchronisation automatique ? (Y/n): ").lower()
    if auto_sync != 'n':
        gh.config['auto_sync'] = True
        gh.save_config()
        gh.setup_automatic_sync()
        
    print("\n✅ Configuration GitHub terminée !")
    print(f"🔗 Repository: https://github.com/{username}/{repo_name}")

if __name__ == "__main__":
    main()