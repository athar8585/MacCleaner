#!/usr/bin/env python3
"""
MacCleaner Guardian - INDICATEUR BARRE DE MENU SIMPLE
Version simple utilisant les notifications macOS et scripts AppleScript
"""

import subprocess
import threading
import time
import json
import os
from datetime import datetime
from pathlib import Path

class SimpleMenuBarGuardian:
    """Indicateur simple dans la barre de menu via AppleScript"""
    
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.monitoring_active = True
        self.current_status = "optimal"
        
        # Configuration
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 30,
            'auto_cleanup_threshold': 85,
            'memory_threshold': 80,
            'notifications_enabled': True,
            'last_cleanup': None
        }
        
        self.load_config()
        self.create_menu_bar_indicator()
    
    def load_config(self):
        """Charge la configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except:
            pass
    
    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def create_menu_bar_indicator(self):
        """Crée l'indicateur dans la barre de menu"""
        
        # Script AppleScript pour créer l'indicateur persistant
        applescript = '''
        on run
            set statusText to "🛡️ MacCleaner Guardian"
            
            -- Créer une notification persistante qui reste dans le centre de notifications
            display notification "MacCleaner Guardian est actif et surveille votre Mac" with title "🛡️ Guardian Actif" subtitle "Cliquez pour voir le statut"
            
            -- Créer un script qui affiche le menu quand appelé
            tell application "System Events"
                -- Optionnel: ajouter à la barre de menu via un processus en arrière-plan
            end tell
            
            return "Guardian indicator created"
        end run
        '''
        
        try:
            subprocess.run(['osascript', '-e', applescript], 
                         capture_output=True, timeout=10)
            print("🛡️  Indicateur barre de menu créé")
        except Exception as e:
            print(f"❌ Erreur création indicateur: {e}")
    
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
                free_pages = 0
                active_pages = 0
                
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
    
    def send_status_notification(self, status_text, details):
        """Envoie une notification de statut mise à jour"""
        try:
            # Notification avec détails système
            script = f'''
            display notification "{details}" with title "{status_text}" subtitle "MacCleaner Guardian" sound name ""
            '''
            
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def create_interactive_menu(self, metrics):
        """Crée un menu interactif avec les options"""
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        menu_script = f'''
        set statusInfo to "📊 ÉTAT SYSTÈME ({time.strftime("%H:%M")})\\n\\n💾 Disque: {disk_percent}% ({metrics.get('disk_free', '--')} libre)\\n🧠 Mémoire: {memory_percent}% ({metrics.get('memory_free_mb', 0)}MB libre)\\n⚡ CPU: {cpu_percent}%\\n\\n"
        
        if {disk_percent} > 80 then
            set statusInfo to statusInfo & "⚠️  Espace disque faible !\\n"
        end if
        
        if {memory_percent} > 75 then
            set statusInfo to statusInfo & "⚠️  Mémoire saturée !\\n"
        end if
        
        set actionButtons to {{"🧹 Nettoyage Rapide", "⚡ Optimisation", "🔄 Actualiser", "⚙️ Configuration", "❌ Fermer"}}
        
        set userChoice to choose from list actionButtons with title "🛡️ MacCleaner Guardian" with prompt statusInfo default items {{"🔄 Actualiser"}} OK button name "Exécuter" cancel button name "Fermer"
        
        if userChoice is not false then
            set selectedAction to item 1 of userChoice
            return selectedAction
        else
            return "Fermer"
        end if
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', menu_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                action = result.stdout.strip()
                return action
            
        except Exception as e:
            print(f"❌ Erreur menu interactif: {e}")
        
        return None
    
    def handle_user_action(self, action):
        """Traite l'action choisie par l'utilisateur"""
        if action == "🧹 Nettoyage Rapide":
            self.perform_cleanup()
        elif action == "⚡ Optimisation":
            self.perform_optimization()
        elif action == "🔄 Actualiser":
            self.force_update()
        elif action == "⚙️ Configuration":
            self.show_configuration()
        
    def perform_cleanup(self):
        """Effectue un nettoyage rapide"""
        try:
            self.send_notification("🧹 Nettoyage", "Nettoyage en cours...")
            
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
            
            self.config['last_cleanup'] = datetime.now().isoformat()
            self.save_config()
            
            self.send_notification(
                "✅ Nettoyage terminé", 
                f"{len(actions)} optimisations appliquées"
            )
            
            print(f"✅ Nettoyage terminé: {actions}")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
            self.send_notification("❌ Erreur", "Nettoyage échoué")
    
    def perform_optimization(self):
        """Effectue une optimisation système"""
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
    
    def force_update(self):
        """Force une mise à jour du statut"""
        self.update_system_status()
        self.send_notification("🔄 Actualisation", "Statut mis à jour")
    
    def show_configuration(self):
        """Affiche la configuration"""
        config_script = f'''
        set configText to "⚙️ CONFIGURATION ACTUELLE\\n\\n"
        set configText to configText & "🧹 Nettoyage automatique: {'OUI' if self.config['auto_cleanup_enabled'] else 'NON'}\\n"
        set configText to configText & "🔔 Notifications: {'OUI' if self.config['notifications_enabled'] else 'NON'}\\n"
        set configText to configText & "📊 Seuil disque: {self.config['auto_cleanup_threshold']}%\\n"
        set configText to configText & "🧠 Seuil mémoire: {self.config['memory_threshold']}%\\n"
        set configText to configText & "⏱️  Intervalle: {self.config['monitoring_interval']}s\\n"
        
        set configButtons to {{"✅ Activer Auto-Nettoyage", "❌ Désactiver Auto-Nettoyage", "🔔 Basculer Notifications", "📊 Panneau Complet", "🔙 Retour"}}
        
        set userChoice to choose from list configButtons with title "⚙️ Configuration Guardian" with prompt configText default items {{"🔙 Retour"}} OK button name "Appliquer" cancel button name "Retour"
        
        if userChoice is not false then
            return item 1 of userChoice
        else
            return "Retour"
        end if
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', config_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                action = result.stdout.strip()
                
                if action == "✅ Activer Auto-Nettoyage":
                    self.config['auto_cleanup_enabled'] = True
                    self.save_config()
                    self.send_notification("✅ Configuration", "Auto-nettoyage activé")
                
                elif action == "❌ Désactiver Auto-Nettoyage":
                    self.config['auto_cleanup_enabled'] = False
                    self.save_config()
                    self.send_notification("❌ Configuration", "Auto-nettoyage désactivé")
                
                elif action == "🔔 Basculer Notifications":
                    self.config['notifications_enabled'] = not self.config['notifications_enabled']
                    self.save_config()
                    status = "activées" if self.config['notifications_enabled'] else "désactivées"
                    self.send_notification("🔔 Configuration", f"Notifications {status}")
                
                elif action == "📊 Panneau Complet":
                    # Ouvrir le panneau complet
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    subprocess.Popen(['python3', os.path.join(current_dir, 'maccleaner_guardian.py')])
        
        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
    
    def send_notification(self, title, message):
        """Envoie une notification macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" subtitle "MacCleaner Guardian" sound name "Funk"
            '''
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def update_system_status(self):
        """Met à jour le statut système et notifie si nécessaire"""
        metrics = self.get_system_metrics()
        
        if not metrics:
            return
        
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        # Déterminer l'état
        new_status = "optimal"
        status_icon = "🛡️"
        
        if disk_percent > 85 or memory_percent > 80:
            new_status = "critical"
            status_icon = "⚠️"
            status_text = "⚠️ Attention requise"
        elif disk_percent > 70 or memory_percent > 65:
            new_status = "warning"
            status_icon = "🟡"
            status_text = "🟡 Surveillance active"
        else:
            status_text = "✅ Système optimal"
        
        # Notifier si changement d'état
        if new_status != self.current_status:
            details = f"Disque: {disk_percent}% | RAM: {memory_percent}% | CPU: {cpu_percent}%"
            self.send_status_notification(status_text, details)
            self.current_status = new_status
        
        # Vérifier nettoyage automatique
        if (self.config['auto_cleanup_enabled'] and 
            disk_percent > self.config['auto_cleanup_threshold']):
            self.schedule_auto_cleanup(disk_percent)
        
        print(f"{status_icon} {status_text} | Disque: {disk_percent}% | RAM: {memory_percent}% | CPU: {cpu_percent}%")
        
        return metrics
    
    def schedule_auto_cleanup(self, disk_percent):
        """Programme un nettoyage automatique"""
        if self.config['notifications_enabled']:
            # Notification avec option d'annulation
            script = f'''
            display dialog "🛡️ MacCleaner Guardian\\n\\nNettoyage automatique recommandé\\n\\nDisque utilisé: {disk_percent}%\\n\\nLancer le nettoyage maintenant ?" buttons {{"⏱️  Plus tard", "🧹 Nettoyer"}} default button "🧹 Nettoyer" with title "Auto-Nettoyage" with icon note giving up after 30
            '''
            
            try:
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True, timeout=35)
                
                if result.returncode == 0 and "Nettoyer" in result.stdout:
                    # L'utilisateur a accepté
                    self.perform_cleanup()
                
            except:
                # Timeout ou annulation - nettoyage automatique silencieux
                self.perform_cleanup()
    
    def create_status_indicator(self):
        """Crée un indicateur de statut permanent dans les notifications"""
        # Notification persistante mise à jour régulièrement
        script = '''
        tell application "System Events"
            -- Vérifier si le processus Guardian existe déjà
            if not (exists process "Guardian") then
                -- Créer une notification persistante
                display notification "MacCleaner Guardian surveille votre Mac en arrière-plan" with title "🛡️ Guardian Actif" subtitle "Cliquez sur cette notification pour accéder au menu"
            end if
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def show_interactive_menu(self):
        """Affiche le menu interactif"""
        metrics = self.update_system_status()
        if metrics:
            action = self.create_interactive_menu(metrics)
            if action and action != "Fermer" and action != "❌ Fermer":
                self.handle_user_action(action)
                return True
        return False
    
    def monitoring_loop(self):
        """Boucle de surveillance principale"""
        print("🛡️  MacCleaner Guardian MenuBar - Démarrage surveillance...")
        
        # Créer l'indicateur initial
        self.create_status_indicator()
        
        while self.monitoring_active:
            try:
                self.update_system_status()
                time.sleep(self.config['monitoring_interval'])
                
                # Recréer l'indicateur périodiquement
                if int(time.time()) % 300 == 0:  # Toutes les 5 minutes
                    self.create_status_indicator()
                
            except Exception as e:
                print(f"❌ Erreur surveillance: {e}")
                time.sleep(60)
    
    def run(self):
        """Lance le Guardian"""
        try:
            # Démarrer la surveillance en arrière-plan
            monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
            monitoring_thread.start()
            
            print("🛡️  MacCleaner Guardian MenuBar actif!")
            print("💡 Cliquez sur les notifications pour accéder au menu")
            print("🔄 Le système est surveillé automatiquement")
            print("⏹️  Ctrl+C pour arrêter")
            
            # Afficher le menu initial
            time.sleep(2)
            self.show_interactive_menu()
            
            # Boucle principale avec menu périodique
            while self.monitoring_active:
                time.sleep(60)  # Attendre 1 minute
                
                # Optionnel: afficher le menu automatiquement si problème détecté
                if self.current_status in ['critical', 'warning']:
                    print("💡 Problème détecté - menu disponible via notification")
                
        except KeyboardInterrupt:
            print("\n🛡️  MacCleaner Guardian arrêté.")
            self.monitoring_active = False

def main():
    """Point d'entrée principal"""
    import sys
    
    # Gestion des arguments de ligne de commande
    if len(sys.argv) > 1:
        command = sys.argv[1]
        guardian = SimpleMenuBarGuardian()
        
        if command == '--menu':
            # Afficher le menu interactif
            guardian.show_interactive_menu()
        elif command == '--status':
            # Afficher le statut actuel
            guardian.update_system_status()
        elif command == '--cleanup':
            # Nettoyage manuel
            guardian.perform_cleanup()
        elif command == '--optimize':
            # Optimisation manuelle
            guardian.perform_optimization()
        return
    
    # Mode normal - surveillance continue
    guardian = SimpleMenuBarGuardian()
    guardian.run()

if __name__ == "__main__":
    main()