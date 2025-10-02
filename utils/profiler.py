#!/usr/bin/env python3
"""
Module de profiling performance pour MacCleaner Pro
Mesure CPU/disque/mémoire avant/après nettoyage
"""

import psutil
import time
import json
from datetime import datetime
from pathlib import Path

class PerformanceProfiler:
    """Profileur de performance système"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start_metrics = {}
        self.end_metrics = {}
        self.profile_data = {}
    
    def start_profiling(self):
        """Démarrer le profiling"""
        self.start_time = time.time()
        self.start_metrics = self._get_system_metrics()
        print(f"📊 Profiling démarré à {datetime.now().strftime('%H:%M:%S')}")
    
    def stop_profiling(self):
        """Arrêter le profiling"""
        self.end_time = time.time()
        self.end_metrics = self._get_system_metrics()
        self._calculate_differences()
        print(f"📊 Profiling terminé à {datetime.now().strftime('%H:%M:%S')}")
        return self.get_summary()
    
    def _get_system_metrics(self):
        """Collecter les métriques système actuelles"""
        try:
            # Métriques CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Métriques mémoire
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Métriques disque
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Métriques réseau
            net_io = psutil.net_io_counters()
            
            # Processus
            process_count = len(psutil.pids())
            
            return {
                'timestamp': time.time(),
                'cpu': {
                    'percent': cpu_percent,
                    'freq_current': cpu_freq.current if cpu_freq else 0,
                    'count': cpu_count
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'percent': swap.percent
                },
                'disk': {
                    'total': disk_usage.total,
                    'used': disk_usage.used,
                    'free': disk_usage.free,
                    'read_bytes': disk_io.read_bytes if disk_io else 0,
                    'write_bytes': disk_io.write_bytes if disk_io else 0,
                    'read_count': disk_io.read_count if disk_io else 0,
                    'write_count': disk_io.write_count if disk_io else 0
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent if net_io else 0,
                    'bytes_recv': net_io.bytes_recv if net_io else 0,
                    'packets_sent': net_io.packets_sent if net_io else 0,
                    'packets_recv': net_io.packets_recv if net_io else 0
                },
                'processes': process_count
            }
        except Exception as e:
            print(f"⚠️ Erreur collecte métriques: {e}")
            return {}
    
    def _calculate_differences(self):
        """Calculer les différences avant/après"""
        if not self.start_metrics or not self.end_metrics:
            return
        
        duration = self.end_time - self.start_time
        
        # Différences mémoire
        memory_freed = self.start_metrics['memory']['used'] - self.end_metrics['memory']['used']
        memory_percent_change = self.end_metrics['memory']['percent'] - self.start_metrics['memory']['percent']
        
        # Différences disque
        disk_freed = self.start_metrics['disk']['used'] - self.end_metrics['disk']['used']
        disk_reads = self.end_metrics['disk']['read_count'] - self.start_metrics['disk']['read_count']
        disk_writes = self.end_metrics['disk']['write_count'] - self.start_metrics['disk']['write_count']
        
        # Différences CPU (moyennes)
        avg_cpu_start = self.start_metrics['cpu']['percent']
        avg_cpu_end = self.end_metrics['cpu']['percent']
        
        # Différences processus
        process_change = self.end_metrics['processes'] - self.start_metrics['processes']
        
        self.profile_data = {
            'duration_seconds': round(duration, 2),
            'memory': {
                'freed_bytes': memory_freed,
                'freed_mb': round(memory_freed / (1024*1024), 2),
                'percent_change': round(memory_percent_change, 2)
            },
            'disk': {
                'freed_bytes': disk_freed,
                'freed_mb': round(disk_freed / (1024*1024), 2),
                'reads_during_clean': disk_reads,
                'writes_during_clean': disk_writes
            },
            'cpu': {
                'start_percent': avg_cpu_start,
                'end_percent': avg_cpu_end,
                'change_percent': round(avg_cpu_end - avg_cpu_start, 2)
            },
            'processes': {
                'start_count': self.start_metrics['processes'],
                'end_count': self.end_metrics['processes'],
                'change': process_change
            }
        }
    
    def get_summary(self):
        """Obtenir résumé du profiling"""
        if not self.profile_data:
            return "Aucune donnée de profiling disponible"
        
        summary = []
        summary.append(f"⏱️ Durée: {self.profile_data['duration_seconds']}s")
        summary.append(f"🧠 Mémoire libérée: {self.profile_data['memory']['freed_mb']} MB ({self.profile_data['memory']['percent_change']:+.1f}%)")
        summary.append(f"💾 Espace disque libéré: {self.profile_data['disk']['freed_mb']} MB")
        summary.append(f"💻 CPU: {self.profile_data['cpu']['start_percent']:.1f}% → {self.profile_data['cpu']['end_percent']:.1f}% ({self.profile_data['cpu']['change_percent']:+.1f}%)")
        summary.append(f"⚙️ Processus: {self.profile_data['processes']['change']:+d}")
        summary.append(f"📁 I/O: {self.profile_data['disk']['reads_during_clean']} lectures, {self.profile_data['disk']['writes_during_clean']} écritures")
        
        return "\n".join(summary)
    
    def export_to_file(self, filepath):
        """Exporter les données vers un fichier JSON"""
        try:
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'start_metrics': self.start_metrics,
                'end_metrics': self.end_metrics,
                'profile_summary': self.profile_data
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"📊 Profil exporté: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Erreur export profil: {e}")
            return False
    
    def get_detailed_report(self):
        """Générer rapport détaillé HTML"""
        if not self.profile_data:
            return "<p>Aucune donnée de profiling</p>"
        
        html = f"""
        <div class="performance-report">
            <h3>📊 Rapport de Performance</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>⏱️ Temps d'exécution</h4>
                    <span class="metric-value">{self.profile_data['duration_seconds']}s</span>
                </div>
                <div class="metric-card">
                    <h4>🧠 Mémoire</h4>
                    <span class="metric-value">{self.profile_data['memory']['freed_mb']} MB libérés</span>
                    <span class="metric-change {('positive' if self.profile_data['memory']['percent_change'] < 0 else 'negative')}">{self.profile_data['memory']['percent_change']:+.1f}%</span>
                </div>
                <div class="metric-card">
                    <h4>💾 Disque</h4>
                    <span class="metric-value">{self.profile_data['disk']['freed_mb']} MB libérés</span>
                </div>
                <div class="metric-card">
                    <h4>💻 CPU</h4>
                    <span class="metric-value">{self.profile_data['cpu']['start_percent']:.1f}% → {self.profile_data['cpu']['end_percent']:.1f}%</span>
                    <span class="metric-change {('negative' if self.profile_data['cpu']['change_percent'] > 0 else 'positive')}">{self.profile_data['cpu']['change_percent']:+.1f}%</span>
                </div>
            </div>
        </div>
        """
        return html