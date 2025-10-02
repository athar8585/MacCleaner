#!/usr/bin/env python3
"""
Tests unitaires pour le module d'intégrité
"""

import unittest
import tempfile
import os
import json
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.integrity import hash_file, generate_manifest, verify_paths, load_hash_manifest

class TestIntegrity(unittest.TestCase):
    
    def setUp(self):
        """Préparer les fichiers de test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        self.manifest_file = os.path.join(self.test_dir, 'hashes.json')
        
        # Créer un fichier de test
        with open(self.test_file, 'w') as f:
            f.write('Hello MacCleaner Pro!')
    
    def tearDown(self):
        """Nettoyer après les tests"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_hash_file(self):
        """Tester le calcul de hash"""
        hash1 = hash_file(self.test_file)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA-256
        
        # Hash du même fichier doit être identique
        hash2 = hash_file(self.test_file)
        self.assertEqual(hash1, hash2)
    
    def test_hash_nonexistent_file(self):
        """Tester hash sur fichier inexistant"""
        hash_result = hash_file('/nonexistent/file.txt')
        self.assertEqual(hash_result, '')
    
    def test_generate_manifest(self):
        """Tester génération de manifeste"""
        rel_path = os.path.relpath(self.test_file, self.test_dir)
        generate_manifest([rel_path], self.test_dir, self.manifest_file)
        
        self.assertTrue(os.path.exists(self.manifest_file))
        
        manifest = load_hash_manifest(self.manifest_file)
        self.assertIn(rel_path, manifest)
        self.assertEqual(len(manifest[rel_path]), 64)
    
    def test_verify_paths_ok(self):
        """Tester vérification avec fichiers OK"""
        rel_path = os.path.relpath(self.test_file, self.test_dir)
        generate_manifest([rel_path], self.test_dir, self.manifest_file)
        
        results = verify_paths([rel_path], self.test_dir)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]['ok'])
    
    def test_verify_paths_altered(self):
        """Tester vérification avec fichier modifié"""
        rel_path = os.path.relpath(self.test_file, self.test_dir)
        generate_manifest([rel_path], self.test_dir, self.manifest_file)
        
        # Modifier le fichier
        with open(self.test_file, 'a') as f:
            f.write(' MODIFIED')
        
        results = verify_paths([rel_path], self.test_dir)
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0]['ok'])

if __name__ == '__main__':
    unittest.main()