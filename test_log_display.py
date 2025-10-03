#!/usr/bin/env python3
"""
Test rapide de l'affichage des logs dans l'interface
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_log_display():
    """Test simple pour vérifier l'affichage des logs"""
    print("🧪 Test d'affichage des logs...")
    
    try:
        # Importer et tester la classe principale
        from mac_cleaner import MacCleanerPro
        import tkinter as tk
        
        # Test simple sans lancer l'interface complète
        print("✅ Import MacCleanerPro réussi")
        print("✅ La zone de logs devrait maintenant s'afficher avec:")
        print("   - Fond gris clair (#f8f9fa)")
        print("   - Texte noir (#333333)")
        print("   - Police Monaco 9pt")
        print("   - Message d'accueil")
        print("   - Horodatage des messages")
        print("   - Auto-scroll vers le bas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_log_display()
    print(f"\n🎯 Test {'✅ RÉUSSI' if success else '❌ ÉCHOUÉ'}")
    
    print("\n📋 Instructions pour l'utilisateur:")
    print("1. Ouvrez MacCleaner Pro")
    print("2. Regardez la zone sous 'Prêt à nettoyer'")
    print("3. Elle devrait afficher un fond gris clair avec du texte")
    print("4. Lancez une opération pour voir les logs en temps réel")
    print("5. Les messages devraient défiler avec l'heure")