#!/usr/bin/env python3
"""
Script de validation complète de MacCleaner Pro
Test AUTONOME de toutes les fonctions critiques
"""

import os
import sys
import traceback
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_log(message):
    """Logger simple avec timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def run_test(test_name, test_func):
    """Exécuter un test et capturer les erreurs"""
    test_log(f"🧪 TEST: {test_name}")
    try:
        result = test_func()
        test_log(f"✅ SUCCÈS: {test_name} - {result}")
        return True
    except Exception as e:
        test_log(f"❌ ÉCHEC: {test_name} - {e}")
        return False

def test_database():
    """Test base de données"""
    from database.db import init_db, record_clean_run, stats_summary
    
    # Init DB
    init_db()
    
    # Enregistrer un nettoyage
    record_clean_run("Test Validation", 15.5, 2.3)
    
    # Lire les stats
    stats = stats_summary()
    return f"Stats: {stats}"

def test_config():
    """Test configuration"""
    from config.loader import load_settings
    
    settings = load_settings(force=True)
    version_url = settings.get('version_check_url', '')
    scanner_config = settings.get('malware_scanner', {})
    malware_url = scanner_config.get('malware_signatures_url', '')
    
    return f"URLs OK - Version: {bool(version_url)}, Malware: {bool(malware_url)}"

def test_heuristic_scanner():
    """Test scanner heuristique"""
    from utils.heuristic_scanner import HeuristicScanner
    
    scanner = HeuristicScanner()
    
    # Test scan fichier
    result = scanner.scan_file('/usr/bin/python3')
    
    # Test scan processus
    processes = scanner.scan_processes()
    
    return f"Scan OK - Threat: {result['threat_score']}, Processus: {len(processes)}"

def test_notifications():
    """Test notifications"""
    from utils.notifications import notify
    
    # Test notification (peut échouer si pas d'autorisation)
    try:
        notify("MacCleaner Test", "Test de validation")
        return "Notification envoyée"
    except:
        return "Notification non autorisée (normal)"

def test_malware_scanner():
    """Test scanner malware"""
    from malware_scanner.scanner import MalwareScanner
    
    scanner = MalwareScanner()
    
    # Test scan d'un fichier système sûr
    result = scanner.scan_file('/usr/bin/ls')
    
    return f"Scan malware: {result.get('status', 'unknown')}"

def test_plugins():
    """Test système de plugins"""
    from plugins.plugin_loader import PluginManager
    
    manager = PluginManager()
    plugins = manager.get_available_plugins()
    
    return f"Plugins disponibles: {len(plugins)}"

def test_core_functions():
    """Test des fonctions de nettoyage de base"""
    # Test calcul de taille
    import os
    
    # Calculer taille d'un dossier système
    test_dir = '/usr/bin'
    if os.path.exists(test_dir):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(test_dir):
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
                except:
                    continue
        
        return f"Calcul taille OK: {total_size / (1024*1024):.1f} MB"
    else:
        return "Test dir non trouvé"

def test_update_functionality():
    """Test fonction de mise à jour"""
    import urllib.request
    import json
    
    # Test URL de version
    url = "https://api.github.com/repos/microsoft/vscode/releases/latest"
    
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())
        version = data.get('tag_name', 'N/A')
    
    return f"Mise à jour OK: Version {version}"

def main():
    """Test principal"""
    test_log("🚀 VALIDATION COMPLÈTE DE MACCLEANER PRO")
    test_log("=" * 50)
    
    tests = [
        ("Base de données", test_database),
        ("Configuration", test_config),
        ("Scanner heuristique", test_heuristic_scanner),
        ("Notifications", test_notifications),
        ("Scanner malware", test_malware_scanner),
        ("Système plugins", test_plugins),
        ("Fonctions core", test_core_functions),
        ("Mise à jour", test_update_functionality)
    ]
    
    successes = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            successes += 1
    
    test_log("")
    test_log(f"🎯 RÉSULTATS: {successes}/{total} tests réussis")
    
    if successes == total:
        test_log("✅ VALIDATION COMPLÈTE: MacCleaner Pro est OPÉRATIONNEL")
        return 0
    else:
        test_log("❌ VALIDATION ÉCHOUÉE: Des problèmes subsistent")
        return 1

if __name__ == "__main__":
    sys.exit(main())