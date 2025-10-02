#!/usr/bin/env python3
"""
MacCleaner Guardian - Version Stable
Version contrôlée sans spam de notifications
"""

import os
import sys
import time
import subprocess
import threading
import signal
import json
from datetime import datetime, timedelta

class GuardianStable:
    def __init__(self):
        self.running = False
        self.pid_file = "/tmp/guardian_stable.pid"
        self.last_notification = None
        self.notification_cooldown = 300  # 5 minutes entre les notifications
        self.monitoring_interval = 60  # Vérification toutes les minutes
        self.disk_threshold = 90  # Alerte si disque > 90%
        self.memory_threshold = 85  # Alerte si mémoire > 85%
        
    def write_pid_file(self):
        """Écrire le PID dans un fichier pour éviter les doublons"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except:
            pass
    
    def remove_pid_file(self):
        """Supprimer le fichier PID à l'arrêt"""
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except:
            pass
    
    def is_already_running(self):
        """Vérifier si Guardian est déjà en cours d'exécution"""
        if not os.path.exists(self.pid_file):
            return False
            
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Vérifier si le processus existe
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            # Le processus n'existe plus, supprimer le fichier PID
            self.remove_pid_file()
            return False
    
    def get_disk_usage(self):
        """Obtenir l'utilisation du disque principal"""
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    percentage = parts[4].replace('%', '')
                    return int(percentage)
        except:
            pass
        return 0
    
    def get_memory_usage(self):
        """Obtenir l'utilisation de la mémoire"""
        try:
            result = subprocess.run(['vm_stat'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            
            free_pages = 0
            inactive_pages = 0
            active_pages = 0
            wired_pages = 0
            
            for line in lines:
                if 'Pages free:' in line:
                    free_pages = int(line.split(':')[1].strip().replace('.', ''))
                elif 'Pages inactive:' in line:
                    inactive_pages = int(line.split(':')[1].strip().replace('.', ''))
                elif 'Pages active:' in line:
                    active_pages = int(line.split(':')[1].strip().replace('.', ''))
                elif 'Pages wired down:' in line:
                    wired_pages = int(line.split(':')[1].strip().replace('.', ''))
            
            total_pages = free_pages + inactive_pages + active_pages + wired_pages
            used_pages = total_pages - free_pages
            
            if total_pages > 0:
                return int((used_pages / total_pages) * 100)
        except:
            pass
        return 0
    
    def can_send_notification(self):
        """Vérifier si on peut envoyer une notification (cooldown)"""
        if self.last_notification is None:
            return True
        
        time_diff = datetime.now() - self.last_notification
        return time_diff.total_seconds() >= self.notification_cooldown
    
    def send_notification(self, title, message, urgent=False):
        """Envoyer une notification avec contrôle de fréquence"""
        if not urgent and not self.can_send_notification():
            return
        
        try:
            script = f'''
            tell application "System Events"
                display notification "{message}" with title "{title}" subtitle "MacCleaner Guardian"
            end tell
            '''
            subprocess.run(['osascript', '-e', script], timeout=5)
            self.last_notification = datetime.now()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Notification: {title} - {message}")
        except:
            pass
    
    def cleanup_temp_files(self):
        """Nettoyer les fichiers temporaires"""
        temp_dirs = ['/tmp', '/var/tmp', os.path.expanduser('~/Downloads')]
        cleaned = 0
        
        for temp_dir in temp_dirs:
            try:
                if not os.path.exists(temp_dir):
                    continue
                    
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            # Supprimer les fichiers temporaires de plus de 7 jours
                            if os.path.getmtime(file_path) < time.time() - (7 * 24 * 3600):
                                if file.startswith('.') or file.endswith('.tmp') or 'temp' in file.lower():
                                    os.remove(file_path)
                                    cleaned += 1
                        except:
                            continue
                        
                        # Limiter le nettoyage pour éviter de bloquer
                        if cleaned > 100:
                            break
                    if cleaned > 100:
                        break
            except:
                continue
        
        return cleaned
    
    def monitor_system(self):
        """Surveillance principale du système"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Guardian démarré - Surveillance active")
        
        # Notification de démarrage (une seule fois)
        self.send_notification("🛡️ Guardian", "Surveillance démarrée", urgent=True)
        
        while self.running:
            try:
                # Vérifier l'utilisation du disque
                disk_usage = self.get_disk_usage()
                if disk_usage >= self.disk_threshold:
                    self.send_notification("⚠️ Disque plein", f"Utilisation: {disk_usage}%")
                    # Auto-nettoyage
                    cleaned = self.cleanup_temp_files()
                    if cleaned > 0:
                        self.send_notification("🧹 Nettoyage", f"{cleaned} fichiers temporaires supprimés")
                
                # Vérifier l'utilisation de la mémoire
                memory_usage = self.get_memory_usage()
                if memory_usage >= self.memory_threshold:
                    self.send_notification("⚠️ Mémoire", f"Utilisation: {memory_usage}%")
                
                # Log de surveillance (discret)
                if disk_usage > 0 or memory_usage > 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Disque: {disk_usage}% | Mémoire: {memory_usage}%")
                
                # Attendre avant la prochaine vérification
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"Erreur de surveillance: {e}")
                time.sleep(30)  # Attendre avant de retenter
    
    def start_daemon(self):
        """Démarrer Guardian en mode daemon"""
        if self.is_already_running():
            print("Guardian est déjà en cours d'exécution")
            return False
        
        self.write_pid_file()
        self.running = True
        
        # Gérer les signaux d'arrêt proprement
        def signal_handler(signum, frame):
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Signal reçu, arrêt de Guardian...")
            self.stop_daemon()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            self.monitor_system()
        except Exception as e:
            print(f"Erreur Guardian: {e}")
        finally:
            self.stop_daemon()
        
        return True
    
    def stop_daemon(self):
        """Arrêter Guardian proprement"""
        self.running = False
        self.remove_pid_file()
        self.send_notification("🛡️ Guardian", "Surveillance arrêtée", urgent=True)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Guardian arrêté")
    
    def status(self):
        """Afficher le statut de Guardian"""
        if self.is_already_running():
            with open(self.pid_file, 'r') as f:
                pid = f.read().strip()
            print(f"✅ Guardian actif (PID: {pid})")
            
            # Afficher les métriques actuelles
            disk_usage = self.get_disk_usage()
            memory_usage = self.get_memory_usage()
            print(f"📊 Disque: {disk_usage}% | Mémoire: {memory_usage}%")
        else:
            print("❌ Guardian inactif")
    
    def show_menu(self):
        """Afficher le menu interactif"""
        print("\n🛡️ MacCleaner Guardian - Menu")
        print("1. Démarrer la surveillance")
        print("2. Arrêter la surveillance")
        print("3. Statut du système")
        print("4. Nettoyage manuel")
        print("5. Quitter")
        
        choice = input("\nChoisissez une option (1-5): ").strip()
        
        if choice == "1":
            if not self.is_already_running():
                print("Démarrage de Guardian...")
                threading.Thread(target=self.start_daemon, daemon=True).start()
                time.sleep(2)
                self.status()
            else:
                print("Guardian est déjà actif")
        
        elif choice == "2":
            if self.is_already_running():
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
                print("Guardian arrêté")
            else:
                print("Guardian n'est pas actif")
        
        elif choice == "3":
            self.status()
        
        elif choice == "4":
            print("Nettoyage en cours...")
            cleaned = self.cleanup_temp_files()
            print(f"✅ {cleaned} fichiers temporaires supprimés")
        
        elif choice == "5":
            return False
        
        return True

def main():
    guardian = GuardianStable()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daemon":
            guardian.start_daemon()
        elif sys.argv[1] == "--status":
            guardian.status()
        elif sys.argv[1] == "--stop":
            if guardian.is_already_running():
                with open(guardian.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
                print("Guardian arrêté")
            else:
                print("Guardian n'est pas actif")
        elif sys.argv[1] == "--menu":
            while guardian.show_menu():
                input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("Usage: python3 guardian_stable.py [--daemon|--status|--stop|--menu]")
    else:
        # Mode interactif par défaut
        while guardian.show_menu():
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()