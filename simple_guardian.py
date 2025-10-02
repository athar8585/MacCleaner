#!/usr/bin/env python3
"""
MacCleaner Guardian - NOTIFICATION SIMPLE BARRE DE MENU
Version minimaliste qui fonctionne à coup sûr
"""

import subprocess
import time
import threading
from datetime import datetime

class SimpleGuardianNotifier:
    """Guardian simple via notifications macOS"""
    
    def __init__(self):
        print("🛡️ MacCleaner Guardian - Notifications barre de menu")
        self.active = True
    
    def send_notification(self, title, message, subtitle="MacCleaner Guardian"):
        """Envoie une notification simple"""
        try:
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'
            ], timeout=3)
        except:
            pass
    
    def get_disk_usage(self):
        """Obtient l'usage disque simple"""
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        return int(fields[4].replace('%', ''))
            return 0
        except:
            return 0
    
    def show_simple_menu(self):
        """Menu simple et rapide"""
        disk_usage = self.get_disk_usage()
        
        # Menu ultra-simple sans variables complexes
        try:
            result = subprocess.run([
                'osascript', '-e',
                'choose from list {"🧹 Nettoyage Rapide", "📊 Voir Statut", "❌ Arrêter"} with title "🛡️ Guardian" with prompt "MacCleaner Guardian Menu" OK button name "Exécuter"'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                choice = result.stdout.strip()
                
                if "Nettoyage" in choice:
                    self.quick_clean()
                elif "Statut" in choice:
                    self.show_status()
                elif "Arrêter" in choice:
                    self.stop()
                    
        except Exception as e:
            print(f"❌ Erreur menu: {e}")
    
    def quick_clean(self):
        """Nettoyage rapide"""
        self.send_notification("🧹 Nettoyage", "Nettoyage en cours...")
        
        try:
            # Vider corbeille
            subprocess.run(['rm', '-rf', f'{Path.home()}/.Trash/*'], 
                         shell=True, timeout=10)
            
            # Notification succès
            self.send_notification("✅ Terminé", "Nettoyage effectué")
            print("✅ Nettoyage terminé")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
            self.send_notification("❌ Erreur", "Nettoyage échoué")
    
    def show_status(self):
        """Affiche le statut simple"""
        disk_usage = self.get_disk_usage()
        
        try:
            subprocess.run([
                'osascript', '-e',
                f'display dialog "🛡️ Guardian Actif\\n\\n💾 Disque: {disk_usage}%\\n🕒 {datetime.now().strftime("%H:%M")}\\n\\nSurveillance active" buttons {{"OK"}} with title "Statut Guardian"'
            ], timeout=10)
            
        except Exception as e:
            print(f"❌ Erreur statut: {e}")
    
    def stop(self):
        """Arrête le Guardian"""
        self.active = False
        self.send_notification("🛡️ Arrêt", "Guardian arrêté")
        print("🛡️ Guardian arrêté")
    
    def monitor_loop(self):
        """Boucle de surveillance simple"""
        print("🔍 Surveillance démarrée...")
        
        while self.active:
            try:
                disk_usage = self.get_disk_usage()
                
                # Alerte si disque plein
                if disk_usage > 85:
                    self.send_notification("⚠️ Disque plein", f"Espace utilisé: {disk_usage}%")
                
                # Notification de statut toutes les 5 minutes
                if int(time.time()) % 300 == 0:
                    icon = "⚠️" if disk_usage > 80 else "🟡" if disk_usage > 70 else "🛡️"
                    self.send_notification(f"{icon} Guardian", f"Surveillance active - Disque {disk_usage}%")
                
                time.sleep(60)  # Vérifier chaque minute
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erreur surveillance: {e}")
                time.sleep(60)
    
    def run_with_icon(self):
        """Lance avec simulation d'icône"""
        # Notification initiale
        self.send_notification("🛡️ Guardian", "Actif - Surveillance démarrée")
        
        # Démarrer surveillance en arrière-plan
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        print("🛡️ Guardian actif avec notifications!")
        print("💡 Pour le menu: python3 simple_guardian.py --menu")
        print("⏹️  Ctrl+C pour arrêter")
        
        try:
            while self.active:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

def main():
    import sys
    from pathlib import Path
    
    guardian = SimpleGuardianNotifier()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--menu':
            guardian.show_simple_menu()
        elif command == '--clean':
            guardian.quick_clean()
        elif command == '--status':
            guardian.show_status()
        elif command == '--monitor':
            guardian.run_with_icon()
        return
    
    # Mode par défaut
    guardian.run_with_icon()

if __name__ == "__main__":
    main()