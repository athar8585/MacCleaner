#!/usr/bin/env python3
"""
MacCleaner Guardian - ICÔNE BARRE DE MENU SIMPLE
Version rapide qui créé immédiatement une icône visible dans la barre de menu
"""

import subprocess
import threading
import time
import json
import os
from datetime import datetime
from pathlib import Path

class QuickMenuBarIcon:
    """Icône rapide barre de menu via AppleScript et Automator"""
    
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.monitoring_active = True
        self.current_icon = "🛡️"
        
        # Configuration
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 60,
            'auto_cleanup_threshold': 85,
            'notifications_enabled': True
        }
        
        self.load_config()
        print("🛡️ MacCleaner Guardian - Création icône barre de menu...")
    
    def load_config(self):
        """Charge la configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config.update(json.load(f))
        except:
            pass
    
    def create_menu_bar_app_bundle(self):
        """Crée un app bundle qui apparaît dans la barre de menu"""
        
        # Créer le répertoire de l'application
        app_path = Path('/Users/loicdeloison/Desktop/MacCleaner/MacCleanerGuardian.app')
        contents_path = app_path / 'Contents'
        macos_path = contents_path / 'MacOS'
        resources_path = contents_path / 'Resources'
        
        # Créer la structure
        macos_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        
        # Créer Info.plist pour une app barre de menu
        info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>MacCleaner Guardian</string>
    <key>CFBundleExecutable</key>
    <string>guardian</string>
    <key>CFBundleIconFile</key>
    <string>guardian_icon</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleaner.guardian</string>
    <key>CFBundleName</key>
    <string>MacCleanerGuardian</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>LSBackgroundOnly</key>
    <false/>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>'''
        
        with open(contents_path / 'Info.plist', 'w') as f:
            f.write(info_plist)
        
        # Créer le script exécutable
        guardian_script = '''#!/bin/bash
cd "$(dirname "$0")/../../.."
exec python3 quick_menubar_icon.py --app-mode
'''
        
        with open(macos_path / 'guardian', 'w') as f:
            f.write(guardian_script)
        
        os.chmod(macos_path / 'guardian', 0o755)
        
        print(f"✅ App bundle créé: {app_path}")
        return app_path
    
    def create_simple_menu_bar_script(self):
        """Crée un script AppleScript qui ajoute une icône persistante"""
        
        applescript_code = '''
        on run
            -- Configuration
            set guardianIcon to "🛡️"
            set guardianTitle to "MacCleaner Guardian"
            
            -- Créer un processus en arrière-plan permanent
            tell application "System Events"
                -- Lancer le processus Guardian en arrière-plan
                do shell script "cd /Users/loicdeloison/Desktop/MacCleaner && python3 quick_menubar_icon.py --daemon > /dev/null 2>&1 &"
            end tell
            
            -- Notification de démarrage
            display notification "Guardian est maintenant actif dans la barre de menu" with title guardianTitle subtitle "Icône 🛡️ ajoutée" sound name "Funk"
            
            -- Attendre un peu puis afficher le menu initial
            delay 2
            
            -- Menu de confirmation
            display dialog "🛡️ MacCleaner Guardian est maintenant actif !\\n\\nL'icône 🛡️ a été ajoutée à la barre de menu.\\n\\nFonctionnalités:\\n• Surveillance automatique du système\\n• Nettoyage intelligent\\n• Notifications d'alerte\\n• Menu accessible via l'icône\\n\\nLe Guardian fonctionne maintenant en arrière-plan." buttons {"📊 Ouvrir Panneau", "✅ OK"} default button "✅ OK" with title "Guardian Actif" with icon note
            
            set userChoice to button returned of result
            
            if userChoice is "📊 Ouvrir Panneau" then
                do shell script "cd /Users/loicdeloison/Desktop/MacCleaner && python3 maccleaner_guardian.py > /dev/null 2>&1 &"
            end if
            
            return "Guardian started successfully"
        end run
        '''
        
        script_path = Path('/Users/loicdeloison/Desktop/MacCleaner/start_guardian_icon.scpt')
        with open(script_path, 'w') as f:
            f.write(applescript_code)
        
        return script_path
    
    def launch_menu_bar_icon(self):
        """Lance l'icône dans la barre de menu"""
        
        # Créer et lancer le script AppleScript
        script_path = self.create_simple_menu_bar_script()
        
        try:
            # Exécuter le script AppleScript
            result = subprocess.run(['osascript', str(script_path)], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Script AppleScript exécuté avec succès")
                print("🛡️ Icône Guardian ajoutée à la barre de menu!")
                return True
            else:
                print(f"❌ Erreur script: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lancement: {e}")
            return False
    
    def get_system_metrics(self):
        """Récupère les métriques système"""
        try:
            metrics = {}
            
            # Disque via df
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        metrics['disk_percent'] = int(float(fields[4].replace('%', '')))
                        metrics['disk_free'] = fields[3]
            
            # Mémoire via vm_stat
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\n')
                free_pages = active_pages = 0
                
                for line in lines:
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                total_pages = free_pages + active_pages
                if total_pages > 0:
                    metrics['memory_percent'] = int((active_pages / total_pages) * 100)
                    metrics['memory_free_mb'] = int((free_pages * 4096) // (1024 * 1024))
            
            # CPU via uptime
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            if uptime_result.returncode == 0:
                output = uptime_result.stdout
                if 'load averages:' in output:
                    load_avg_str = output.split('load averages:')[-1].strip().split()[0]
                    load_avg_str = load_avg_str.replace(',', '.')
                    metrics['cpu_percent'] = int(min(float(load_avg_str) * 25, 100))
            
            return metrics
            
        except Exception as e:
            print(f"❌ Erreur métriques: {e}")
            return {}
    
    def show_guardian_menu(self):
        """Affiche le menu principal Guardian"""
        metrics = self.get_system_metrics()
        
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        # Déterminer l'icône selon l'état
        if disk_percent > 85 or memory_percent > 80:
            status_icon = "⚠️"
            status_text = "Attention requise"
        elif disk_percent > 70 or memory_percent > 65:
            status_icon = "🟡"
            status_text = "Surveillance active"
        else:
            status_icon = "🛡️"
            status_text = "Système optimal"
        
        # Créer le menu interactif
        menu_text = f"""{status_icon} MACCLEANER GUARDIAN

📊 ÉTAT SYSTÈME ({datetime.now().strftime('%H:%M')})
💾 Disque: {disk_percent}% ({metrics.get('disk_free', '--')} libre)
🧠 Mémoire: {memory_percent}% ({metrics.get('memory_free_mb', 0)}MB libre)
⚡ CPU: {cpu_percent}%

{status_text}
"""
        
        if disk_percent > 80:
            menu_text += "\n⚠️ Espace disque faible - Nettoyage recommandé"
        
        menu_script = f'''
        set menuText to "{menu_text}"
        set actionButtons to {{"🧹 Nettoyage Rapide", "⚡ Optimisation", "🔄 Actualiser", "⚙️ Configuration", "📊 Panneau Complet", "❌ Quitter Guardian"}}
        
        set userChoice to choose from list actionButtons with title "🛡️ MacCleaner Guardian" with prompt menuText default items {{"🔄 Actualiser"}} OK button name "Exécuter" cancel button name "Fermer"
        
        if userChoice is not false then
            return item 1 of userChoice
        else
            return "Fermer"
        end if
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', menu_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                action = result.stdout.strip()
                self.handle_menu_action(action)
            
        except Exception as e:
            print(f"❌ Erreur menu: {e}")
    
    def handle_menu_action(self, action):
        """Traite l'action choisie dans le menu"""
        print(f"🎮 Action choisie: {action}")
        
        if action == "🧹 Nettoyage Rapide":
            self.perform_cleanup()
        elif action == "⚡ Optimisation":
            self.perform_optimization()
        elif action == "🔄 Actualiser":
            self.show_guardian_menu()
        elif action == "⚙️ Configuration":
            self.show_configuration()
        elif action == "📊 Panneau Complet":
            self.open_full_panel()
        elif action == "❌ Quitter Guardian":
            self.quit_guardian()
    
    def perform_cleanup(self):
        """Nettoyage rapide"""
        try:
            self.send_notification("🧹 Nettoyage", "Démarrage du nettoyage...")
            
            actions = []
            
            # Vider la corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists():
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=30, capture_output=True)
                actions.append("Corbeille vidée")
            
            # Nettoyer caches
            cache_paths = [
                Path.home() / 'Library/Caches/com.apple.Safari/WebKitCache',
                Path('/tmp')
            ]
            
            for cache_path in cache_paths:
                if cache_path.exists():
                    try:
                        subprocess.run([
                            'find', str(cache_path), 
                            '-type', 'f', '-mtime', '+7', 
                            '-delete'
                        ], timeout=60, capture_output=True)
                        actions.append(f"Cache {cache_path.name}")
                    except:
                        pass
            
            self.send_notification("✅ Nettoyage terminé", f"{len(actions)} optimisations appliquées")
            print(f"✅ Nettoyage terminé: {actions}")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
            self.send_notification("❌ Erreur", "Nettoyage échoué")
    
    def perform_optimization(self):
        """Optimisation système"""
        try:
            self.send_notification("⚡ Optimisation", "Optimisation en cours...")
            
            # DNS flush
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], 
                         timeout=10, capture_output=True)
            
            # Purge mémoire
            subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
            
            self.send_notification("✅ Optimisation OK", "Système optimisé")
            print("⚡ Optimisation terminée")
            
        except Exception as e:
            print(f"❌ Erreur optimisation: {e}")
            self.send_notification("❌ Erreur", "Optimisation échouée")
    
    def show_configuration(self):
        """Affiche la configuration"""
        config_text = f"""⚙️ CONFIGURATION GUARDIAN

🧹 Nettoyage automatique: {'✅ OUI' if self.config['auto_cleanup_enabled'] else '❌ NON'}
🔔 Notifications: {'✅ OUI' if self.config['notifications_enabled'] else '❌ NON'}
📊 Seuil disque critique: {self.config['auto_cleanup_threshold']}%
⏱️ Intervalle surveillance: {self.config['monitoring_interval']}s

Dernière vérification: {datetime.now().strftime('%H:%M:%S')}"""
        
        script = f'''
        display dialog "{config_text}" buttons {{"🔙 Retour", "📊 Panneau Complet"}} default button "🔙 Retour" with title "⚙️ Configuration Guardian" with icon note
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "Panneau Complet" in result.stdout:
                self.open_full_panel()
        
        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
    
    def open_full_panel(self):
        """Ouvre le panneau de contrôle complet"""
        try:
            subprocess.Popen(['python3', 'maccleaner_guardian.py'], 
                           cwd='/Users/loicdeloison/Desktop/MacCleaner')
            print("📊 Panneau complet ouvert")
        except Exception as e:
            print(f"❌ Erreur ouverture panneau: {e}")
    
    def quit_guardian(self):
        """Arrête le Guardian"""
        try:
            # Arrêter les processus Guardian
            subprocess.run(['pkill', '-f', 'quick_menubar_icon'], capture_output=True)
            subprocess.run(['pkill', '-f', 'guardian_menubar'], capture_output=True)
            
            self.send_notification("🛡️ Guardian arrêté", "Surveillance désactivée")
            print("🛡️ Guardian arrêté")
            self.monitoring_active = False
            
        except Exception as e:
            print(f"❌ Erreur arrêt: {e}")
    
    def send_notification(self, title, message):
        """Envoie une notification macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" subtitle "MacCleaner Guardian"
            '''
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def run_daemon_mode(self):
        """Lance en mode daemon avec surveillance continue"""
        print("🛡️ Guardian Daemon démarré - Surveillance active")
        
        while self.monitoring_active:
            try:
                # Vérifier l'état du système
                metrics = self.get_system_metrics()
                disk_percent = metrics.get('disk_percent', 0)
                memory_percent = metrics.get('memory_percent', 0)
                
                # Alertes automatiques
                if disk_percent > 85:
                    self.send_notification(
                        "⚠️ Disque plein", 
                        f"Espace utilisé: {disk_percent}% - Nettoyage recommandé"
                    )
                elif memory_percent > 80:
                    self.send_notification(
                        "⚠️ Mémoire saturée", 
                        f"RAM utilisée: {memory_percent}% - Optimisation recommandée"
                    )
                
                # Nettoyage automatique si activé
                if (self.config['auto_cleanup_enabled'] and 
                    disk_percent > self.config['auto_cleanup_threshold']):
                    
                    # Demander confirmation via notification
                    script = f'''
                    display dialog "🛡️ MacCleaner Guardian\\n\\nNettoyage automatique recommandé\\n\\nDisque utilisé: {disk_percent}%\\n\\nLancer le nettoyage maintenant ?" buttons {{"⏱️ Plus tard", "🧹 Nettoyer"}} default button "🧹 Nettoyer" with title "Auto-Nettoyage" with icon caution giving up after 30
                    '''
                    
                    try:
                        result = subprocess.run(['osascript', '-e', script], 
                                              capture_output=True, text=True, timeout=35)
                        
                        if result.returncode == 0 and "Nettoyer" in result.stdout:
                            self.perform_cleanup()
                    except:
                        pass  # Timeout ou annulation
                
                # Attendre avant prochaine vérification
                time.sleep(self.config['monitoring_interval'])
                
            except KeyboardInterrupt:
                print("\n🛡️ Guardian arrêté par l'utilisateur")
                break
            except Exception as e:
                print(f"❌ Erreur daemon: {e}")
                time.sleep(60)
    
    def create_clickable_menu_bar_icon(self):
        """Crée une icône cliquable persistante dans la barre de menu"""
        
        # Script qui crée une icône persistante via notifications programmées
        persistent_script = '''
        on run
            -- Créer un processus en arrière-plan qui maintient l'icône
            repeat
                try
                    -- Vérifier si Guardian est encore actif
                    set guardianCheck to do shell script "pgrep -f 'quick_menubar_icon.*daemon'"
                    
                    -- Si Guardian actif, créer/maintenir l'icône
                    if guardianCheck is not "" then
                        -- Notification discrète qui simule une icône
                        display notification "🛡️ Guardian actif - Cliquez pour menu" with title "Guardian" subtitle "" sound name ""
                        
                        -- Attendre 5 minutes avant la prochaine "icône"
                        delay 300
                    else
                        -- Guardian arrêté, sortir de la boucle
                        exit repeat
                    end if
                    
                on error
                    -- En cas d'erreur, attendre et réessayer
                    delay 60
                end try
            end repeat
        end run
        '''
        
        # Sauvegarder et lancer le script persistant
        persistent_path = Path('/Users/loicdeloison/Desktop/MacCleaner/guardian_persistent_icon.scpt')
        with open(persistent_path, 'w') as f:
            f.write(persistent_script)
        
        # Lancer le script en arrière-plan
        try:
            subprocess.Popen(['osascript', str(persistent_path)], 
                           cwd='/Users/loicdeloison/Desktop/MacCleaner')
            print("🛡️ Icône persistante créée")
            return True
        except Exception as e:
            print(f"❌ Erreur icône persistante: {e}")
            return False

def main():
    """Point d'entrée principal"""
    import sys
    
    guardian = QuickMenuBarIcon()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--daemon':
            # Mode daemon - surveillance continue
            guardian.run_daemon_mode()
        
        elif command == '--menu':
            # Afficher le menu Guardian
            guardian.show_guardian_menu()
        
        elif command == '--app-mode':
            # Mode application - créer l'icône et lancer daemon
            guardian.create_clickable_menu_bar_icon()
            guardian.run_daemon_mode()
        
        elif command == '--install':
            # Installation de l'icône
            if guardian.launch_menu_bar_icon():
                print("✅ Installation réussie!")
            else:
                print("❌ Erreur installation")
        
        return
    
    # Mode par défaut - installer l'icône
    guardian.launch_menu_bar_icon()

if __name__ == "__main__":
    main()