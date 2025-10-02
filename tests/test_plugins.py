#!/usr/bin/env python3
"""
Tests unitaires pour le système de plugins
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.plugin_loader import PluginManager

class TestPluginSystem(unittest.TestCase):
    
    def setUp(self):
        """Préparer environnement de test"""
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = os.path.join(self.test_dir, 'test_plugins')
        os.makedirs(self.plugin_dir)
        
        # Créer un plugin de test
        self.test_plugin_content = '''
def run(log):
    """Plugin de test"""
    log("Test plugin exécuté")
    return 1024  # 1KB libéré
'''
        
        test_plugin_path = os.path.join(self.plugin_dir, 'test_cleanup.py')
        with open(test_plugin_path, 'w') as f:
            f.write(self.test_plugin_content)
    
    def tearDown(self):
        """Nettoyer après tests"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_plugin_discovery(self):
        """Tester découverte des plugins"""
        log_messages = []
        def test_log(msg):
            log_messages.append(msg)
        
        manager = PluginManager(self.plugin_dir, test_log)
        
        self.assertIn('test', manager.plugins)
        self.assertTrue(hasattr(manager.plugins['test'], 'run'))
    
    def test_plugin_execution(self):
        """Tester exécution d'un plugin"""
        log_messages = []
        def test_log(msg):
            log_messages.append(msg)
        
        manager = PluginManager(self.plugin_dir, test_log)
        
        # Exécuter le plugin
        result = manager.plugins['test'].run(test_log)
        
        self.assertEqual(result, 1024)
        self.assertTrue(any('Test plugin exécuté' in msg for msg in log_messages))
    
    def test_plugin_error_handling(self):
        """Tester gestion d'erreurs dans plugins"""
        # Créer un plugin défaillant
        error_plugin_path = os.path.join(self.plugin_dir, 'error_cleanup.py')
        with open(error_plugin_path, 'w') as f:
            f.write('def run(log):\n    raise ValueError("Plugin test error")\n')
        
        log_messages = []
        def test_log(msg):
            log_messages.append(msg)
        
        manager = PluginManager(self.plugin_dir, test_log)
        
        # Le plugin défaillant doit être chargé mais son exécution doit être gérée
        self.assertIn('test', manager.plugins)
        self.assertIn('error', manager.plugins)
    
    def test_empty_plugin_dir(self):
        """Tester avec répertoire vide"""
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir)
        
        log_messages = []
        def test_log(msg):
            log_messages.append(msg)
        
        manager = PluginManager(empty_dir, test_log)
        self.assertEqual(len(manager.plugins), 0)

if __name__ == '__main__':
    unittest.main()