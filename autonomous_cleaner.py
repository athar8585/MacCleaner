#!/usr/bin/env python3
"""
MacCleaner Pro Autonomous - Système de nettoyage autonome intelligent
Surveillance continue, détection de malwares, et maintenance automatique
"""

import os
import sys
import time
import json
import threading
import subprocess
import sqlite3
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import schedule

class AutonomousCleanerAgent:
    def __init__(self):
        self.config_dir = os.path.expanduser('~/Library/Application Support/MacCleaner Pro')
        self.db_path = os.path.join(self.config_dir, 'cleaner_database.db')
        self.malware_db_path = os.path.join(self.config_dir, 'malware_signatures.db')
        self.log_file = os.path.join(self.config_dir, 'autonomous.log')
        
        # Configuration par défaut
        self.config = {
            'auto_clean_threshold': {
                'disk_usage_percent': 85,
                'available_space_gb': 10,
                'memory_usage_percent': 80
            },
            'schedule': {
                'daily_maintenance': '03:00',
                'weekly_deep_clean': 'sunday:02:00',
                'malware_scan': '12:00'
            },
            'protection': {
                'icloud_protection': True,
                'important_files': True,
                'recent_files_days': 7
            },
            'malware_protection': {
                'enabled': True,
                'auto_quarantine': True,
                'scan_downloads': True,
                'real_time_protection': False
            }
        }
        
        self.setup_environment()
        self.init_database()
        self.start_autonomous_monitoring()
        
    def setup_environment(self):
        """Configurer l'environnement autonome"""
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Créer le fichier de configuration
        config_file = os.path.join(self.config_dir, 'config.json')
        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        else:
            with open(config_file, 'r') as f:
                self.config.update(json.load(f))
                
    def init_database(self):
        """Initialiser la base de données intelligente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des scans et nettoyages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                trigger_type TEXT,
                files_cleaned INTEGER,
                space_freed INTEGER,
                duration_seconds INTEGER,
                system_state TEXT
            )
        ''')
        
        # Table des fichiers protégés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protected_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT UNIQUE,
                protection_reason TEXT,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_hash TEXT
            )
        ''')
        
        # Table des malwares détectés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS malware_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT,
                signature_match TEXT,
                threat_level TEXT,
                action_taken TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des métriques système
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                disk_free_gb REAL,
                active_processes INTEGER,
                network_activity TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialiser la base de signatures malware
        self.init_malware_database()
        
    def init_malware_database(self):
        """Initialiser la base de données de signatures malware"""
        conn = sqlite3.connect(self.malware_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS malware_signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signature_hash TEXT UNIQUE,
                malware_name TEXT,
                threat_level INTEGER,
                description TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ajouter des signatures de base
        basic_signatures = [
            ('d41d8cd98f00b204e9800998ecf8427e', 'Generic.Trojan', 5, 'Signature générique trojan'),
            ('5d41402abc4b2a76b9719d911017c592', 'Adware.Generic', 3, 'Logiciel publicitaire générique'),
            ('098f6bcd4621d373cade4e832627b4f6', 'Malware.Downloader', 4, 'Téléchargeur malveillant')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO malware_signatures 
            (signature_hash, malware_name, threat_level, description) 
            VALUES (?, ?, ?, ?)
        ''', basic_signatures)
        
        conn.commit()
        conn.close()
        
    def log_activity(self, message, level='INFO'):
        """Enregistrer les activités"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
            
        print(f"🤖 Agent Autonome: {message}")
        
    def start_autonomous_monitoring(self):
        """Démarrer la surveillance autonome"""
        self.log_activity("Démarrage de l'agent autonome MacCleaner Pro")
        
        # Programmer les tâches automatiques
        schedule.every().day.at(self.config['schedule']['daily_maintenance']).do(self.daily_maintenance)
        schedule.every().day.at(self.config['schedule']['malware_scan']).do(self.scan_malware)
        schedule.every().minute.do(self.check_system_thresholds)
        schedule.every(5).minutes.do(self.record_system_metrics)
        schedule.every().hour.do(self.update_malware_database)
        
        # Démarrer le thread de surveillance
        monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        # Démarrer la protection temps réel si activée
        if self.config['malware_protection']['real_time_protection']:
            realtime_thread = threading.Thread(target=self.realtime_protection, daemon=True)
            realtime_thread.start()
            
    def monitoring_loop(self):
        """Boucle principale de surveillance"""
        while True:
            try:
                schedule.run_pending()
                time.sleep(30)  # Vérifier toutes les 30 secondes
            except Exception as e:
                self.log_activity(f"Erreur monitoring: {str(e)}", 'ERROR')
                time.sleep(60)
                
    def check_system_thresholds(self):
        """Vérifier les seuils système pour déclenchement automatique"""
        try:
            # Vérifier l'usage disque
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            free_gb = disk_usage.free / (1024**3)
            
            # Vérifier l'usage mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Conditions de déclenchement
            should_clean = False
            trigger_reason = []
            
            if disk_percent > self.config['auto_clean_threshold']['disk_usage_percent']:
                should_clean = True
                trigger_reason.append(f"Disque à {disk_percent:.1f}%")
                
            if free_gb < self.config['auto_clean_threshold']['available_space_gb']:
                should_clean = True
                trigger_reason.append(f"Espace libre: {free_gb:.1f}GB")
                
            if memory_percent > self.config['auto_clean_threshold']['memory_usage_percent']:
                should_clean = True
                trigger_reason.append(f"Mémoire à {memory_percent:.1f}%")
                
            if should_clean:
                self.log_activity(f"Seuil dépassé: {', '.join(trigger_reason)} - Déclenchement nettoyage automatique")
                self.trigger_autonomous_cleaning('threshold_exceeded', trigger_reason)
                
        except Exception as e:
            self.log_activity(f"Erreur vérification seuils: {str(e)}", 'ERROR')
            
    def trigger_autonomous_cleaning(self, trigger_type, reasons):
        """Déclencher un nettoyage autonome"""
        start_time = time.time()
        
        try:
            self.log_activity(f"🧹 Début nettoyage autonome - Raison: {trigger_type}")
            
            # Importer et utiliser le nettoyeur principal
            from mac_cleaner import MacCleanerPro
            
            # Créer une instance sans interface graphique
            cleaner = MacCleanerPro()
            cleaner.root.withdraw()  # Cacher la fenêtre
            
            # Activer toutes les protections
            cleaner.protect_icloud.set(True)
            cleaner.analyze_only.set(False)  # Nettoyage réel
            
            # Activer toutes les catégories de nettoyage sûres
            safe_categories = ['System Caches', 'User Caches', 'Logs & Diagnostics', 'System Temp']
            for category in safe_categories:
                if category in cleaner.cleanup_vars:
                    cleaner.cleanup_vars[category].set(True)
                    
            # Lancer le nettoyage
            cleaner._cleaning_thread()
            
            # Enregistrer dans la base de données
            duration = int(time.time() - start_time)
            self.record_cleaning_history(trigger_type, 0, cleaner.total_freed_space, duration, reasons)
            
            self.log_activity(f"✅ Nettoyage autonome terminé - {cleaner.total_freed_space / (1024*1024):.1f} MB libérés")
            
        except Exception as e:
            self.log_activity(f"❌ Erreur nettoyage autonome: {str(e)}", 'ERROR')
            
    def daily_maintenance(self):
        """Maintenance quotidienne automatique"""
        self.log_activity("🔧 Début maintenance quotidienne")
        
        try:
            # Nettoyer les logs anciens
            self.cleanup_old_logs()
            
            # Optimiser la base de données
            self.optimize_database()
            
            # Vérifier les mises à jour de signatures
            self.update_malware_database()
            
            # Nettoyage léger automatique
            self.trigger_autonomous_cleaning('daily_maintenance', ['Maintenance programmée'])
            
        except Exception as e:
            self.log_activity(f"Erreur maintenance: {str(e)}", 'ERROR')
            
    def scan_malware(self):
        """Scanner les malwares"""
        self.log_activity("🛡️ Début scan malware")
        
        try:
            scan_paths = [
                os.path.expanduser('~/Downloads'),
                os.path.expanduser('~/Desktop'),
                '/Applications'
            ]
            
            threats_found = 0
            
            for scan_path in scan_paths:
                if os.path.exists(scan_path):
                    threats_found += self.scan_directory_for_malware(scan_path)
                    
            if threats_found > 0:
                self.log_activity(f"⚠️ {threats_found} menaces détectées et mises en quarantaine", 'WARNING')
            else:
                self.log_activity("✅ Aucune menace détectée")
                
        except Exception as e:
            self.log_activity(f"Erreur scan malware: {str(e)}", 'ERROR')
            
    def scan_directory_for_malware(self, directory):
        """Scanner un répertoire pour les malwares"""
        threats_found = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    
                    if self.is_suspicious_file(filepath):
                        threat_level = self.analyze_file_threat(filepath)
                        
                        if threat_level > 3:  # Menace significative
                            self.quarantine_file(filepath, f"Threat level: {threat_level}")
                            threats_found += 1
                            
        except Exception as e:
            self.log_activity(f"Erreur scan répertoire {directory}: {str(e)}", 'ERROR')
            
        return threats_found
        
    def is_suspicious_file(self, filepath):
        """Détecter si un fichier est suspect"""
        suspicious_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.pif', '.com', '.vbs', '.js',
            '.jar', '.app', '.dmg', '.pkg'
        ]
        
        suspicious_names = [
            'crack', 'keygen', 'patch', 'trojan', 'virus', 'malware',
            'backdoor', 'rootkit', 'spyware', 'adware'
        ]
        
        filename = os.path.basename(filepath).lower()
        
        # Vérifier l'extension
        for ext in suspicious_extensions:
            if filename.endswith(ext):
                return True
                
        # Vérifier les noms suspects
        for suspect in suspicious_names:
            if suspect in filename:
                return True
                
        return False
        
    def analyze_file_threat(self, filepath):
        """Analyser le niveau de menace d'un fichier"""
        try:
            # Calculer le hash du fichier
            file_hash = self.calculate_file_hash(filepath)
            
            # Vérifier dans la base de signatures
            conn = sqlite3.connect(self.malware_db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT threat_level, malware_name FROM malware_signatures WHERE signature_hash = ?',
                (file_hash,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                threat_level, malware_name = result
                self.log_activity(f"🚨 Malware détecté: {malware_name} dans {filepath}")
                return threat_level
                
            # Analyse heuristique
            heuristic_score = 0
            
            # Taille du fichier
            try:
                file_size = os.path.getsize(filepath)
                if file_size < 1024:  # Fichiers très petits suspects
                    heuristic_score += 1
                elif file_size > 100 * 1024 * 1024:  # Fichiers très gros suspects
                    heuristic_score += 2
            except OSError:
                pass
                
            # Emplacement du fichier
            if '/tmp/' in filepath or '/var/tmp/' in filepath:
                heuristic_score += 2
                
            # Nom du fichier
            filename = os.path.basename(filepath).lower()
            if any(c in filename for c in ['$', '~', '..', '--']):
                heuristic_score += 1
                
            return heuristic_score
            
        except Exception as e:
            self.log_activity(f"Erreur analyse menace {filepath}: {str(e)}", 'ERROR')
            return 0
            
    def calculate_file_hash(self, filepath):
        """Calculer le hash MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
            
    def quarantine_file(self, filepath, reason):
        """Mettre un fichier en quarantaine"""
        try:
            quarantine_dir = os.path.join(self.config_dir, 'quarantine')
            os.makedirs(quarantine_dir, exist_ok=True)
            
            # Nom unique pour le fichier en quarantaine
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            quarantine_name = f"{timestamp}_{os.path.basename(filepath)}"
            quarantine_path = os.path.join(quarantine_dir, quarantine_name)
            
            # Déplacer le fichier
            os.rename(filepath, quarantine_path)
            
            # Enregistrer dans la base de données
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO malware_detections 
                (filepath, signature_match, threat_level, action_taken) 
                VALUES (?, ?, ?, ?)
            ''', (filepath, reason, 'HIGH', f'Quarantined to {quarantine_path}'))
            conn.commit()
            conn.close()
            
            self.log_activity(f"🔒 Fichier mis en quarantaine: {filepath} -> {quarantine_path}")
            
        except Exception as e:
            self.log_activity(f"Erreur quarantaine {filepath}: {str(e)}", 'ERROR')
            
    def update_malware_database(self):
        """Mettre à jour la base de signatures malware depuis Internet"""
        try:
            # URL fictive pour les signatures (remplacer par une vraie source)
            signature_url = "https://raw.githubusercontent.com/malware-signatures/database/main/signatures.json"
            
            try:
                with urllib.request.urlopen(signature_url, timeout=10) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        self.update_signatures_from_data(data)
                        self.log_activity("✅ Base de signatures malware mise à jour")
                    else:
                        self.log_activity("⚠️ Impossible de récupérer les signatures", 'WARNING')
            except urllib.error.URLError:
                self.log_activity("⚠️ Pas de connexion Internet pour mise à jour signatures", 'WARNING')
                
        except Exception as e:
            self.log_activity(f"Erreur mise à jour signatures: {str(e)}", 'ERROR')
            
    def update_signatures_from_data(self, data):
        """Mettre à jour les signatures depuis les données téléchargées"""
        try:
            conn = sqlite3.connect(self.malware_db_path)
            cursor = conn.cursor()
            
            for signature in data.get('signatures', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO malware_signatures 
                    (signature_hash, malware_name, threat_level, description) 
                    VALUES (?, ?, ?, ?)
                ''', (
                    signature['hash'],
                    signature['name'],
                    signature['level'],
                    signature['description']
                ))
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.log_activity(f"Erreur mise à jour données: {str(e)}", 'ERROR')
            
    def record_system_metrics(self):
        """Enregistrer les métriques système"""
        try:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_metrics 
                (cpu_usage, memory_usage, disk_usage, disk_free_gb, active_processes) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                cpu_usage,
                memory.percent,
                (disk.used / disk.total) * 100,
                disk.free / (1024**3),
                len(psutil.pids())
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.log_activity(f"Erreur enregistrement métriques: {str(e)}", 'ERROR')
            
    def record_cleaning_history(self, trigger_type, files_cleaned, space_freed, duration, system_state):
        """Enregistrer l'historique de nettoyage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO cleaning_history 
                (trigger_type, files_cleaned, space_freed, duration_seconds, system_state) 
                VALUES (?, ?, ?, ?, ?)
            ''', (trigger_type, files_cleaned, space_freed, duration, json.dumps(system_state)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.log_activity(f"Erreur enregistrement historique: {str(e)}", 'ERROR')
            
    def cleanup_old_logs(self):
        """Nettoyer les anciens logs"""
        try:
            # Garder seulement les 30 derniers jours
            cutoff_date = datetime.now() - timedelta(days=30)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Nettoyer les anciennes métriques
            cursor.execute(
                'DELETE FROM system_metrics WHERE timestamp < ?',
                (cutoff_date.isoformat(),)
            )
            
            # Garder l'historique de nettoyage plus longtemps (90 jours)
            history_cutoff = datetime.now() - timedelta(days=90)
            cursor.execute(
                'DELETE FROM cleaning_history WHERE timestamp < ?',
                (history_cutoff.isoformat(),)
            )
            
            conn.commit()
            conn.close()
            
            # Nettoyer le fichier de log
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    
                # Garder seulement les 1000 dernières lignes
                if len(lines) > 1000:
                    with open(self.log_file, 'w') as f:
                        f.writelines(lines[-1000:])
                        
        except Exception as e:
            self.log_activity(f"Erreur nettoyage logs: {str(e)}", 'ERROR')
            
    def optimize_database(self):
        """Optimiser les bases de données"""
        try:
            for db_path in [self.db_path, self.malware_db_path]:
                conn = sqlite3.connect(db_path)
                conn.execute('VACUUM')
                conn.execute('ANALYZE')
                conn.close()
                
            self.log_activity("✅ Bases de données optimisées")
            
        except Exception as e:
            self.log_activity(f"Erreur optimisation BDD: {str(e)}", 'ERROR')
            
    def realtime_protection(self):
        """Protection en temps réel (surveillance des nouveaux fichiers)"""
        self.log_activity("🛡️ Protection temps réel activée")
        
        watch_dirs = [
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop')
        ]
        
        # Stockage des états précédents
        previous_states = {}
        
        for watch_dir in watch_dirs:
            if os.path.exists(watch_dir):
                previous_states[watch_dir] = set(os.listdir(watch_dir))
                
        while True:
            try:
                for watch_dir in watch_dirs:
                    if os.path.exists(watch_dir):
                        current_files = set(os.listdir(watch_dir))
                        previous_files = previous_states.get(watch_dir, set())
                        
                        # Détecter les nouveaux fichiers
                        new_files = current_files - previous_files
                        
                        for new_file in new_files:
                            filepath = os.path.join(watch_dir, new_file)
                            if os.path.isfile(filepath):
                                self.log_activity(f"🔍 Nouveau fichier détecté: {filepath}")
                                
                                # Scanner immédiatement
                                threat_level = self.analyze_file_threat(filepath)
                                if threat_level > 3:
                                    self.quarantine_file(filepath, f"Real-time detection: {threat_level}")
                                    
                        previous_states[watch_dir] = current_files
                        
                time.sleep(5)  # Vérifier toutes les 5 secondes
                
            except Exception as e:
                self.log_activity(f"Erreur protection temps réel: {str(e)}", 'ERROR')
                time.sleep(30)
                
    def get_status_report(self):
        """Générer un rapport de statut complet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Dernières métriques
            cursor.execute('''
                SELECT cpu_usage, memory_usage, disk_usage, disk_free_gb 
                FROM system_metrics 
                ORDER BY timestamp DESC LIMIT 1
            ''')
            latest_metrics = cursor.fetchone()
            
            # Statistiques de nettoyage
            cursor.execute('''
                SELECT COUNT(*), SUM(space_freed), AVG(duration_seconds)
                FROM cleaning_history 
                WHERE timestamp > datetime('now', '-7 days')
            ''')
            cleaning_stats = cursor.fetchone()
            
            # Détections malware
            cursor.execute('''
                SELECT COUNT(*) 
                FROM malware_detections 
                WHERE timestamp > datetime('now', '-7 days')
            ''')
            malware_count = cursor.fetchone()[0]
            
            conn.close()
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_health': {
                    'cpu_usage': latest_metrics[0] if latest_metrics else 0,
                    'memory_usage': latest_metrics[1] if latest_metrics else 0,
                    'disk_usage': latest_metrics[2] if latest_metrics else 0,
                    'disk_free_gb': latest_metrics[3] if latest_metrics else 0
                },
                'cleaning_performance': {
                    'cleanings_last_week': cleaning_stats[0] if cleaning_stats else 0,
                    'space_freed_mb': (cleaning_stats[1] / (1024*1024)) if cleaning_stats and cleaning_stats[1] else 0,
                    'avg_duration_seconds': cleaning_stats[2] if cleaning_stats else 0
                },
                'security': {
                    'threats_detected_last_week': malware_count,
                    'protection_active': self.config['malware_protection']['enabled']
                }
            }
            
            return report
            
        except Exception as e:
            self.log_activity(f"Erreur génération rapport: {str(e)}", 'ERROR')
            return {}

def start_autonomous_agent():
    """Démarrer l'agent autonome"""
    try:
        agent = AutonomousCleanerAgent()
        
        # Garder le processus actif
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Agent autonome arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur agent autonome: {str(e)}")

if __name__ == "__main__":
    start_autonomous_agent()