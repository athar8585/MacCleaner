#!/usr/bin/env python3
"""
Script de tests pour MacCleaner Pro
Lance tous les tests unitaires et affiche un rapport
"""

import unittest
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """Découvrir et lancer tous les tests"""
    print("🧪 MacCleaner Pro - Suite de Tests")
    print("=" * 50)
    
    # Découvrir tous les tests dans le répertoire tests/
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    
    try:
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        # Lancer les tests avec un runner détaillé
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print(f"✅ Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"❌ Échecs: {len(result.failures)}")
        print(f"🚨 Erreurs: {len(result.errors)}")
        print(f"⏭️ Ignorés: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\n❌ ÉCHECS:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\n🚨 ERREURS:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
        
        # Code de sortie
        success = len(result.failures) == 0 and len(result.errors) == 0
        if success:
            print("\n🎉 Tous les tests sont passés!")
            return 0
        else:
            print(f"\n⚠️ {len(result.failures + result.errors)} test(s) ont échoué")
            return 1
    
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        return 2

def run_specific_test(test_name):
    """Lancer un test spécifique"""
    print(f"🧪 Lancement du test: {test_name}")
    
    try:
        # Charger et lancer le test spécifique
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(test_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
    
    except Exception as e:
        print(f"❌ Erreur test spécifique: {e}")
        return 2

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test spécifique
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Tous les tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)