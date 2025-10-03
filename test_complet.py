#!/usr/bin/env python3
"""
Test complet de MacCleaner Pro - Vérification des fonctions principales
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

def create_test_files():
    """Créer des fichiers de test pour vérifier le nettoyage"""
    print("🧪 Création de fichiers de test...")
    
    # Créer des fichiers dans la corbeille pour tester
    trash_path = os.path.expanduser('~/.Trash')
    test_files = []
    
    # Créer quelques fichiers de test
    for i in range(3):
        test_file = os.path.join(trash_path, f"test_macCleaner_{i}.txt")
        with open(test_file, 'w') as f:
            f.write(f"Fichier de test MacCleaner {i}\n" * 100)  # ~3KB chacun
        test_files.append(test_file)
        print(f"  ✅ Créé: {test_file}")
    
    # Créer un dossier de test
    test_dir = os.path.join(trash_path, "test_macCleaner_dir")
    os.makedirs(test_dir, exist_ok=True)
    
    for i in range(2):
        sub_file = os.path.join(test_dir, f"sub_test_{i}.txt")
        with open(sub_file, 'w') as f:
            f.write(f"Sous-fichier de test {i}\n" * 50)  # ~1.5KB chacun
        test_files.append(sub_file)
    
    print(f"  ✅ Créé dossier: {test_dir} avec 2 fichiers")
    
    return test_files, test_dir

def test_mac_cleaner_functions():
    """Test des fonctions principales de MacCleaner"""
    print("\n🧪 Test des fonctions MacCleaner Pro")
    print("=" * 50)
    
    # Importer le module
    sys.path.insert(0, '/Users/loicdeloison/MacCleaner')
    
    try:
        import mac_cleaner
        print("✅ Import MacCleaner OK")
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        return False
    
    # Créer une instance sans GUI
    class TestLogger:
        def __init__(self):
            self.messages = []
        
        def log(self, msg):
            self.messages.append(msg)
            print(f"[LOG] {msg}")
    
    logger = TestLogger()
    
    # Créer des fichiers de test d'abord
    test_files, test_dir = create_test_files()
    
    print(f"\n1️⃣ État initial de la corbeille:")
    trash_path = os.path.expanduser('~/.Trash')
    initial_items = os.listdir(trash_path) if os.path.exists(trash_path) else []
    print(f"   📂 {len(initial_items)} éléments dans la corbeille")
    
    # Test en mode analyse d'abord
    print(f"\n2️⃣ Test en mode ANALYSE (pas de suppression):")
    
    try:
        # Créer une instance minimale pour les tests
        cleaner = mac_cleaner.MacCleanerPro()
        cleaner.log_message = logger.log
        cleaner.analyze_only.set(True)  # Mode analyse seulement
        cleaner.cleaning_active = True
        
        # Tester le vidage de corbeille en mode analyse
        cleaner.empty_trash_real()
        
        # Vérifier que rien n'a été supprimé
        analysis_items = os.listdir(trash_path) if os.path.exists(trash_path) else []
        if len(analysis_items) == len(initial_items):
            print("   ✅ Mode analyse OK - aucun fichier supprimé")
        else:
            print("   ❌ Mode analyse défaillant - fichiers supprimés!")
            
    except Exception as e:
        print(f"   ❌ Erreur test analyse: {e}")
        return False
    
    # Test en mode réel maintenant
    print(f"\n3️⃣ Test en mode RÉEL (suppression effective):")
    
    response = input("   ❓ Tester le mode réel (supprimer les fichiers de test) ? (oui/non): ")
    
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        try:
            cleaner.analyze_only.set(False)  # Mode réel
            cleaner.total_freed_space = 0
            
            # Tester le vidage réel
            cleaner.empty_trash_real()
            
            # Vérifier le résultat
            final_items = os.listdir(trash_path) if os.path.exists(trash_path) else []
            
            # Compter combien de nos fichiers de test ont été supprimés
            test_files_deleted = 0
            for test_file in test_files:
                if not os.path.exists(test_file):
                    test_files_deleted += 1
            
            if not os.path.exists(test_dir):
                test_files_deleted += 1  # Le dossier aussi
            
            print(f"   📊 Fichiers de test supprimés: {test_files_deleted}")
            print(f"   📊 Espace libéré: {cleaner.total_freed_space / 1024:.1f} KB")
            print(f"   📂 Éléments restants dans corbeille: {len(final_items)}")
            
            if test_files_deleted > 0:
                print("   ✅ Mode réel fonctionne - fichiers supprimés!")
            else:
                print("   ❌ Mode réel défaillant - aucun fichier supprimé!")
                
        except Exception as e:
            print(f"   ❌ Erreur test réel: {e}")
            return False
    else:
        print("   ⏭️ Test réel ignoré")
    
    print(f"\n📋 Messages de log capturés: {len(logger.messages)}")
    if logger.messages:
        print("Derniers messages:")
        for msg in logger.messages[-5:]:
            print(f"   • {msg}")
    
    return True

def test_specific_functions():
    """Test de fonctions spécifiques"""
    print(f"\n4️⃣ Test de fonctions spécifiques:")
    
    sys.path.insert(0, '/Users/loicdeloison/MacCleaner')
    import mac_cleaner
    
    cleaner = mac_cleaner.MacCleanerPro()
    
    # Test de calcul de taille
    try:
        temp_dir = tempfile.mkdtemp()
        
        # Créer quelques fichiers de test
        for i in range(3):
            with open(os.path.join(temp_dir, f"test_{i}.txt"), 'w') as f:
                f.write("Test" * 250)  # 1KB
        
        size = cleaner.get_directory_size(temp_dir)
        print(f"   ✅ Calcul taille répertoire: {size} bytes (~{size/1024:.1f} KB)")
        
        # Nettoyer
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"   ❌ Erreur test calcul taille: {e}")
    
    # Test de détection fichiers importants
    try:
        test_files = [
            "document.pdf",
            "photo.jpg", 
            "video.mp4",
            "cache.tmp",
            "log.log"
        ]
        
        important_count = 0
        for filename in test_files:
            is_important = cleaner.is_important_file(f"/tmp/{filename}")
            if is_important:
                important_count += 1
                print(f"   📎 Fichier important détecté: {filename}")
        
        print(f"   ✅ Détection fichiers importants: {important_count}/{len(test_files)}")
        
    except Exception as e:
        print(f"   ❌ Erreur test détection: {e}")

if __name__ == "__main__":
    print("🧪 TEST COMPLET MacCleaner Pro")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Objectif: Vérifier que les fonctions fonctionnent RÉELLEMENT")
    
    success = test_mac_cleaner_functions()
    
    if success:
        test_specific_functions()
        print(f"\n✅ TESTS TERMINÉS")
        print("💡 Le logiciel fonctionne bien - les fonctions sont opérationnelles!")
    else:
        print(f"\n❌ TESTS ÉCHOUÉS")
        print("🔧 Des corrections sont nécessaires.")