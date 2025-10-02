#!/usr/bin/env python3
"""
Script de test de l'application MacCleaner Pro
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_modules():
    """Tester l'import de tous les modules"""
    print("🧪 Test des imports de modules...")
    
    modules_to_test = [
        'mac_cleaner',
        'utils.heuristic',
        'utils.notifications', 
        'utils.profiler',
        'utils.integrity',
        'plugins.plugin_loader'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {e}")
            return False
    
    return True

def test_basic_functionality():
    """Tester les fonctionnalités de base"""
    print("\n🔧 Test des fonctionnalités de base...")
    
    try:
        # Test scanner heuristique
        from utils.heuristic import HeuristicScanner
        scanner = HeuristicScanner()
        print("  ✅ HeuristicScanner")
        
        # Test notifications
        from utils.notifications import notify
        # Test silencieux
        result = notify("Test", "Application test", sound=False)
        print(f"  ✅ Notifications: {result}")
        
        # Test profiler
        from utils.profiler import PerformanceProfiler
        profiler = PerformanceProfiler()
        print("  ✅ PerformanceProfiler")
        
        # Test plugin manager
        from plugins.plugin_loader import PluginManager
        plugin_manager = PluginManager(log_fn=print)
        print(f"  ✅ PluginManager: {len(plugin_manager.plugins)} plugins")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_application_components():
    """Tester les composants principaux de l'application"""
    print("\n🖥️ Test des composants de l'application...")
    
    try:
        import mac_cleaner
        
        # Test d'import de la classe principale
        app_class = getattr(mac_cleaner, 'MacCleanerPro', None)
        if app_class:
            print("  ✅ Classe MacCleanerPro trouvée")
        else:
            print("  ❌ Classe MacCleanerPro non trouvée")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def main():
    """Test principal"""
    print("🚀 MacCleaner Pro - Tests de Distribution")
    print("=" * 50)
    
    tests = [
        test_modules,
        test_basic_functionality,
        test_application_components
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS")
    
    if all(results):
        print("🎉 Tous les tests sont passés!")
        print("✅ L'application est prête pour la distribution")
        return 0
    else:
        print("❌ Certains tests ont échoué")
        print("⚠️ L'application nécessite des corrections")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)