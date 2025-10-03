#!/usr/bin/env python3
"""
Test rapide du vidage de corbeille
"""

import os
import sys
sys.path.append('/Users/loicdeloison/MacCleaner')

from mac_cleaner import MacCleanerPro

def test_empty_trash():
    """Test spécifique du vidage de corbeille"""
    print("🧪 Test du vidage de corbeille...")
    
    # Vérifier le contenu actuel
    trash_path = os.path.expanduser('~/.Trash')
    if os.path.exists(trash_path):
        items = os.listdir(trash_path)
        print(f"📂 Éléments dans la corbeille: {len(items)}")
        for item in items[:5]:  # Afficher les 5 premiers
            print(f"  - {item}")
        if len(items) > 5:
            print(f"  ... et {len(items) - 5} autres")
    else:
        print("📂 Corbeille vide ou inexistante")
        return
    
    # Créer une instance du nettoyeur
    cleaner = MacCleanerPro()
    cleaner.log_message = lambda msg: print(f"[LOG] {msg}")
    
    # Mode test (ne pas vraiment supprimer)
    print("\n🔍 Test en mode analyse...")
    cleaner.analyze_only.set(True)
    cleaner.empty_trash_real()
    
    # Demander confirmation pour vraiment vider
    response = input("\n❓ Voulez-vous vraiment vider la corbeille ? (oui/non): ")
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        print("\n🗑️ Vidage réel de la corbeille...")
        cleaner.analyze_only.set(False)
        cleaner.cleaning_active = True
        cleaner.empty_trash_real()
        
        # Vérifier le résultat
        items_after = os.listdir(trash_path) if os.path.exists(trash_path) else []
        print(f"\n✅ Résultat: {len(items_after)} éléments restants dans la corbeille")
        print(f"📊 Espace libéré: {cleaner.total_freed_space / (1024*1024):.1f} MB")
    else:
        print("❌ Test annulé")

if __name__ == "__main__":
    test_empty_trash()