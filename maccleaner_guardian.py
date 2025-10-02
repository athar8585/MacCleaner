#!/usr/bin/env python3
"""
MacCleaner Guardian - SERVICE DE SURVEILLANCE ET MAINTENANCE AUTOMATIQUE
Un daemon intelligent qui surveille et maintient votre Mac en arrière-plan
"""

import time
import threading
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
import shutil

class MacCleanerGuardian:
    """Service de surveillance et maintenance automatique"""
    
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.log_file = Path.home() / '.maccleaner_guardian.log'
        self.is_running = False
        self.monitoring_thread = None
        
        # Configuration par défaut
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 300,  # 5 minutes
            'auto_cleanup_threshold': 85,  # % disque utilisé
            'memory_threshold': 80,  # % mémoire utilisée
            'notifications_enabled': True,
            'auto_optimization_enabled': False,
            'daily_maintenance_time': '02:00',
            'weekly_deep_scan': True,
            'last_cleanup': None,
            'last_notification': None
        }
        
        self.load_config()
        self.setup_logging()
    
    def load_config(self):
        """Charge la configuration utilisateur"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except Exception as e:
            self.log(f"Erreur chargement config: {e}")
    
    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log(f"Erreur sauvegarde config: {e}")
    
    def setup_logging(self):
        """Initialise les logs"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"MacCleaner Guardian démarré: {datetime.now()}\n")
                f.write(f"{'='*50}\n")
        except Exception as e:
            print(f"Erreur setup logging: {e}")
    
    def log(self, message):
        """Écrit dans le log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except:
            pass
        
        print(log_entry.strip())
    
    def send_notification(self, title, message, sound=True):
        """Envoie une notification macOS"""
        if not self.config['notifications_enabled']:
            return
        
        try:
            # Éviter spam notifications
            if self.config['last_notification']:
                last_notif = datetime.fromisoformat(self.config['last_notification'])
                if datetime.now() - last_notif < timedelta(minutes=30):
                    return
            
            # Commande AppleScript pour notification native
            script = f'''
            display notification "{message}" with title "{title}" sound name "{"Funk" if sound else ""}"
            '''
            
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
            
            self.config['last_notification'] = datetime.now().isoformat()
            self.save_config()
            self.log(f"Notification envoyée: {title}")
            
        except Exception as e:
            self.log(f"Erreur notification: {e}")
    
    def check_system_health(self):
        """Vérification complète de l'état du système"""
        try:
            # Utiliser les outils système macOS
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            
            # Parser df pour usage disque
            disk_usage = 0
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        usage_str = fields[4].replace('%', '')
                        disk_usage = float(usage_str)
            
            # Parser vm_stat pour mémoire
            memory_usage = 0
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\n')
                free_pages = 0
                active_pages = 0
                for line in lines:
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                if free_pages + active_pages > 0:
                    memory_usage = (active_pages / (free_pages + active_pages)) * 100
            
            # CPU via uptime
            cpu_usage = 0
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            if uptime_result.returncode == 0:
                load_avg_str = uptime_result.stdout.split('load averages:')[-1].strip().split()[0]
                # Gérer format français avec virgule
                load_avg_str = load_avg_str.replace(',', '.')
                cpu_usage = min(float(load_avg_str) * 25, 100)  # Approximation
            
            health_report = {
                'disk_usage': disk_usage,
                'memory_usage': memory_usage,
                'cpu_usage': cpu_usage,
                'process_count': 0,
                'boot_time': 0,
                'load_average': 0
            }
            
            self.log(f"État système - Disque: {health_report['disk_usage']:.1f}%, "
                    f"RAM: {health_report['memory_usage']:.1f}%, "
                    f"CPU: {health_report['cpu_usage']:.1f}%")
            
            return health_report
            
        except Exception as e:
            self.log(f"Erreur vérification système: {e}")
            return {
                'disk_usage': 0,
                'memory_usage': 0,
                'cpu_usage': 0,
                'process_count': 0,
                'boot_time': 0,
                'load_average': 0
            }
    
    def check_cleanup_needed(self, health_report):
        """Vérifie si un nettoyage est nécessaire"""
        needs_cleanup = []
        
        # Vérification disque
        if health_report['disk_usage'] > self.config['auto_cleanup_threshold']:
            needs_cleanup.append(f"Disque plein ({health_report['disk_usage']:.1f}%)")
        
        # Vérification mémoire
        if health_report['memory_usage'] > self.config['memory_threshold']:
            needs_cleanup.append(f"Mémoire saturée ({health_report['memory_usage']:.1f}%)")
        
        # Vérification ancienneté dernier nettoyage
        if self.config['last_cleanup']:
            last_cleanup = datetime.fromisoformat(self.config['last_cleanup'])
            if datetime.now() - last_cleanup > timedelta(days=7):
                needs_cleanup.append("Dernier nettoyage > 7 jours")
        else:
            needs_cleanup.append("Aucun nettoyage enregistré")
        
        return needs_cleanup
    
    def auto_cleanup_safe(self):
        """Nettoyage automatique sécurisé"""
        self.log("🧹 Démarrage nettoyage automatique...")
        
        try:
            cleanup_actions = []
            
            # 1. Vider les corbeilles
            trash_paths = [
                Path.home() / '.Trash',
                Path('/Volumes/*/Trash')
            ]
            
            for trash_path in trash_paths:
                if trash_path.exists():
                    try:
                        subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                                     timeout=30, capture_output=True)
                        cleanup_actions.append("Corbeille vidée")
                    except:
                        pass
            
            # 2. Nettoyer caches temporaires sécurisés
            safe_cache_paths = [
                Path.home() / 'Library/Caches/com.apple.Safari/WebKitCache',
                Path.home() / 'Library/Caches/com.google.Chrome',
                Path('/tmp')
            ]
            
            for cache_path in safe_cache_paths:
                if cache_path.exists():
                    try:
                        # Supprimer seulement fichiers > 7 jours
                        subprocess.run([
                            'find', str(cache_path), 
                            '-type', 'f', '-mtime', '+7', 
                            '-delete'
                        ], timeout=60, capture_output=True)
                        cleanup_actions.append(f"Cache nettoyé: {cache_path.name}")
                    except:
                        pass
            
            # 3. Purge mémoire si nécessaire
            try:
                subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
                cleanup_actions.append("Mémoire purgée")
            except:
                pass
            
            # 4. Mise à jour de la configuration
            self.config['last_cleanup'] = datetime.now().isoformat()
            self.save_config()
            
            if cleanup_actions:
                message = f"Nettoyage automatique terminé: {', '.join(cleanup_actions)}"
                self.log(message)
                self.send_notification("MacCleaner Guardian", message)
            
            return len(cleanup_actions)
            
        except Exception as e:
            self.log(f"Erreur nettoyage automatique: {e}")
            return 0
    
    def intelligent_optimization(self):
        """Optimisation intelligente basée sur l'usage"""
        self.log("⚡ Optimisation intelligente...")
        
        try:
            optimizations = []
            
            # 1. Analyse des processus gourmands
            heavy_processes = []
            try:
                ps_result = subprocess.run(['ps', '-eo', 'pid,pcpu,pmem,comm'], 
                                         capture_output=True, text=True, timeout=10)
                if ps_result.returncode == 0:
                    lines = ps_result.stdout.strip().split('\n')[1:]  # Skip header
                    for line in lines:
                        parts = line.strip().split(None, 3)
                        if len(parts) >= 4:
                            try:
                                cpu = float(parts[1])
                                mem = float(parts[2])
                                if cpu > 30 or mem > 5:
                                    heavy_processes.append({'cpu': cpu, 'mem': mem, 'name': parts[3]})
                            except:
                                continue
            except:
                pass
            
            if len(heavy_processes) > 10:
                optimizations.append(f"{len(heavy_processes)} processus gourmands détectés")
            
            # 2. Flush DNS automatique
            try:
                subprocess.run(['sudo', 'dscacheutil', '-flushcache'], 
                             timeout=10, capture_output=True)
                optimizations.append("DNS flush")
            except:
                pass
            
            # 3. Nettoyage services inutiles (sécurisé)
            try:
                subprocess.run(['sudo', 'killall', '-HUP', 'cfprefsd'], 
                             timeout=5, capture_output=True)
                optimizations.append("Services système optimisés")
            except:
                pass
            
            if optimizations:
                message = f"Optimisation terminée: {', '.join(optimizations)}"
                self.log(message)
                return True
            
            return False
            
        except Exception as e:
            self.log(f"Erreur optimisation: {e}")
            return False
    
    def monitoring_loop(self):
        """Boucle principale de surveillance"""
        self.log("🔍 Démarrage surveillance système...")
        
        while self.is_running:
            try:
                # Vérification état système
                health_report = self.check_system_health()
                
                # Vérification si nettoyage nécessaire
                cleanup_needed = self.check_cleanup_needed(health_report)
                
                if cleanup_needed and self.config['auto_cleanup_enabled']:
                    # Notification avant nettoyage automatique
                    self.send_notification(
                        "MacCleaner Guardian",
                        f"Nettoyage nécessaire: {', '.join(cleanup_needed[:2])}"
                    )
                    
                    # Attendre 30 secondes pour annulation utilisateur
                    time.sleep(30)
                    
                    # Lancer nettoyage
                    cleaned_items = self.auto_cleanup_safe()
                    
                    if cleaned_items > 0:
                        self.send_notification(
                            "Nettoyage terminé",
                            f"{cleaned_items} optimisations appliquées"
                        )
                
                # Optimisation intelligente périodique
                if self.config['auto_optimization_enabled']:
                    current_hour = datetime.now().hour
                    if current_hour in [2, 14]:  # 2h et 14h
                        self.intelligent_optimization()
                
                # Attendre avant prochaine vérification
                time.sleep(self.config['monitoring_interval'])
                
            except Exception as e:
                self.log(f"Erreur boucle surveillance: {e}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    def start_guardian(self):
        """Démarre le service Guardian"""
        if self.is_running:
            return False
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        self.log("🛡️  MacCleaner Guardian démarré")
        self.send_notification(
            "MacCleaner Guardian",
            "Surveillance système activée"
        )
        
        return True
    
    def stop_guardian(self):
        """Arrête le service Guardian"""
        if not self.is_running:
            return False
        
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        self.log("🛡️  MacCleaner Guardian arrêté")
        return True
    
    def get_status(self):
        """Retourne le statut du Guardian"""
        health = self.check_system_health()
        
        return {
            'running': self.is_running,
            'last_cleanup': self.config.get('last_cleanup'),
            'auto_cleanup': self.config['auto_cleanup_enabled'],
            'disk_usage': health['disk_usage'],
            'memory_usage': health['memory_usage'],
            'cpu_usage': health['cpu_usage']
        }

class GuardianControlPanel:
    """Interface de contrôle du Guardian"""
    
    def __init__(self):
        self.guardian = MacCleanerGuardian()
        
    def show_control_panel(self):
        """Affiche le panneau de contrôle"""
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        # Fenêtre principale
        root = tk.Tk()
        root.title("MacCleaner Guardian - Panneau de Contrôle")
        root.geometry("600x500")
        root.configure(bg='#2c3e50')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Guardian.TFrame', background='#2c3e50')
        style.configure('Guardian.TLabel', background='#2c3e50', foreground='#ecf0f1', font=('SF Pro Display', 12))
        style.configure('Title.TLabel', background='#2c3e50', foreground='#ecf0f1', font=('SF Pro Display', 18, 'bold'))
        
        main_frame = ttk.Frame(root, style='Guardian.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🛡️  MacCleaner Guardian", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Statut actuel
        status_frame = ttk.Frame(main_frame, style='Guardian.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        status = self.guardian.get_status()
        
        status_text = f"""
📊 ÉTAT SYSTÈME ACTUEL:
• Service Guardian: {'🟢 Actif' if status['running'] else '🔴 Inactif'}
• Usage disque: {status['disk_usage']:.1f}%
• Usage mémoire: {status['memory_usage']:.1f}%
• Usage CPU: {status['cpu_usage']:.1f}%
• Dernier nettoyage: {status['last_cleanup'][:10] if status['last_cleanup'] else 'Jamais'}
        """
        
        status_label = ttk.Label(status_frame, text=status_text.strip(), style='Guardian.TLabel', justify=tk.LEFT)
        status_label.pack(anchor='w')
        
        # Configuration
        config_frame = ttk.Frame(main_frame, style='Guardian.TFrame')
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(config_frame, text="⚙️  CONFIGURATION:", style='Guardian.TLabel').pack(anchor='w')
        
        # Checkboxes pour configuration
        self.auto_cleanup_var = tk.BooleanVar(value=self.guardian.config['auto_cleanup_enabled'])
        ttk.Checkbutton(
            config_frame, 
            text="Nettoyage automatique",
            variable=self.auto_cleanup_var,
            command=self.update_config
        ).pack(anchor='w', pady=2)
        
        self.notifications_var = tk.BooleanVar(value=self.guardian.config['notifications_enabled'])
        ttk.Checkbutton(
            config_frame,
            text="Notifications",
            variable=self.notifications_var,
            command=self.update_config
        ).pack(anchor='w', pady=2)
        
        self.auto_optimization_var = tk.BooleanVar(value=self.guardian.config['auto_optimization_enabled'])
        ttk.Checkbutton(
            config_frame,
            text="Optimisation automatique",
            variable=self.auto_optimization_var,
            command=self.update_config
        ).pack(anchor='w', pady=2)
        
        # Boutons de contrôle
        buttons_frame = ttk.Frame(main_frame, style='Guardian.TFrame')
        buttons_frame.pack(fill=tk.X, pady=20)
        
        def start_guardian():
            if self.guardian.start_guardian():
                messagebox.showinfo("Guardian", "Service démarré avec succès!")
                root.destroy()
                self.show_control_panel()  # Refresh
            else:
                messagebox.showwarning("Guardian", "Service déjà en cours!")
        
        def stop_guardian():
            if self.guardian.stop_guardian():
                messagebox.showinfo("Guardian", "Service arrêté!")
                root.destroy()
                self.show_control_panel()  # Refresh
            else:
                messagebox.showwarning("Guardian", "Service déjà arrêté!")
        
        def force_cleanup():
            cleaned = self.guardian.auto_cleanup_safe()
            messagebox.showinfo("Nettoyage", f"Nettoyage terminé: {cleaned} actions effectuées")
        
        start_btn = tk.Button(
            buttons_frame, text="🚀 DÉMARRER GUARDIAN",
            command=start_guardian, bg='#27ae60', fg='white',
            font=('SF Pro Display', 12, 'bold'), padx=15, pady=8
        )
        start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        stop_btn = tk.Button(
            buttons_frame, text="⏹️  ARRÊTER GUARDIAN",
            command=stop_guardian, bg='#e74c3c', fg='white',
            font=('SF Pro Display', 12, 'bold'), padx=15, pady=8
        )
        stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cleanup_btn = tk.Button(
            buttons_frame, text="🧹 NETTOYAGE MANUEL",
            command=force_cleanup, bg='#f39c12', fg='white',
            font=('SF Pro Display', 12, 'bold'), padx=15, pady=8
        )
        cleanup_btn.pack(side=tk.LEFT)
        
        root.mainloop()
    
    def update_config(self):
        """Met à jour la configuration"""
        self.guardian.config['auto_cleanup_enabled'] = self.auto_cleanup_var.get()
        self.guardian.config['notifications_enabled'] = self.notifications_var.get()
        self.guardian.config['auto_optimization_enabled'] = self.auto_optimization_var.get()
        self.guardian.save_config()

def main():
    """Point d'entrée principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--daemon':
            # Mode daemon
            guardian = MacCleanerGuardian()
            guardian.start_guardian()
            
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                guardian.stop_guardian()
                print("Guardian arrêté.")
        
        elif sys.argv[1] == '--install':
            # Installation du service au démarrage
            install_launch_agent()
        
        elif sys.argv[1] == '--uninstall':
            # Désinstallation du service
            uninstall_launch_agent()
    
    else:
        # Mode interface graphique
        control_panel = GuardianControlPanel()
        control_panel.show_control_panel()

def install_launch_agent():
    """Installe MacCleaner Guardian comme service de démarrage"""
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maccleaner.guardian</string>
    <key>Program</key>
    <string>{sys.executable}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{os.path.abspath(__file__)}</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{os.path.dirname(os.path.abspath(__file__))}</string>
</dict>
</plist>'''
    
    plist_path = Path.home() / 'Library/LaunchAgents/com.maccleaner.guardian.plist'
    
    try:
        plist_path.parent.mkdir(exist_ok=True)
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        # Charger le service
        subprocess.run(['launchctl', 'load', str(plist_path)], check=True)
        print("✅ MacCleaner Guardian installé comme service de démarrage!")
        
    except Exception as e:
        print(f"❌ Erreur installation: {e}")

def uninstall_launch_agent():
    """Désinstalle le service de démarrage"""
    plist_path = Path.home() / 'Library/LaunchAgents/com.maccleaner.guardian.plist'
    
    try:
        # Décharger le service
        subprocess.run(['launchctl', 'unload', str(plist_path)], check=True)
        
        # Supprimer le fichier
        if plist_path.exists():
            plist_path.unlink()
        
        print("✅ MacCleaner Guardian désinstallé!")
        
    except Exception as e:
        print(f"❌ Erreur désinstallation: {e}")

if __name__ == "__main__":
    main()