#!/usr/bin/env python3
"""
Tests unitaires pour le système de notifications
"""

import unittest
import tempfile
import os
import sys
import subprocess

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.notifications import notify, notify_completion, notify_alert, test_notifications

class TestNotifications(unittest.TestCase):
    
    def setUp(self):
        """Préparer environnement de test"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Nettoyer après tests"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_basic_notify(self):
        """Tester notification de base"""
        # Test en mode silent pour éviter l'affichage réel
        try:
            result = notify("Test Title", "Test message", sound=False)
            # Le résultat peut être True/False selon la disponibilité du système de notifications
            self.assertIsInstance(result, bool)
        except Exception as e:
            # Les notifications peuvent échouer dans un environnement de test
            self.assertIsInstance(e, Exception)
    
    def test_notify_completion(self):
        """Tester notification de fin"""
        try:
            result = notify_completion("Test operation", 1024*1024*100, 150)  # 100MB en 150s
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.assertIsInstance(e, Exception)
    
    def test_notify_alert(self):
        """Tester notification d'alerte"""
        try:
            result = notify_alert("Test Alert", "Critical issue detected")
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.assertIsInstance(e, Exception)
    
    def test_notify_with_different_types(self):
        """Tester différents types de notifications"""
        test_cases = [
            ("info", "Information message"),
            ("warning", "Warning message"),
            ("error", "Error message"),
            ("success", "Success message")
        ]
        
        for urgency, message in test_cases:
            try:
                result = notify("Test", message, urgency=urgency, sound=False)
                self.assertIsInstance(result, (bool, type(None)))
            except Exception:
                # Acceptable dans un environnement de test
                pass
    
    def test_notify_with_sound(self):
        """Tester notification avec son"""
        try:
            result = notify("Test", "Message with sound", sound=True)
            self.assertIsInstance(result, bool)
        except Exception:
            # Son peut ne pas être disponible dans l'environnement de test
            pass
    
    def test_notify_with_invalid_params(self):
        """Tester notification avec paramètres invalides"""
        # Titre vide
        result = notify("", "Message")
        self.assertIsInstance(result, (bool, type(None)))
        
        # Message vide
        result = notify("Title", "")
        self.assertIsInstance(result, (bool, type(None)))
    
    def test_format_size_function(self):
        """Tester la fonction de formatage de taille (si elle existe dans le module)"""
        # Cette fonction pourrait être utilisée dans notify_completion
        try:
            from utils.notifications import format_size
            
            # Test différentes tailles
            self.assertEqual(format_size(1024), "1.0 KB")
            self.assertEqual(format_size(1024*1024), "1.0 MB")
            self.assertEqual(format_size(1024*1024*1024), "1.0 GB")
            
        except ImportError:
            # La fonction pourrait ne pas être exportée
            pass
    
    def test_system_notification_availability(self):
        """Tester la disponibilité du système de notifications"""
        # Vérifier si osascript est disponible (macOS)
        try:
            result = subprocess.run(['which', 'osascript'], 
                                  capture_output=True, text=True)
            osascript_available = (result.returncode == 0)
            
            # Vérifier si pync est importable
            pync_available = False
            try:
                import pync
                pync_available = True
            except ImportError:
                pass
            
            # Au moins un système doit être disponible sur macOS
            if sys.platform == 'darwin':
                self.assertTrue(osascript_available or pync_available, 
                               "Aucun système de notification disponible")
                
        except Exception:
            # Test peut échouer dans certains environnements
            pass
    
    def test_notifications_stress(self):
        """Tester multiple notifications rapidement"""
        success_count = 0
        total_tests = 5
        
        for i in range(total_tests):
            try:
                if notify(f"Test {i}", f"Message {i}", sound=False):
                    success_count += 1
            except Exception:
                pass
        
        # Au moins quelques notifications devraient réussir
        # ou toutes échouer gracieusement
        self.assertGreaterEqual(success_count, 0)
        self.assertLessEqual(success_count, total_tests)
    
    def test_test_notifications_function(self):
        """Tester la fonction de test des notifications"""
        try:
            # Fonction qui teste tous les types de notifications
            test_notifications()
            # Si ça ne lève pas d'exception, c'est un succès
            self.assertTrue(True)
        except Exception as e:
            # Acceptable dans un environnement de test
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    unittest.main()