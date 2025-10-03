#!/usr/bin/env python3
"""
Détection heuristique de comportements suspects
Surveillance processus CPU + création fichiers sensibles
"""

import psutil
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
import os
import json

class HeuristicScanner:
    """Scanner heuristique pour détecter comportements suspects"""
    
    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.monitoring = False
        self.monitor_thread = None
        self.alerts = []
        
        # Seuils de détection
        self.cpu_threshold = 80.0  # % CPU suspect
        self.cpu_duration_threshold = 30  # secondes
        self.memory_threshold = 1024 * 1024 * 1024  # 1GB
        
        # Dossiers sensibles à surveiller
        self.sensitive_paths = [
            Path.home() / 'Library' / 'LaunchAgents',
            Path.home() / 'Library' / 'LaunchDaemons',
            Path('/Library/LaunchAgents'),
            Path('/Library/LaunchDaemons'),
            Path('/System/Library/LaunchAgents'),
            Path('/System/Library/LaunchDaemons'),
            Path.home() / 'Library' / 'Application Support',
            Path.home() / 'Library' / 'Preferences',
        ]
        
        # Extensions de fichiers suspects
        self.suspicious_extensions = {'.plist', '.app', '.pkg', '.dmg', '.sh', '.py', '.pl', '.rb'}
        
        # Processus surveillés
        self.monitored_processes = {}
        self.file_watchers = {}
    
    def start_monitoring(self):
        """Démarrer la surveillance heuristique"""
        if self.monitoring:
            self.log("⚠️ Surveillance déjà active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.log("🔍 Surveillance heuristique démarrée")
    
    def stop_monitoring(self):
        """Arrêter la surveillance"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.log("🔍 Surveillance heuristique arrêtée")
    
    def _monitor_loop(self):
        """Boucle principale de surveillance"""
        while self.monitoring:
            try:
                self._check_cpu_anomalies()
                self._check_file_changes()
                self._check_network_activity()
                time.sleep(5)  # Vérification toutes les 5 secondes
            except Exception as e:
                self.log(f"❌ Erreur surveillance: {e}")
                time.sleep(10)
    
    def _check_cpu_anomalies(self):
        """Détecter processus avec forte utilisation CPU"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'create_time']):
                try:
                    proc_info = proc.info
                    cpu_percent = proc.cpu_percent()
                    
                    if cpu_percent > self.cpu_threshold:
                        pid = proc_info['pid']
                        
                        # Suivre le processus
                        if pid not in self.monitored_processes:
                            self.monitored_processes[pid] = {
                                'name': proc_info['name'],
                                'start_time': time.time(),
                                'alerts_sent': 0,
                                'max_cpu': cpu_percent,
                                'memory_mb': proc_info['memory_info'].rss / (1024*1024) if proc_info['memory_info'] else 0
                            }
                        else:
                            # Mettre à jour
                            self.monitored_processes[pid]['max_cpu'] = max(
                                self.monitored_processes[pid]['max_cpu'], 
                                cpu_percent
                            )
                        
                        # Vérifier si alerte nécessaire
                        duration = time.time() - self.monitored_processes[pid]['start_time']
                        if (duration > self.cpu_duration_threshold and 
                            self.monitored_processes[pid]['alerts_sent'] == 0):
                            
                            self._create_alert(
                                'cpu_anomaly',
                                f"Processus {proc_info['name']} (PID {pid}) utilise {cpu_percent:.1f}% CPU depuis {duration:.0f}s",
                                {'pid': pid, 'name': proc_info['name'], 'cpu': cpu_percent, 'duration': duration}
                            )
                            self.monitored_processes[pid]['alerts_sent'] += 1
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Nettoyer les processus terminés
            active_pids = {p.pid for p in psutil.process_iter()}
            finished_pids = set(self.monitored_processes.keys()) - active_pids
            for pid in finished_pids:
                del self.monitored_processes[pid]
                
        except Exception as e:
            self.log(f"❌ Erreur check CPU: {e}")
    
    def _check_file_changes(self):
        """Surveiller création/modification fichiers sensibles"""
        try:
            for path in self.sensitive_paths:
                if not path.exists():
                    continue
                
                try:
                    # Vérifier modification récente (dernières 5 minutes)
                    for item in path.iterdir():
                        if item.is_file():
                            stat = item.stat()
                            age = time.time() - stat.st_mtime
                            
                            if age < 300:  # 5 minutes
                                # Double validation: extension ET nom suspect
                                # Mais JAMAIS pour les fichiers Apple
                                if self._is_truly_suspicious_file(item):
                                    alert_key = f"file_{item}"
                                    if alert_key not in self.file_watchers:
                                        self._create_alert(
                                            'suspicious_file',
                                            f"Fichier suspect créé: {item}",
                                            {'path': str(item), 'age_seconds': age, 'size': stat.st_size}
                                        )
                                        self.file_watchers[alert_key] = time.time()
                
                except (PermissionError, OSError):
                    continue
        
        except Exception as e:
            self.log(f"❌ Erreur check fichiers: {e}")
    
    def _check_network_activity(self):
        """Détecter activité réseau anormale"""
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                # Vérifier processus avec forte activité réseau
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        connections = proc.connections()
                        if len(connections) > 10:  # Beaucoup de connexions
                            pid = proc.info['pid']
                            name = proc.info['name']
                            
                            alert_key = f"network_{pid}"
                            if alert_key not in self.file_watchers:
                                self._create_alert(
                                    'network_anomaly',
                                    f"Processus {name} (PID {pid}) a {len(connections)} connexions réseau",
                                    {'pid': pid, 'name': name, 'connections': len(connections)}
                                )
                                self.file_watchers[alert_key] = time.time()
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        
        except Exception as e:
            self.log(f"❌ Erreur check réseau: {e}")
    
    def _is_truly_suspicious_file(self, file_path):
        """Validation complète pour éviter les faux positifs Apple"""
        filename = file_path.name.lower()
        
        # 1. JAMAIS signaler les fichiers Apple
        if 'com.apple.' in filename:
            return False
            
        # 2. Ignorer les fichiers système connus
        apple_system_files = [
            'contextstore', 'dataaccess.babysitter', 'spaces',
            'assistant', 'sharingd', 'ncprefs', 'icloud',
            'speech.recognition', 'telephonyutilities', 'duetexpertcenter',
            'knowledge-agent', 'xpc.activity', 'calaccessd', 'addressbook'
        ]
        
        for system_file in apple_system_files:
            if system_file in filename:
                return False
        
        # 3. Seulement pour des fichiers VRAIMENT suspects
        # Extensions suspectes MAIS pas dans Preferences Apple
        if file_path.suffix.lower() == '.plist':
            # Les .plist dans Preferences sont généralement légitimes
            if 'preferences' in str(file_path.parent).lower():
                return False
        
        # 4. Vérifier le nom avec la nouvelle fonction
        return self._is_suspicious_name(filename)

    def _is_suspicious_name(self, filename):
        """Vérifier si nom de fichier suspect - avec filtrage intelligent Apple"""
        
        # Exclure TOUS les fichiers système Apple
        filename_lower = filename.lower()
        
        # Patterns Apple à ignorer complètement
        apple_patterns = [
            'com.apple.',           # Tous les fichiers Apple
            'contextstore',         # ContextStoreAgent
            'dataaccess.babysitter', # com.apple.dataaccess.babysitter
            'spaces',               # com.apple.spaces
            'assistant',            # com.apple.assistant
            'sharingd',             # com.apple.sharingd
            'ncprefs',              # com.apple.ncprefs
            'icloud',               # iCloud related
            'speech.recognition',   # Speech recognition
            'telephonyutilities',   # Telephony
            'duetexpertcenter',     # Duet Expert
            'knowledge-agent',      # Knowledge agent
            'xpc.activity',         # XPC activities
            'calaccessd',           # Calendar access
            'addressbook'           # Address book
        ]
        
        # Si c'est un fichier Apple, ne pas le considérer comme suspect
        for pattern in apple_patterns:
            if pattern in filename_lower:
                return False
        
        # Patterns vraiment suspects (pas Apple)
        suspicious_patterns = [
            'keylog', 'capture', 'monitor', 'spy', 'rat', 'backdoor',
            'cryptominer', 'miner', 'stealer', 'ransomware', 'trojan',
            'malware', 'virus', 'exploit', 'payload'
        ]
        
        return any(pattern in filename_lower for pattern in suspicious_patterns)
    
    def _create_alert(self, alert_type, message, metadata=None):
        """Créer une alerte"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'metadata': metadata or {}
        }
        self.alerts.append(alert)
        self.log(f"🚨 ALERTE HEURISTIQUE: {message}")
        
        # Limiter le nombre d'alertes stockées
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-50:]
    
    def get_alerts(self, hours=24):
        """Obtenir alertes récentes"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_alerts = []
        
        for alert in self.alerts:
            alert_time = datetime.fromisoformat(alert['timestamp'])
            if alert_time > cutoff:
                recent_alerts.append(alert)
        
        return recent_alerts
    
    def get_summary(self):
        """Résumé de la surveillance"""
        recent_alerts = self.get_alerts(24)
        alert_types = {}
        for alert in recent_alerts:
            alert_type = alert['type']
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        return {
            'monitoring': self.monitoring,
            'total_alerts_24h': len(recent_alerts),
            'alert_types': alert_types,
            'monitored_processes': len(self.monitored_processes),
            'monitored_paths': len([p for p in self.sensitive_paths if p.exists()])
        }
    
    def export_alerts(self, filepath):
        """Exporter alertes vers fichier"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.alerts, f, indent=2)
            return True
        except Exception as e:
            self.log(f"❌ Erreur export alertes: {e}")
            return False