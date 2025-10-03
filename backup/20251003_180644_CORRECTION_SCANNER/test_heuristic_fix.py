#!/usr/bin/env python3
"""
Test de validation de la correction du scanner heuristique
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.heuristic_scanner import HeuristicScanner

def test_heuristic_scanner():
    """Tester toutes les méthodes du scanner heuristique"""
    print("🧪 === TEST SCANNER HEURISTIQUE CORRIGÉ ===")
    
    # Test 1: Création du scanner
    try:
        scanner = HeuristicScanner()
        print("✅ Test 1: Création du scanner - OK")
    except Exception as e:
        print(f"❌ Test 1: Erreur création - {e}")
        return False
    
    # Test 2: Méthode get_scan_results()
    try:
        results = scanner.get_scan_results()
        assert isinstance(results, dict), "Résultats doivent être un dictionnaire"
        assert 'monitoring_active' in results, "Clé monitoring_active manquante"
        assert 'scan_timestamp' in results, "Clé scan_timestamp manquante"
        assert 'suspicious_processes' in results, "Clé suspicious_processes manquante"
        assert 'suspicious_files' in results, "Clé suspicious_files manquante"
        assert 'alerts' in results, "Clé alerts manquante"
        assert 'total_alerts' in results, "Clé total_alerts manquante"
        print("✅ Test 2: get_scan_results() format - OK")
    except Exception as e:
        print(f"❌ Test 2: Erreur format - {e}")
        return False
    
    # Test 3: Méthode get_alerts() (compatibilité)
    try:
        alerts = scanner.get_alerts()
        assert isinstance(alerts, list), "Alertes doivent être une liste"
        print("✅ Test 3: get_alerts() compatibilité - OK")
    except Exception as e:
        print(f"❌ Test 3: Erreur get_alerts - {e}")
        return False
    
    # Test 4: Scan de fichier
    try:
        file_result = scanner.scan_file("/usr/bin/python3")
        assert isinstance(file_result, dict), "Résultat scan fichier doit être un dict"
        assert 'threat_score' in file_result, "Score de menace manquant"
        assert 'issues' in file_result, "Issues manquantes"
        print("✅ Test 4: scan_file() - OK")
    except Exception as e:
        print(f"❌ Test 4: Erreur scan fichier - {e}")
        return False
    
    # Test 5: Scan des processus
    try:
        proc_result = scanner.scan_processes()
        assert isinstance(proc_result, list), "Résultat scan processus doit être une liste"
        print("✅ Test 5: scan_processes() - OK")
    except Exception as e:
        print(f"❌ Test 5: Erreur scan processus - {e}")
        return False
    
    # Test 6: Démarrage/arrêt monitoring
    try:
        scanner.start_monitoring()
        results_monitoring = scanner.get_scan_results()
        assert results_monitoring['monitoring_active'] == True, "Monitoring devrait être actif"
        
        scanner.stop_monitoring()
        results_stopped = scanner.get_scan_results()
        assert results_stopped['monitoring_active'] == False, "Monitoring devrait être arrêté"
        print("✅ Test 6: start/stop monitoring - OK")
    except Exception as e:
        print(f"❌ Test 6: Erreur monitoring - {e}")
        return False
    
    # Test 7: Clear results
    try:
        scanner.clear_results()
        cleared_results = scanner.get_scan_results()
        assert cleared_results['total_alerts'] == 0, "Alertes devraient être effacées"
        print("✅ Test 7: clear_results() - OK")
    except Exception as e:
        print(f"❌ Test 7: Erreur clear results - {e}")
        return False
    
    print("🎯 === TOUS LES TESTS RÉUSSIS ===")
    print("✅ Scanner heuristique entièrement opérationnel")
    print("✅ Correction de l'erreur 'get_scan_results' réussie")
    print("✅ Compatible avec l'interface MacCleaner Pro")
    
    return True

if __name__ == "__main__":
    success = test_heuristic_scanner()
    exit_code = 0 if success else 1
    sys.exit(exit_code)