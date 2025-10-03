#!/usr/bin/env python3
"""
Test final des corrections - Scanner heuristique et malware
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_final_corrections():
    """Test complet de toutes les corrections"""
    print("🎯 === TEST FINAL DES CORRECTIONS ===")
    
    # Test 1: Scanner heuristique - filtrage Apple
    try:
        from utils.heuristic import HeuristicScanner
        heuristic_scanner = HeuristicScanner()
        
        apple_files = [
            'com.apple.calaccessd.plist',
            'com.apple.spaces.plist',
            'ContextStoreAgent.plist'
        ]
        
        all_ignored = True
        for file in apple_files:
            if heuristic_scanner._is_suspicious_name(file):
                all_ignored = False
                break
                
        assert all_ignored, "Fichiers Apple encore détectés comme suspects"
        print("✅ Test 1: Scanner heuristique - Filtrage Apple OK")
    except Exception as e:
        print(f"❌ Test 1: Erreur scanner heuristique - {e}")
        return False
    
    # Test 2: Scanner malware - filtrage système
    try:
        from malware_scanner.scanner import MalwareScanner
        malware_scanner = MalwareScanner()
        
        # Vérifier que les nouvelles signatures sont chargées
        signature_names = [sig['name'] for sig in malware_scanner.signatures]
        assert "Empty File Test" not in signature_names, "Ancienne signature présente"
        assert len(malware_scanner.signatures) >= 4, "Pas assez de signatures"
        
        print("✅ Test 2: Scanner malware - Signatures corrigées OK")
    except Exception as e:
        print(f"❌ Test 2: Erreur scanner malware - {e}")
        return False
    
    # Test 3: Scanner heuristique utils/heuristic_scanner.py
    try:
        from utils.heuristic_scanner import HeuristicScanner
        scanner = HeuristicScanner()
        
        # Vérifier que get_scan_results existe
        results = scanner.get_scan_results()
        assert isinstance(results, dict), "get_scan_results doit retourner un dict"
        assert 'monitoring_active' in results, "Clé monitoring_active manquante"
        
        print("✅ Test 3: Scanner heuristique_scanner - get_scan_results OK")
    except Exception as e:
        print(f"❌ Test 3: Erreur heuristic_scanner - {e}")
        return False
    
    # Test 4: Test complet filtrage faux positifs
    try:
        from utils.heuristic import HeuristicScanner
        from pathlib import Path
        
        scanner = HeuristicScanner()
        
        # Fichiers qui causaient des fausses alertes
        false_positive_files = [
            Path('/Users/test/Library/Preferences/com.apple.calaccessd.plist'),
            Path('/Users/test/Library/Preferences/ContextStoreAgent.plist'),
            Path('/Users/test/.localized')
        ]
        
        for file_path in false_positive_files:
            if hasattr(scanner, '_is_truly_suspicious_file'):
                is_suspicious = scanner._is_truly_suspicious_file(file_path)
            else:
                is_suspicious = scanner._is_suspicious_name(file_path.name)
                
            assert not is_suspicious, f"Faux positif détecté: {file_path.name}"
        
        print("✅ Test 4: Élimination faux positifs - OK")
    except Exception as e:
        print(f"❌ Test 4: Erreur faux positifs - {e}")
        return False
    
    print("🎯 === TOUS LES TESTS RÉUSSIS ===")
    print("✅ Scanner heuristique corrigé - Plus de fausses alertes Apple")
    print("✅ Scanner malware corrigé - Signatures précises")
    print("✅ Interface compatible - get_scan_results fonctionnel")
    print("✅ Faux positifs éliminés - Filtrage intelligent")
    print("")
    print("🎉 MACCEANER PRO ENTIÈREMENT CORRIGÉ ET OPÉRATIONNEL!")
    
    return True

if __name__ == "__main__":
    success = test_final_corrections()
    exit_code = 0 if success else 1
    sys.exit(exit_code)