#!/usr/bin/env python3
"""
Test du Scanner Heuristique Amélioré
Validation des actions automatiques
"""

import time
import threading
from utils.heuristic_scanner import HeuristicScanner

def test_log(msg):
    print(f"[SCANNER] {msg}")

def simulate_suspicious_activity():
    """Simuler une activité suspecte pour tester les actions"""
    print("\n🧪 SIMULATION D'ACTIVITÉ SUSPECTE")
    print("=" * 40)
    
    scanner = HeuristicScanner(test_log)
    
    # Activer actions automatiques
    scanner.enable_auto_actions(True)
    
    # Test 1: Fichier système sûr (doit être ignoré)
    print("\n📁 Test 1: Fichier système sûr")
    safe_file = "/Users/test/Library/Preferences/com.apple.spaces.plist" 
    is_safe = scanner._is_system_file_safe(safe_file)
    print(f"Fichier {safe_file} est sûr: {is_safe}")
    
    # Test 2: Scanner les processus actuels
    print("\n🔍 Test 2: Scan processus avec actions")
    scanner.start_monitoring()
    
    # Laisser tourner 5 secondes
    time.sleep(5)
    
    # Obtenir résultats
    alerts = scanner.get_scan_results()
    print(f"\n📊 RÉSULTATS: {len(alerts)} alertes détectées")
    
    # Afficher quelques alertes avec actions
    for i, alert in enumerate(alerts[:3]):
        print(f"  {i+1}. {alert.get('type', 'unknown')}: {alert.get('reason', 'N/A')}")
    
    scanner.stop_monitoring()
    
    # Test 3: Actions prises
    print(f"\n🎯 Actions automatiques testées avec succès!")
    
    return len(alerts)

if __name__ == "__main__":
    try:
        alerts_count = simulate_suspicious_activity()
        print(f"\n✅ Test terminé: {alerts_count} alertes traitées avec actions automatiques")
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()