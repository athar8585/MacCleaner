#!/usr/bin/env python3
"""
Scanner Heuristique pour MacCleaner Pro
Détection comportementale de malware et activités suspectes
"""

import os
import psutil
import threading
import time
from datetime import datetime
from pathlib import Path

class HeuristicScanner:
    def __init__(self, log_fn=None):
        self.log = log_fn or print  # Utiliser print par défaut
        self.monitoring = False
        self.monitor_thread = None
        self.suspicious_processes = []
        self.suspicious_files = []
        self.alerts = []
        self.auto_actions = True  # Actions automatiques activées
        
        # Signatures comportementales
        self.suspicious_patterns = {
            'processes': [
                'cryptominer', 'xmrig', 'cpuminer', 'nicehash',
                'malware', 'virus', 'trojan', 'backdoor',
                'keylogger', 'ransomware', 'adware'
            ],
            'files': [
                '.cryptominer', '.miner', '.hidden',
                'malware', 'virus', 'trojan'
            ],
            'network': [
                'mining.pool', 'crypto.pool', 'suspicious.domain'
            ],
            'ignore_system_files': [
                'com.apple.', '.GlobalPreferences', 'ContextStoreAgent',
                'BezelServices', 'dataaccess.babysitter', 'spaces',
                'assistant', 'Accessibility', 'ncprefs', 'icloud',
                'SpeakSelection', 'speech.recognition', 'HIToolbox',
                'DuetExpertCenter', 'knowledge-agent', 'xpc.activity'
            ]
        }
        
        # Seuils de détection
        self.thresholds = {
            'cpu_usage': 90,      # % CPU suspect
            'memory_usage': 80,   # % RAM suspect
            'network_connections': 50,  # Nb connexions suspectes (réduit)
            'cpu_duration': 30    # Durée CPU élevé en secondes
        }
    
    def start_monitoring(self):
        """Démarrer la surveillance heuristique"""
        if self.monitoring:
            self.log("⚠️ Scanner heuristique déjà actif")
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.log("🔍 Scanner heuristique démarré")
    
    def stop_monitoring(self):
        """Arrêter la surveillance"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        self.log("🛑 Scanner heuristique arrêté")
    
    def scan_file(self, file_path):
        """Scanner un fichier spécifique"""
        threat_score = 0
        issues = []
        
        try:
            # Vérifier l'existence du fichier
            if not os.path.exists(file_path):
                return {"threat_score": 0, "issues": ["Fichier non trouvé"]}
            
            # Scanner les patterns suspects dans le nom
            filename = os.path.basename(file_path).lower()
            for pattern in self.suspicious_patterns['files']:
                if pattern in filename:
                    threat_score += 2
                    issues.append(f"Nom suspect: {pattern}")
            
            # Vérifier les permissions suspectes
            stat = os.stat(file_path)
            if stat.st_mode & 0o111:  # Exécutable
                threat_score += 1
                issues.append("Fichier exécutable")
                
            return {"threat_score": min(threat_score, 10), "issues": issues}
            
        except Exception as e:
            return {"threat_score": 0, "issues": [f"Erreur scan: {e}"]}
    
    def scan_processes(self):
        """Scanner les processus en cours"""
        suspicious = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    name = proc.info['name'].lower()
                    for pattern in self.suspicious_patterns['processes']:
                        if pattern in name:
                            suspicious.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'reason': f"Nom suspect: {pattern}"
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.log(f"Erreur scan processus: {e}")
        
        return suspicious
    
    def get_alerts(self):
        """Obtenir les alertes du monitoring"""
        all_alerts = []
        all_alerts.extend(self.alerts)
        all_alerts.extend(self.suspicious_processes)
        all_alerts.extend(self.suspicious_files)
        return all_alerts

    def get_scan_results(self):
        """Obtenir les résultats formatés pour l'interface"""
        return {
            'monitoring_active': self.monitoring,
            'scan_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'suspicious_processes': self.suspicious_processes,
            'suspicious_files': self.suspicious_files,
            'alerts': self.alerts,
            'total_alerts': len(self.alerts) + len(self.suspicious_processes) + len(self.suspicious_files)
        }

    def _monitor_loop(self):
        """Boucle principale de monitoring"""
        while self.monitoring:
            try:
                # Scanner les processus
                self._scan_processes()
                
                # Scanner les ressources système
                self._monitor_system_resources()
                
                # Scanner l'activité réseau
                self._scan_network_activity()
                
                # Attendre avant le prochain scan
                time.sleep(5)
                
            except Exception as e:
                self.log(f"Erreur monitoring: {e}")
                time.sleep(5)

    def _scan_processes(self):
        """Scanner les processus suspects"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    name = proc.info['name'].lower()
                    
                    # Vérifier les noms suspects
                    for pattern in self.suspicious_patterns['processes']:
                        if pattern in name:
                            alert = {
                                'type': 'suspicious_process',
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'reason': f"Processus suspect détecté: {pattern}",
                                'timestamp': datetime.now().isoformat()
                            }
                            if alert not in self.suspicious_processes:
                                self.suspicious_processes.append(alert)
                                self.log(f"⚠️ Processus suspect: {proc.info['name']} (PID: {proc.info['pid']})")
                                # Prendre action
                                self._take_action_on_threat('suspicious_process', alert)
                    
                    # Vérifier l'usage anormal des ressources
                    cpu_percent = proc.info['cpu_percent'] or 0
                    if cpu_percent > self.thresholds['cpu_usage']:
                        alert = {
                            'type': 'high_cpu',
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cpu_percent': cpu_percent,
                            'reason': f"Usage CPU élevé: {cpu_percent:.1f}%",
                            'timestamp': datetime.now().isoformat()
                        }
                        if alert not in self.alerts:
                            self.alerts.append(alert)
                            # Prendre action pour CPU élevé
                            self._take_action_on_threat('high_cpu_process', alert)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.log(f"Erreur scan processus: {e}")

    def _monitor_system_resources(self):
        """Surveiller l'utilisation des ressources système"""
        try:
            # Vérifier la RAM
            memory = psutil.virtual_memory()
            if memory.percent > self.thresholds['memory_usage']:
                alert = {
                    'type': 'high_memory',
                    'value': memory.percent,
                    'reason': f"Usage mémoire élevé: {memory.percent:.1f}%",
                    'timestamp': datetime.now().isoformat()
                }
                if alert not in self.alerts:
                    self.alerts.append(alert)
            
            # Vérifier le CPU global
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.thresholds['cpu_usage']:
                alert = {
                    'type': 'high_cpu_global',
                    'value': cpu_percent,
                    'reason': f"Usage CPU global élevé: {cpu_percent:.1f}%",
                    'timestamp': datetime.now().isoformat()
                }
                if alert not in self.alerts:
                    self.alerts.append(alert)
                    
        except Exception as e:
            self.log(f"Erreur monitoring ressources: {e}")

    def _scan_network_activity(self):
        """Scanner l'activité réseau suspecte"""
        try:
            connections = psutil.net_connections()
            active_connections = [c for c in connections if c.status == 'ESTABLISHED']
            
            if len(active_connections) > self.thresholds['network_connections']:
                alert = {
                    'type': 'high_network_activity',
                    'connections': len(active_connections),
                    'reason': f"Nombre élevé de connexions: {len(active_connections)}",
                    'timestamp': datetime.now().isoformat()
                }
                if alert not in self.alerts:
                    self.alerts.append(alert)
                    # Prendre action pour activité réseau élevée
                    self._take_action_on_threat('high_network_activity', alert)
                    
        except Exception as e:
            self.log(f"Erreur scan réseau: {e}")

    def clear_results(self):
        """Effacer tous les résultats et alertes"""
        self.suspicious_processes.clear()
        self.suspicious_files.clear()
        self.alerts.clear()
        self.log("🗑️ Résultats du scanner effacés")

    def _is_system_file_safe(self, file_path):
        """Vérifier si un fichier système est sûr (à ignorer)"""
        filename = os.path.basename(file_path).lower()
        for pattern in self.suspicious_patterns['ignore_system_files']:
            if pattern in filename:
                return True
        return False

    def _take_action_on_threat(self, threat_type, threat_data):
        """Prendre une action automatique contre une menace"""
        if not self.auto_actions:
            return False
            
        try:
            if threat_type == 'high_cpu_process':
                pid = threat_data.get('pid')
                name = threat_data.get('name', 'unknown')
                
                # Ne pas tuer les processus système critiques
                if name.lower() in ['kernel_task', 'launchd', 'windowserver', 'finder']:
                    self.log(f"🛡️ Processus système protégé: {name}")
                    return False
                
                # Avertissement pour les processus gourmands
                if threat_data.get('cpu_percent', 0) > 95:
                    self.log(f"⚠️ ACTION: Processus {name} (PID {pid}) consomme {threat_data.get('cpu_percent'):.1f}% CPU")
                    self.log(f"💡 CONSEIL: Vérifiez si {name} est nécessaire")
                    return True
                    
            elif threat_type == 'suspicious_file':
                file_path = threat_data.get('path', '')
                
                # Ignorer les fichiers système sûrs
                if self._is_system_file_safe(file_path):
                    return False
                    
                # Actions pour fichiers suspects
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    self.log(f"🔍 ANALYSE: Fichier suspect {file_path} ({size} bytes)")
                    
                    # Si petit fichier dans un dossier temporaire, on peut le signaler
                    if '/tmp/' in file_path or size < 1024:
                        self.log(f"⚠️ Fichier temporaire suspect détecté")
                        return True
                        
            elif threat_type == 'high_network_activity':
                connections = threat_data.get('connections', 0)
                self.log(f"🌐 ACTION: {connections} connexions réseau détectées")
                self.log(f"💡 CONSEIL: Vérifiez les applications qui utilisent internet")
                return True
                
        except Exception as e:
            self.log(f"❌ Erreur action automatique: {e}")
            
        return False

    def enable_auto_actions(self, enabled=True):
        """Activer/désactiver les actions automatiques"""
        self.auto_actions = enabled
        status = "activées" if enabled else "désactivées"
        self.log(f"🔧 Actions automatiques {status}")

# Test autonome
if __name__ == "__main__":
    def test_log(msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    
    print("🧪 Test du Scanner Heuristique")
    scanner = HeuristicScanner(test_log)
    
    # Test scan de fichier
    result = scanner.scan_file("/usr/bin/python3")
    print(f"📊 Scan fichier: {result}")
    
    # Test scan processus
    processes = scanner.scan_processes()
    print(f"📊 Processus suspects: {len(processes)}")
    
    # Test monitoring bref
    scanner.start_monitoring()
    time.sleep(3)
    alerts = scanner.get_alerts()
    scanner.stop_monitoring()
    print(f"📊 Alertes: {len(alerts)}")
    
    print("✅ Test terminé")