#!/usr/bin/env python3
"""
Tests unitaires pour le module de surveillance heuristique
"""

import unittest
import tempfile
import time
import threading
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.heuristic import HeuristicScanner

class TestHeuristicScanner(unittest.TestCase):
    
    def setUp(self):
        """Préparer environnement de test"""
        self.test_dir = tempfile.mkdtemp()
        self.log_messages = []
        
        def test_log(msg):
            self.log_messages.append(msg)
        
        self.scanner = HeuristicScanner(log_callback=test_log)
    
    def tearDown(self):
        """Nettoyer après tests"""
        if self.scanner.monitoring:
            self.scanner.stop_monitoring()
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_scanner_initialization(self):
        """Tester l'initialisation du scanner"""
        self.assertFalse(self.scanner.monitoring)
        self.assertIsNotNone(self.scanner.alerts)
        self.assertEqual(len(self.scanner.alerts), 0)
        self.assertGreater(len(self.scanner.sensitive_paths), 0)
    
    def test_start_stop_monitoring(self):
        """Tester démarrage/arrêt de la surveillance"""
        # Démarrer surveillance
        self.scanner.start_monitoring()
        self.assertTrue(self.scanner.monitoring)
        self.assertIsNotNone(self.scanner.monitor_thread)
        
        # Arrêter surveillance
        self.scanner.stop_monitoring()
        self.assertFalse(self.scanner.monitoring)
        
        # Vérifier messages de log
        self.assertTrue(any('Surveillance heuristique démarrée' in msg for msg in self.log_messages))
        self.assertTrue(any('Surveillance heuristique arrêtée' in msg for msg in self.log_messages))
    
    def test_suspicious_name_detection(self):
        """Tester détection de noms suspects"""
        self.assertTrue(self.scanner._is_suspicious_name('launch_agent.plist'))
        self.assertTrue(self.scanner._is_suspicious_name('keylogger.app'))
        self.assertTrue(self.scanner._is_suspicious_name('backdoor_daemon.py'))
        self.assertFalse(self.scanner._is_suspicious_name('normal_file.txt'))
        self.assertFalse(self.scanner._is_suspicious_name('document.pdf'))
    
    def test_alert_creation(self):
        """Tester création d'alertes"""
        initial_count = len(self.scanner.alerts)
        
        self.scanner._create_alert('test_type', 'Test alert message', {'key': 'value'})
        
        self.assertEqual(len(self.scanner.alerts), initial_count + 1)
        alert = self.scanner.alerts[-1]
        self.assertEqual(alert['type'], 'test_type')
        self.assertEqual(alert['message'], 'Test alert message')
        self.assertEqual(alert['metadata']['key'], 'value')
        self.assertIn('timestamp', alert)
    
    def test_get_alerts(self):
        """Tester récupération d'alertes récentes"""
        # Créer quelques alertes
        self.scanner._create_alert('type1', 'Alert 1')
        self.scanner._create_alert('type2', 'Alert 2')
        
        recent_alerts = self.scanner.get_alerts(24)
        self.assertGreaterEqual(len(recent_alerts), 2)
    
    def test_get_summary(self):
        """Tester résumé de surveillance"""
        self.scanner._create_alert('cpu_anomaly', 'Test CPU alert')
        self.scanner._create_alert('suspicious_file', 'Test file alert')
        
        summary = self.scanner.get_summary()
        
        self.assertIn('monitoring', summary)
        self.assertIn('total_alerts_24h', summary)
        self.assertIn('alert_types', summary)
        self.assertIn('monitored_processes', summary)
        self.assertIn('monitored_paths', summary)
        
        self.assertGreaterEqual(summary['total_alerts_24h'], 2)
        self.assertIn('cpu_anomaly', summary['alert_types'])
        self.assertIn('suspicious_file', summary['alert_types'])
    
    def test_export_alerts(self):
        """Tester export d'alertes"""
        self.scanner._create_alert('test', 'Export test alert')
        
        export_file = os.path.join(self.test_dir, 'alerts_export.json')
        result = self.scanner.export_alerts(export_file)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(export_file))
        
        # Vérifier le contenu
        import json
        with open(export_file, 'r') as f:
            exported_alerts = json.load(f)
        
        self.assertIsInstance(exported_alerts, list)
        self.assertGreater(len(exported_alerts), 0)
    
    def test_monitoring_double_start(self):
        """Tester double démarrage de surveillance"""
        self.scanner.start_monitoring()
        initial_log_count = len(self.log_messages)
        
        # Tenter un second démarrage
        self.scanner.start_monitoring()
        
        # Doit afficher un avertissement
        self.assertTrue(any('Surveillance déjà active' in msg for msg in self.log_messages[initial_log_count:]))

if __name__ == '__main__':
    unittest.main()