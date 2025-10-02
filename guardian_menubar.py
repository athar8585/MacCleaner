#!/usr/bin/env python3
"""
MacCleaner Guardian - INDICATEUR BARRE DE MENU
Icône discrète dans la barre de menu macOS avec surveillance système
"""

import rumps
import subprocess
import threading
import time
from datetime import datetime
import os
import json
from pathlib import Path

class MacCleanerMenuBar(rumps.App):
    """Application barre de menu pour MacCleaner Guardian"""
    
    def __init__(self):
        # Icône principale dans la barre de menu
        super(MacCleanerMenuBar, self).__init__(
            name="MacCleaner Guardian",
            title="🛡️",  # Icône par défaut
            quit_button=None  # Pas de bouton quitter par défaut
        )
        
        # Configuration
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.log_file = Path.home() / '.maccleaner_guardian.log'
        self.monitoring_active = True
        self.last_metrics = {}
        
        # Charger configuration
        self.load_config()
        
        # Configurer le menu
        self.setup_menu()
        
        # Démarrer surveillance
        self.start_monitoring()
    
    def load_config(self):
        """Charge la configuration"""
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 30,  # 30 secondes
            'auto_cleanup_threshold': 85,
            'memory_threshold': 80,
            'notifications_enabled': True,
            'last_cleanup': None
        }
        
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
    
    def setup_menu(self):
        """Configure le menu déroulant"""
        # Statut système
        self.status_item = rumps.MenuItem("📊 Analyse en cours...", callback=None)
        self.menu.add(self.status_item)
        
        # Séparateur
        self.menu.add(rumps.separator)
        
        # Métriques détaillées
        self.disk_item = rumps.MenuItem("💾 Disque: --", callback=None)
        self.memory_item = rumps.MenuItem("🧠 Mémoire: --", callback=None)
        self.cpu_item = rumps.MenuItem("⚡ CPU: --", callback=None)
        
        self.menu.add(self.disk_item)
        self.menu.add(self.memory_item)
        self.menu.add(self.cpu_item)
        
        # Séparateur
        self.menu.add(rumps.separator)
        
        # Actions rapides
        self.menu.add(rumps.MenuItem("🧹 Nettoyage Rapide", callback=self.quick_cleanup))
        self.menu.add(rumps.MenuItem("⚡ Optimisation", callback=self.quick_optimization))
        self.menu.add(rumps.MenuItem("🔄 Actualiser", callback=self.force_update))
        
        # Séparateur
        self.menu.add(rumps.separator)
        
        # Configuration
        self.auto_cleanup_toggle = rumps.MenuItem(
            "✅ Nettoyage Automatique" if self.config['auto_cleanup_enabled'] else "❌ Nettoyage Automatique",
            callback=self.toggle_auto_cleanup
        )
        self.menu.add(self.auto_cleanup_toggle)
        
        self.notifications_toggle = rumps.MenuItem(
            "🔔 Notifications" if self.config['notifications_enabled'] else "🔕 Notifications",
            callback=self.toggle_notifications
        )
        self.menu.add(self.notifications_toggle)
        
        # Séparateur
        self.menu.add(rumps.separator)
        
        # Informations
        self.menu.add(rumps.MenuItem("📊 Ouvrir Panneau Complet", callback=self.open_full_panel))
        self.menu.add(rumps.MenuItem("📝 Voir Logs", callback=self.view_logs))
        
        # Séparateur et Quitter
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("❌ Quitter Guardian", callback=self.quit_app))
    
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
                        metrics['disk_percent'] = float(fields[4].replace('%', ''))
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
                    metrics['memory_percent'] = (active_pages / total_pages) * 100
                    metrics['memory_free_mb'] = (free_pages * 4096) // (1024 * 1024)
            
            # CPU via uptime
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            if uptime_result.returncode == 0:
                output = uptime_result.stdout
                if 'load averages:' in output:
                    load_avg_str = output.split('load averages:')[-1].strip().split()[0]
                    load_avg_str = load_avg_str.replace(',', '.')
                    metrics['cpu_percent'] = min(float(load_avg_str) * 25, 100)
            
            return metrics
            
        except Exception as e:
            print(f"Erreur métriques: {e}")
            return {}
    
    def update_menu_display(self):
        """Met à jour l'affichage du menu"""
        metrics = self.get_system_metrics()
        
        if not metrics:
            return
        
        self.last_metrics = metrics
        
        # Déterminer l'état général
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        # Changer l'icône selon l'état
        if disk_percent > 85 or memory_percent > 80:
            self.title = "⚠️"  # Alerte
            status_text = "⚠️  Attention requise"
            status_color = "rouge"
        elif disk_percent > 70 or memory_percent > 65:
            self.title = "🟡"  # Surveillance
            status_text = "🟡 Surveillance active"
            status_color = "orange"
        else:
            self.title = "🛡️"  # OK
            status_text = "✅ Système optimal"
            status_color = "vert"
        
        # Mettre à jour les éléments du menu
        self.status_item.title = f"{status_text} ({datetime.now().strftime('%H:%M')})"
        
        self.disk_item.title = f"💾 Disque: {disk_percent:.0f}% ({metrics.get('disk_free', 'N/A')} libre)"
        self.memory_item.title = f"🧠 Mémoire: {memory_percent:.0f}% ({metrics.get('memory_free_mb', 0):.0f}MB libre)"
        self.cpu_item.title = f"⚡ CPU: {cpu_percent:.0f}%"
        
        # Vérifier si nettoyage nécessaire
        if self.config['auto_cleanup_enabled'] and disk_percent > self.config['auto_cleanup_threshold']:
            self.schedule_auto_cleanup()
    
    def schedule_auto_cleanup(self):
        """Programme un nettoyage automatique"""
        if self.config['notifications_enabled']:
            self.send_notification(
                "MacCleaner Guardian",
                f"Nettoyage automatique dans 30 secondes (disque {self.last_metrics.get('disk_percent', 0):.0f}%)"
            )
        
        # Programmer nettoyage dans 30 secondes
        def delayed_cleanup():
            time.sleep(30)
            self.perform_auto_cleanup()
        
        threading.Thread(target=delayed_cleanup, daemon=True).start()
    
    def perform_auto_cleanup(self):
        """Effectue le nettoyage automatique"""
        try:
            actions = []
            
            # Vider la corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists():
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=30, capture_output=True)
                actions.append("Corbeille vidée")
            
            # Nettoyer caches sécurisés
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
                        actions.append(f"Cache {cache_path.name} nettoyé")
                    except:
                        pass
            
            # Purge mémoire
            try:
                subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
                actions.append("Mémoire purgée")
            except:
                pass
            
            # Mettre à jour config
            self.config['last_cleanup'] = datetime.now().isoformat()
            self.save_config()
            
            # Notification de succès
            if actions and self.config['notifications_enabled']:
                self.send_notification(
                    "Nettoyage terminé",
                    f"{len(actions)} optimisations appliquées"
                )
            
        except Exception as e:
            print(f"Erreur nettoyage auto: {e}")
    
    def send_notification(self, title, message):
        """Envoie une notification macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" sound name "Funk"
            '''
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def monitoring_loop(self):
        """Boucle de surveillance en arrière-plan"""
        while self.monitoring_active:
            try:
                self.update_menu_display()
                time.sleep(self.config['monitoring_interval'])
            except:
                time.sleep(60)
    
    def start_monitoring(self):
        """Démarre la surveillance système"""
        monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        monitoring_thread.start()
    
    # Callbacks du menu
    @rumps.clicked("🧹 Nettoyage Rapide")
    def quick_cleanup(self, _):
        """Nettoyage rapide manuel"""
        self.title = "🧹"  # Indication visuelle
        
        def cleanup_thread():
            self.perform_auto_cleanup()
            time.sleep(2)
            self.update_menu_display()  # Restaurer icône normale
        
        threading.Thread(target=cleanup_thread, daemon=True).start()
    
    @rumps.clicked("⚡ Optimisation")
    def quick_optimization(self, _):
        """Optimisation rapide"""
        self.title = "⚡"  # Indication visuelle
        
        def optimize_thread():
            try:
                # DNS flush
                subprocess.run(['sudo', 'dscacheutil', '-flushcache'], 
                             timeout=10, capture_output=True)
                
                # Purge mémoire
                subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
                
                if self.config['notifications_enabled']:
                    self.send_notification("Optimisation terminée", "Système optimisé")
                
                time.sleep(2)
                self.update_menu_display()  # Restaurer icône normale
                
            except Exception as e:
                print(f"Erreur optimisation: {e}")
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    @rumps.clicked("🔄 Actualiser")
    def force_update(self, _):
        """Force la mise à jour des métriques"""
        self.update_menu_display()
    
    def toggle_auto_cleanup(self, sender):
        """Bascule le nettoyage automatique"""
        self.config['auto_cleanup_enabled'] = not self.config['auto_cleanup_enabled']
        self.save_config()
        
        if self.config['auto_cleanup_enabled']:
            sender.title = "✅ Nettoyage Automatique"
        else:
            sender.title = "❌ Nettoyage Automatique"
    
    def toggle_notifications(self, sender):
        """Bascule les notifications"""
        self.config['notifications_enabled'] = not self.config['notifications_enabled']
        self.save_config()
        
        if self.config['notifications_enabled']:
            sender.title = "🔔 Notifications"
        else:
            sender.title = "🔕 Notifications"
    
    @rumps.clicked("📊 Ouvrir Panneau Complet")
    def open_full_panel(self, _):
        """Ouvre le panneau de contrôle complet"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            subprocess.Popen([
                'python3', 
                os.path.join(current_dir, 'maccleaner_guardian.py')
            ])
        except Exception as e:
            print(f"Erreur ouverture panneau: {e}")
    
    @rumps.clicked("📝 Voir Logs")
    def view_logs(self, _):
        """Ouvre les logs dans l'éditeur"""
        try:
            subprocess.run(['open', '-a', 'TextEdit', str(self.log_file)])
        except:
            pass
    
    @rumps.clicked("❌ Quitter Guardian")
    def quit_app(self, _):
        """Quitte l'application"""
        self.monitoring_active = False
        rumps.quit_application()

def main():
    """Point d'entrée principal"""
    print("🛡️  Démarrage MacCleaner Guardian MenuBar...")
    
    # Créer et lancer l'app
    app = MacCleanerMenuBar()
    app.run()

if __name__ == "__main__":
    main()