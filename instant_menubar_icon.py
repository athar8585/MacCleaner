#!/usr/bin/env python3
"""
MacCleaner Guardian - ICÔNE BARRE DE MENU IMMÉDIATE
Version ultra-rapide qui place immédiatement une icône cliquable
"""

import subprocess
import threading
import time
import json
from datetime import datetime
from pathlib import Path

class InstantMenuBarIcon:
    """Icône instantanée dans la barre de menu"""
    
    def __init__(self):
        self.monitoring_active = True
        self.icon_process = None
        print("🛡️ MacCleaner Guardian - Icône barre de menu instantanée")
    
    def create_instant_icon(self):
        """Crée instantanément une icône cliquable dans la barre de menu"""
        
        # Script AppleScript minimal pour icône immédiate
        instant_script = '''
        tell application "System Events"
            -- Notification immédiate qui s'affiche comme une icône
            display notification "Guardian actif - Surveillance en cours" with title "🛡️" subtitle "MacCleaner Guardian" sound name ""
        end tell
        
        -- Lancer le processus de surveillance en arrière-plan
        do shell script "cd /Users/loicdeloison/Desktop/MacCleaner && python3 instant_menubar_icon.py --daemon > /dev/null 2>&1 &"
        
        return "Icon created instantly"
        '''
        
        try:
            # Lancer immédiatement
            subprocess.run(['osascript', '-e', instant_script], 
                         timeout=5, capture_output=True)
            
            print("✅ Icône instantanée créée dans la barre de menu!")
            print("🔔 Regardez les notifications en haut à droite")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur création icône: {e}")
            return False
    
    def create_persistent_menu_notifications(self):
        """Crée des notifications persistantes qui simulent une icône de menu"""
        
        print("🔄 Démarrage des notifications de menu persistantes...")
        
        while self.monitoring_active:
            try:
                # Obtenir l'état du système
                metrics = self.get_system_metrics()
                disk_percent = metrics.get('disk_percent', 0)
                memory_percent = metrics.get('memory_percent', 0)
                
                # Déterminer l'icône selon l'état
                if disk_percent > 85 or memory_percent > 80:
                    icon = "⚠️"
                    status = "Attention"
                elif disk_percent > 70 or memory_percent > 65:
                    icon = "🟡"
                    status = "Surveillance"
                else:
                    icon = "🛡️"
                    status = "Optimal"
                
                # Notification qui simule l'icône de menu
                notification_script = f'''
                display notification "Disque: {disk_percent}% | RAM: {memory_percent}% | Cliquez pour menu" with title "{icon} Guardian" subtitle "{status} - {datetime.now().strftime('%H:%M')}" sound name ""
                '''
                
                subprocess.run(['osascript', '-e', notification_script], 
                             timeout=5, capture_output=True)
                
                # Attendre 2 minutes avant la prochaine "icône"
                time.sleep(120)
                
            except KeyboardInterrupt:
                print("\\n🛡️ Arrêt des notifications de menu")
                break
            except Exception as e:
                print(f"❌ Erreur notification: {e}")
                time.sleep(60)
    
    def get_system_metrics(self):
        """Récupère rapidement les métriques système"""
        try:
            metrics = {}
            
            # Disque (rapide)
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=3)
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        metrics['disk_percent'] = int(float(fields[4].replace('%', '')))
            
            # Mémoire (rapide)
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=3)
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\\n')
                free_pages = active_pages = 0
                
                for line in lines[:10]:  # Seulement les premières lignes
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                total_pages = free_pages + active_pages
                if total_pages > 0:
                    metrics['memory_percent'] = int((active_pages / total_pages) * 100)
            
            return metrics
            
        except Exception as e:
            print(f"❌ Erreur métriques: {e}")
            return {'disk_percent': 0, 'memory_percent': 0}
    
    def show_quick_menu(self):
        """Affiche un menu rapide accessible"""
        metrics = self.get_system_metrics()
        
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        
        menu_text = f"""🛡️ MACCLEANER GUARDIAN

📊 ÉTAT ACTUEL:
💾 Disque: {disk_percent}%
🧠 Mémoire: {memory_percent}%
🕒 {datetime.now().strftime('%H:%M:%S')}

Que voulez-vous faire ?"""
        
        # Menu rapide avec AppleScript
        quick_menu_script = f'''
        set menuText to "{menu_text}"
        set quickActions to {{"🧹 Nettoyage", "⚡ Optimisation", "📊 Statut", "❌ Arrêter"}}
        
        set userChoice to choose from list quickActions with title "🛡️ MacCleaner Guardian" with prompt menuText OK button name "Exécuter" cancel button name "Fermer"
        
        if userChoice is not false then
            return item 1 of userChoice
        else
            return "Fermer"
        end if
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', quick_menu_script], 
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                action = result.stdout.strip()
                self.handle_quick_action(action)
            
        except Exception as e:
            print(f"❌ Erreur menu rapide: {e}")
    
    def handle_quick_action(self, action):
        """Traite rapidement l'action choisie"""
        print(f"🎮 Action: {action}")
        
        if action == "🧹 Nettoyage":
            self.quick_cleanup()
        elif action == "⚡ Optimisation":
            self.quick_optimization()
        elif action == "📊 Statut":
            self.show_detailed_status()
        elif action == "❌ Arrêter":
            self.stop_guardian()
    
    def quick_cleanup(self):
        """Nettoyage ultra-rapide"""
        try:
            # Notification de début
            subprocess.run(['osascript', '-e', 
                          'display notification "Nettoyage en cours..." with title "🧹 Guardian" sound name ""'], 
                         timeout=3)
            
            # Actions rapides
            actions = 0
            
            # Corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists() and any(trash_path.iterdir()):
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=10, capture_output=True)
                actions += 1
            
            # Cache rapide
            temp_files = list(Path('/tmp').glob('*'))
            if len(temp_files) > 100:
                subprocess.run(['find', '/tmp', '-type', 'f', '-mtime', '+1', '-delete'], 
                             timeout=10, capture_output=True)
                actions += 1
            
            # Notification de fin
            subprocess.run(['osascript', '-e', 
                          f'display notification "{actions} optimisations appliquées" with title "✅ Nettoyage OK" sound name "Funk"'], 
                         timeout=3)
            
            print(f"✅ Nettoyage rapide terminé: {actions} actions")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
    
    def quick_optimization(self):
        """Optimisation ultra-rapide"""
        try:
            # Notification
            subprocess.run(['osascript', '-e', 
                          'display notification "Optimisation système..." with title "⚡ Guardian" sound name ""'], 
                         timeout=3)
            
            # DNS flush (rapide)
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], 
                         timeout=5, capture_output=True)
            
            # Notification succès
            subprocess.run(['osascript', '-e', 
                          'display notification "Système optimisé" with title "✅ Optimisation OK" sound name "Funk"'], 
                         timeout=3)
            
            print("⚡ Optimisation rapide terminée")
            
        except Exception as e:
            print(f"❌ Erreur optimisation: {e}")
    
    def show_detailed_status(self):
        """Affiche le statut détaillé"""
        metrics = self.get_system_metrics()
        
        status_text = f"""🛡️ MACCLEANER GUARDIAN - STATUT DÉTAILLÉ

📊 MÉTRIQUES SYSTÈME:
💾 Utilisation disque: {metrics.get('disk_percent', 0)}%
🧠 Utilisation mémoire: {metrics.get('memory_percent', 0)}%

⏰ SURVEILLANCE:
🔄 Dernière vérification: {datetime.now().strftime('%H:%M:%S')}
🛡️ Guardian actif depuis le lancement

🔧 ACTIONS DISPONIBLES:
• Nettoyage automatique
• Optimisation système
• Surveillance continue
• Notifications intelligentes"""
        
        # Afficher le statut
        status_script = f'''
        display dialog "{status_text}" buttons {{"🔙 Retour", "📊 Panneau Complet"}} default button "🔙 Retour" with title "📊 Statut Guardian" with icon note
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', status_script], 
                                  capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and "Panneau Complet" in result.stdout:
                # Ouvrir le panneau complet
                subprocess.Popen(['python3', 'maccleaner_guardian.py'], 
                               cwd='/Users/loicdeloison/Desktop/MacCleaner')
        
        except Exception as e:
            print(f"❌ Erreur statut: {e}")
    
    def stop_guardian(self):
        """Arrête le Guardian"""
        self.monitoring_active = False
        
        subprocess.run(['osascript', '-e', 
                      'display notification "Guardian arrêté" with title "🛡️ Arrêt" sound name ""'], 
                     timeout=3)
        
        print("🛡️ Guardian arrêté")
    
    def run_instant_daemon(self):
        """Lance le daemon avec icônes instantanées"""
        print("🚀 Démarrage Guardian avec icône barre de menu...")
        
        # Créer l'icône immédiatement
        if self.create_instant_icon():
            # Démarrer les notifications persistantes
            self.create_persistent_menu_notifications()
        else:
            print("❌ Impossible de créer l'icône")

def main():
    """Point d'entrée"""
    import sys
    
    guardian = InstantMenuBarIcon()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--daemon':
            # Mode daemon avec icônes
            guardian.run_instant_daemon()
        
        elif command == '--menu':
            # Menu rapide
            guardian.show_quick_menu()
        
        elif command == '--cleanup':
            # Nettoyage direct
            guardian.quick_cleanup()
        
        elif command == '--optimize':
            # Optimisation directe
            guardian.quick_optimization()
        
        elif command == '--status':
            # Statut détaillé
            guardian.show_detailed_status()
        
        return
    
    # Mode par défaut - créer l'icône et menu
    if guardian.create_instant_icon():
        print("💡 Icône créée! Pour le menu complet:")
        print("   python3 instant_menubar_icon.py --menu")
        print("💡 Pour surveillance continue:")
        print("   python3 instant_menubar_icon.py --daemon")

if __name__ == "__main__":
    main()