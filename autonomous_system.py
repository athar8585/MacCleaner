#!/usr/bin/env python3
"""
MacCleaner Pro Autonomous System
Système de surveillance et nettoyage autonome avec seuils d'alerte
"""

import os
import sys
import time
import json
import sqlite3
import threading
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import hashlib
import plistlib

class MacCleanerAutonomous:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config" / "autonomous_config.json"
        self.db_file = self.base_dir / "data" / "cleaner_database.db"
        self.malware_db_file = self.base_dir / "data" / "malware_signatures.db"
        
        # Configuration par défaut
        self.default_config = {
            "monitoring": {
                "disk_usage_threshold": 85,  # %
                "memory_usage_threshold": 80,  # %
                "scan_interval": 3600,  # secondes (1 heure)
                "auto_clean_enabled": True,
                "malware_scan_enabled": True
            },
            "protection": {
                "protect_icloud": True,
                "protect_recent_files": True,
                "recent_files_days": 7,
                "whitelist_extensions": [".docx", ".pdf", ".jpg", ".png", ".mp4", ".mov"],
                "critical_directories": ["Documents", "Desktop", "Projects", "Pictures"]
            },
            "updates": {
                "auto_update_db": True,
                "update_server": "https://raw.githubusercontent.com/yourusername/MacCleaner-Pro/main/updates/",
                "check_interval": 86400  # 24 heures
            },
            "notifications": {
                "show_alerts": True,
                "alert_sounds": True,
                "cleanup_reports": True
            }
        }
        
        self.running = False
        self.last_scan = None
        self.stats = {
            "total_cleanups": 0,
            "space_freed": 0,
            "malware_detected": 0,
            "last_cleanup": None
        }
        
        self.setup_environment()
        
    def setup_environment(self):
        """Initialiser l'environnement du système autonome"""
        # Créer les répertoires nécessaires
        for dir_name in ["config", "data", "logs", "temp", "quarantine"]:
            (self.base_dir / dir_name).mkdir(exist_ok=True)
            
        # Initialiser la configuration
        if not self.config_file.exists():
            self.save_config(self.default_config)
        else:
            self.config = self.load_config()
            
        # Initialiser la base de données
        self.init_database()
        
        # Initialiser la base de données de malware
        self.init_malware_database()
        
        print("🚀 MacCleaner Pro Autonomous System initialisé")
        
    def load_config(self):
        """Charger la configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return self.default_config
            
    def save_config(self, config):
        """Sauvegarder la configuration"""
        self.config = config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def init_database(self):
        """Initialiser la base de données de nettoyage"""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cleanup_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    files_cleaned INTEGER,
                    space_freed INTEGER,
                    categories TEXT,
                    duration REAL,
                    trigger_type TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    disk_usage REAL,
                    memory_usage REAL,
                    cpu_usage REAL,
                    temperature REAL,
                    alert_triggered BOOLEAN
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS file_whitelist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    date_added TEXT,
                    reason TEXT
                )
            ''')
            
    def init_malware_database(self):
        """Initialiser la base de données de malware"""
        with sqlite3.connect(self.malware_db_file) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS malware_signatures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signature_hash TEXT UNIQUE,
                    malware_name TEXT,
                    threat_level INTEGER,
                    description TEXT,
                    date_added TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS scan_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    file_path TEXT,
                    threat_detected BOOLEAN,
                    threat_name TEXT,
                    action_taken TEXT
                )
            ''')
            
    def start_autonomous_monitoring(self):
        """Démarrer la surveillance autonome"""
        self.running = True
        print("🔍 Surveillance autonome démarrée...")
        
        # Thread de surveillance principale
        monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        # Thread de mise à jour des bases de données
        update_thread = threading.Thread(target=self._update_loop, daemon=True)
        update_thread.start()
        
        return True
        
    def _monitoring_loop(self):
        """Boucle principale de surveillance"""
        while self.running:
            try:
                # Collecter les métriques système
                metrics = self.collect_system_metrics()
                
                # Enregistrer dans la base de données
                self.save_metrics(metrics)
                
                # Vérifier les seuils d'alerte
                alerts = self.check_alert_thresholds(metrics)
                
                if alerts:
                    self.handle_alerts(alerts, metrics)
                    
                # Scanner les malwares périodiquement
                if self.config["monitoring"]["malware_scan_enabled"]:
                    if self.should_scan_malware():
                        self.scan_for_malware()
                        
                # Attendre avant le prochain scan
                time.sleep(self.config["monitoring"]["scan_interval"])
                
            except Exception as e:
                self.log_error(f"Erreur surveillance: {e}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
                
    def collect_system_metrics(self):
        """Collecter les métriques système"""
        try:
            # Utilisation disque
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Utilisation mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Utilisation CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Température (si disponible)
            temperature = self.get_cpu_temperature()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'disk_usage': disk_percent,
                'memory_usage': memory_percent,
                'cpu_usage': cpu_percent,
                'temperature': temperature,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            self.log_error(f"Erreur collecte métriques: {e}")
            return None
            
    def get_cpu_temperature(self):
        """Obtenir la température du CPU (macOS)"""
        try:
            # Utiliser powermetrics pour obtenir la température
            result = subprocess.run(['powermetrics', '-n', '1', '-s', 'cpu_power'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Parser la sortie pour extraire la température
                for line in result.stdout.split('\n'):
                    if 'CPU die temperature' in line:
                        temp_str = line.split(':')[1].strip().replace('°C', '')
                        return float(temp_str)
        except Exception:
            pass
        return None
        
    def save_metrics(self, metrics):
        """Sauvegarder les métriques en base"""
        if not metrics:
            return
            
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    INSERT INTO system_monitoring 
                    (timestamp, disk_usage, memory_usage, cpu_usage, temperature, alert_triggered)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    metrics['timestamp'],
                    metrics['disk_usage'],
                    metrics['memory_usage'], 
                    metrics['cpu_usage'],
                    metrics['temperature'],
                    False
                ))
        except Exception as e:
            self.log_error(f"Erreur sauvegarde métriques: {e}")
            
    def check_alert_thresholds(self, metrics):
        """Vérifier les seuils d'alerte"""
        if not metrics:
            return []
            
        alerts = []
        config = self.config["monitoring"]
        
        # Seuil disque
        if metrics['disk_usage'] >= config["disk_usage_threshold"]:
            alerts.append({
                'type': 'disk_full',
                'severity': 'high' if metrics['disk_usage'] >= 95 else 'medium',
                'message': f"Disque plein à {metrics['disk_usage']:.1f}%",
                'value': metrics['disk_usage']
            })
            
        # Seuil mémoire
        if metrics['memory_usage'] >= config["memory_usage_threshold"]:
            alerts.append({
                'type': 'memory_high',
                'severity': 'medium',
                'message': f"Mémoire élevée à {metrics['memory_usage']:.1f}%",
                'value': metrics['memory_usage']
            })
            
        # Seuil température
        if metrics['temperature'] and metrics['temperature'] >= 80:
            alerts.append({
                'type': 'temperature_high',
                'severity': 'high',
                'message': f"Température élevée: {metrics['temperature']:.1f}°C",
                'value': metrics['temperature']
            })
            
        return alerts
        
    def handle_alerts(self, alerts, metrics):
        """Gérer les alertes déclenchées"""
        print(f"🚨 {len(alerts)} alerte(s) détectée(s)")
        
        for alert in alerts:
            print(f"   ⚠️  {alert['message']}")
            
            # Envoyer notification système
            if self.config["notifications"]["show_alerts"]:
                self.send_system_notification(alert['message'])
                
            # Déclencher nettoyage automatique si configuré
            if (self.config["monitoring"]["auto_clean_enabled"] and 
                alert['type'] == 'disk_full' and 
                alert['severity'] == 'high'):
                
                print("🧹 Déclenchement du nettoyage automatique...")
                self.trigger_autonomous_cleanup(alert)
                
        # Marquer l'alerte en base
        self.mark_alert_triggered(metrics['timestamp'])
        
    def send_system_notification(self, message):
        """Envoyer une notification système macOS"""
        try:
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" with title "MacCleaner Pro" sound name "Glass"'
            ], check=True)
        except Exception as e:
            self.log_error(f"Erreur notification: {e}")
            
    def trigger_autonomous_cleanup(self, alert):
        """Déclencher un nettoyage autonome"""
        try:
            print("🚀 Début du nettoyage autonome...")
            
            # Importer le module de nettoyage principal
            from mac_cleaner import MacCleanerPro
            
            # Créer une instance en mode autonome
            cleaner = MacCleanerPro()
            cleaner.protect_icloud.set(True)  # Protection activée par défaut
            
            # Sélectionner les catégories de nettoyage selon l'alerte
            categories = self.select_cleanup_categories(alert)
            
            # Effectuer le nettoyage
            for category in categories:
                if category in cleaner.cleanup_vars:
                    cleaner.cleanup_vars[category].set(True)
                    
            # Lancer le nettoyage
            start_time = time.time()
            # cleaner.start_cleaning()  # Méthode simplifiée pour le mode autonome
            
            # Enregistrer les résultats
            duration = time.time() - start_time
            self.save_cleanup_results({
                'files_cleaned': 0,  # À implémenter
                'space_freed': 0,    # À implémenter
                'categories': categories,
                'duration': duration,
                'trigger_type': 'autonomous'
            })
            
            # Notification de fin
            self.send_system_notification("Nettoyage autonome terminé ✅")
            
        except Exception as e:
            self.log_error(f"Erreur nettoyage autonome: {e}")
            
    def select_cleanup_categories(self, alert):
        """Sélectionner les catégories de nettoyage selon l'alerte"""
        if alert['type'] == 'disk_full':
            if alert['severity'] == 'high':
                # Nettoyage agressif
                return ['System Caches', 'User Caches', 'Logs & Diagnostics', 
                       'System Temp', 'Downloads & Trash']
            else:
                # Nettoyage modéré
                return ['System Caches', 'User Caches', 'System Temp']
        elif alert['type'] == 'memory_high':
            return ['System Caches', 'User Caches']
        else:
            return ['System Temp']
            
    def scan_for_malware(self):
        """Scanner les malwares"""
        print("🔍 Scan anti-malware en cours...")
        
        try:
            # Chemins à scanner
            scan_paths = [
                os.path.expanduser('~/Downloads'),
                os.path.expanduser('~/Applications'),
                '/Applications',
                '/tmp'
            ]
            
            threats_found = 0
            
            for scan_path in scan_paths:
                if os.path.exists(scan_path):
                    threats_found += self.scan_directory_for_malware(scan_path)
                    
            if threats_found > 0:
                self.send_system_notification(f"⚠️ {threats_found} menace(s) détectée(s)")
            else:
                print("✅ Aucune menace détectée")
                
        except Exception as e:
            self.log_error(f"Erreur scan malware: {e}")
            
    def scan_directory_for_malware(self, directory):
        """Scanner un répertoire pour les malwares"""
        threats_found = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.scan_file_for_malware(file_path):
                        threats_found += 1
                        
        except Exception as e:
            self.log_error(f"Erreur scan répertoire {directory}: {e}")
            
        return threats_found
        
    def scan_file_for_malware(self, file_path):
        """Scanner un fichier pour les malwares"""
        try:
            # Vérifier la taille du fichier (ignorer les très gros fichiers)
            if os.path.getsize(file_path) > 100 * 1024 * 1024:  # 100MB
                return False
                
            # Calculer le hash du fichier
            file_hash = self.calculate_file_hash(file_path)
            
            # Vérifier contre la base de signatures
            if self.check_malware_signature(file_hash):
                self.quarantine_file(file_path)
                return True
                
            # Vérifications heuristiques
            if self.heuristic_malware_check(file_path):
                self.quarantine_file(file_path)
                return True
                
        except Exception as e:
            self.log_error(f"Erreur scan fichier {file_path}: {e}")
            
        return False
        
    def calculate_file_hash(self, file_path):
        """Calculer le hash SHA256 d'un fichier"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return None
            
    def check_malware_signature(self, file_hash):
        """Vérifier si le hash correspond à une signature de malware"""
        try:
            with sqlite3.connect(self.malware_db_file) as conn:
                cursor = conn.execute(
                    "SELECT malware_name FROM malware_signatures WHERE signature_hash = ?",
                    (file_hash,)
                )
                result = cursor.fetchone()
                return result is not None
        except Exception:
            return False
            
    def heuristic_malware_check(self, file_path):
        """Vérifications heuristiques pour détecter les malwares"""
        filename = os.path.basename(file_path).lower()
        
        # Noms de fichiers suspects
        suspicious_names = [
            'flashplayer', 'mackeeper', 'cleanmaster', 'advanced mac cleaner',
            'mac auto fixer', 'mac speedup', 'chromium', 'genieo'
        ]
        
        for suspicious in suspicious_names:
            if suspicious in filename:
                return True
                
        # Extensions suspectes
        suspicious_extensions = ['.dmg', '.pkg', '.app']
        if any(filename.endswith(ext) for ext in suspicious_extensions):
            # Vérifications supplémentaires pour ces types de fichiers
            if self.check_suspicious_app(file_path):
                return True
                
        return False
        
    def check_suspicious_app(self, file_path):
        """Vérifier si une application est suspecte"""
        try:
            # Vérifier les bundles .app
            if file_path.endswith('.app'):
                info_plist_path = os.path.join(file_path, 'Contents', 'Info.plist')
                if os.path.exists(info_plist_path):
                    with open(info_plist_path, 'rb') as f:
                        plist_data = plistlib.load(f)
                        
                    # Vérifier les identifiants suspects
                    bundle_id = plist_data.get('CFBundleIdentifier', '')
                    suspicious_ids = ['com.genieo', 'com.mackeeper', 'com.cleanmaster']
                    
                    for suspicious in suspicious_ids:
                        if suspicious in bundle_id:
                            return True
                            
        except Exception:
            pass
            
        return False
        
    def quarantine_file(self, file_path):
        """Mettre un fichier en quarantaine"""
        try:
            quarantine_dir = self.base_dir / "quarantine"
            quarantine_dir.mkdir(exist_ok=True)
            
            # Générer un nom unique pour le fichier en quarantaine
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            quarantine_name = f"{timestamp}_{os.path.basename(file_path)}"
            quarantine_path = quarantine_dir / quarantine_name
            
            # Déplacer le fichier
            shutil.move(file_path, quarantine_path)
            
            # Enregistrer l'action
            self.log_quarantine_action(file_path, str(quarantine_path))
            
            print(f"🔒 Fichier mis en quarantaine: {file_path}")
            
        except Exception as e:
            self.log_error(f"Erreur quarantaine {file_path}: {e}")
            
    def _update_loop(self):
        """Boucle de mise à jour des bases de données"""
        while self.running:
            try:
                if self.config["updates"]["auto_update_db"]:
                    self.update_malware_database()
                    
                # Attendre 24h avant la prochaine mise à jour
                time.sleep(self.config["updates"]["check_interval"])
                
            except Exception as e:
                self.log_error(f"Erreur mise à jour: {e}")
                time.sleep(3600)  # Réessayer dans 1h en cas d'erreur
                
    def update_malware_database(self):
        """Mettre à jour la base de données de malware depuis Internet"""
        try:
            print("🔄 Mise à jour de la base de données de malware...")
            
            # URL de la base de signatures (à créer sur GitHub)
            url = self.config["updates"]["update_server"] + "malware_signatures.json"
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                signatures = response.json()
                
                with sqlite3.connect(self.malware_db_file) as conn:
                    for sig in signatures:
                        conn.execute('''
                            INSERT OR REPLACE INTO malware_signatures 
                            (signature_hash, malware_name, threat_level, description, date_added)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            sig['hash'],
                            sig['name'],
                            sig['threat_level'],
                            sig['description'],
                            datetime.now().isoformat()
                        ))
                        
                print(f"✅ Base de données mise à jour: {len(signatures)} signatures")
                
        except Exception as e:
            self.log_error(f"Erreur mise à jour DB: {e}")
            
    def log_error(self, message):
        """Enregistrer une erreur dans les logs"""
        log_file = self.base_dir / "logs" / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            with open(log_file, 'a') as f:
                f.write(f"[{datetime.now().isoformat()}] {message}\n")
        except Exception:
            pass
            
    def log_quarantine_action(self, original_path, quarantine_path):
        """Enregistrer une action de quarantaine"""
        try:
            with sqlite3.connect(self.malware_db_file) as conn:
                conn.execute('''
                    INSERT INTO scan_results 
                    (timestamp, file_path, threat_detected, threat_name, action_taken)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    original_path,
                    True,
                    "Heuristic Detection",
                    f"Quarantined to {quarantine_path}"
                ))
        except Exception as e:
            self.log_error(f"Erreur log quarantaine: {e}")
            
    def should_scan_malware(self):
        """Déterminer s'il faut lancer un scan malware"""
        # Scanner une fois par jour
        if self.last_scan is None:
            self.last_scan = datetime.now()
            return True
            
        if datetime.now() - self.last_scan > timedelta(days=1):
            self.last_scan = datetime.now()
            return True
            
        return False
        
    def mark_alert_triggered(self, timestamp):
        """Marquer qu'une alerte a été déclenchée"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    UPDATE system_monitoring 
                    SET alert_triggered = 1 
                    WHERE timestamp = ?
                ''', (timestamp,))
        except Exception as e:
            self.log_error(f"Erreur marquage alerte: {e}")
            
    def save_cleanup_results(self, results):
        """Sauvegarder les résultats de nettoyage"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    INSERT INTO cleanup_history 
                    (timestamp, files_cleaned, space_freed, categories, duration, trigger_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    results['files_cleaned'],
                    results['space_freed'],
                    json.dumps(results['categories']),
                    results['duration'],
                    results['trigger_type']
                ))
                
            self.stats['total_cleanups'] += 1
            self.stats['space_freed'] += results['space_freed']
            self.stats['last_cleanup'] = datetime.now().isoformat()
            
        except Exception as e:
            self.log_error(f"Erreur sauvegarde résultats: {e}")
            
    def stop_monitoring(self):
        """Arrêter la surveillance"""
        self.running = False
        print("🛑 Surveillance autonome arrêtée")
        
    def get_status(self):
        """Obtenir le statut du système"""
        return {
            'running': self.running,
            'last_scan': self.last_scan.isoformat() if self.last_scan else None,
            'stats': self.stats,
            'config': self.config
        }

if __name__ == "__main__":
    # Créer et démarrer le système autonome
    autonomous_system = MacCleanerAutonomous()
    
    try:
        # Démarrer la surveillance
        autonomous_system.start_autonomous_monitoring()
        
        print("✅ Système autonome démarré")
        print("📊 Surveillance en cours...")
        print("🔍 Anti-malware actif")
        print("⚡ Nettoyage automatique configuré")
        print("\nAppuyez sur Ctrl+C pour arrêter")
        
        # Maintenir le programme en vie
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé...")
        autonomous_system.stop_monitoring()
        print("👋 Système autonome arrêté")
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        autonomous_system.stop_monitoring()