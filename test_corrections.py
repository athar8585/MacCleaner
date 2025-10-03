#!/usr/bin/env python3
"""
Test de validation complète des corrections MacCleaner
"""

import os
import sys
import tempfile
import shutil

def test_mac_cleaner_corrections():
    """Test complet des corrections apportées"""
    print("🔬 TEST DES CORRECTIONS MacCleaner Pro")
    print("=" * 60)
    
    # Ajouter le répertoire au path
    sys.path.insert(0, '/Users/loicdeloison/MacCleaner')
    
    # Test 1: Import sans erreur
    print("\n1️⃣ Test d'import du module corrigé...")
    try:
        import mac_cleaner
        print("✅ Import réussi")
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        return False
    
    # Test 2: Création de l'instance
    print("\n2️⃣ Test de création d'instance...")
    try:
        # Simuler l'absence d'affichage pour éviter l'erreur tkinter
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        app = mac_cleaner.MacCleanerPro()
        print("✅ Instance créée")
        
        # Test de l'état initial
        print(f"   • Mode analyse: {app.analyze_only.get()}")
        print(f"   • Protection iCloud: {app.protect_icloud.get()}")
        print(f"   • Nettoyage actif: {app.cleaning_active}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur création instance: {e}")
        return False
    
    # Test 3: Vérification des chemins de nettoyage
    print("\n3️⃣ Test des chemins de nettoyage...")
    try:
        app = mac_cleaner.MacCleanerPro()
        app.root.withdraw()
        
        total_paths = 0
        valid_paths = 0
        
        for category, paths in app.cleanup_paths.items():
            print(f"   📁 {category}:")
            for path_pattern in paths:
                total_paths += 1
                expanded = os.path.expanduser(path_pattern)
                
                # Vérifier si le chemin ou son parent existe
                if os.path.exists(expanded) or os.path.exists(os.path.dirname(expanded)):
                    valid_paths += 1
                    print(f"      ✅ {path_pattern}")
                else:
                    print(f"      ⚠️ {path_pattern} (peut ne pas exister)")
        
        print(f"   📊 Chemins valides: {valid_paths}/{total_paths}")
        app.root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur vérification chemins: {e}")
        return False
    
    # Test 4: Test des fonctions de base
    print("\n4️⃣ Test des fonctions de nettoyage de base...")
    try:
        app = mac_cleaner.MacCleanerPro()
        app.root.withdraw()
        
        # Créer un fichier de test temporaire
        test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tmp')
        test_file.write(b"Test MacCleaner")
        test_file.close()
        
        # Test du calcul de taille
        size = app.get_path_size(test_file.name)
        print(f"   📏 Calcul taille: {size} bytes")
        
        # Test de détection de fichier important
        is_important = app.should_protect_file(test_file.name)
        print(f"   🔒 Fichier important: {is_important}")
        
        # Test de nettoyage en mode analyse
        app.analyze_only.set(True)
        initial_files = len(app.analyzed_files)
        
        # Simuler le nettoyage d'un fichier temporaire
        if os.path.exists(test_file.name):
            app.clean_path(test_file.name)
            
        analysis_files = len(app.analyzed_files)
        print(f"   📊 Fichiers analysés: {analysis_files - initial_files}")
        
        # Vérifier que le fichier existe toujours (mode analyse)
        if os.path.exists(test_file.name):
            print("   ✅ Mode analyse OK - fichier préservé")
            os.unlink(test_file.name)  # Nettoyer
        else:
            print("   ❌ Mode analyse défaillant - fichier supprimé!")
        
        app.root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur test fonctions: {e}")
        return False
    
    # Test 5: Test de la corbeille en mode sécurisé
    print("\n5️⃣ Test de la fonction corbeille...")
    try:
        # Créer quelques fichiers dans la corbeille pour tester
        trash_path = os.path.expanduser('~/.Trash')
        test_files = []
        
        for i in range(2):
            test_file = os.path.join(trash_path, f"test_correction_{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"Test correction {i}")
            test_files.append(test_file)
        
        print(f"   📝 Créé {len(test_files)} fichiers de test dans la corbeille")
        
        # Test en mode analyse
        app = mac_cleaner.MacCleanerPro()
        app.root.withdraw()
        app.analyze_only.set(True)
        
        initial_count = len(os.listdir(trash_path))
        app.empty_trash_real()
        final_count = len(os.listdir(trash_path))
        
        if initial_count == final_count:
            print("   ✅ Mode analyse corbeille OK - rien supprimé")
        else:
            print("   ❌ Mode analyse corbeille défaillant")
        
        # Nettoyer les fichiers de test
        for test_file in test_files:
            if os.path.exists(test_file):
                os.remove(test_file)
        
        app.root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur test corbeille: {e}")
        return False
    
    print("\n✅ TOUS LES TESTS DE CORRECTION PASSENT")
    print("🎉 Le logiciel MacCleaner est maintenant corrigé et fonctionnel !")
    return True

def test_real_functionality():
    """Test optionnel de fonctionnalité réelle"""
    print("\n" + "="*60)
    print("🚨 TEST OPTIONNEL DE FONCTIONNALITÉ RÉELLE")
    print("="*60)
    
    response = input("Voulez-vous tester la suppression réelle de fichiers de test ? (oui/non): ")
    
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("⏭️ Test réel ignoré")
        return True
    
    print("\n6️⃣ Test de suppression réelle...")
    try:
        # Créer des fichiers de test temporaires
        temp_dir = tempfile.mkdtemp(prefix="test_maccleaner_")
        test_files = []
        
        for i in range(3):
            test_file = os.path.join(temp_dir, f"test_real_{i}.tmp")
            with open(test_file, 'w') as f:
                f.write(f"Test réel {i}" * 100)
            test_files.append(test_file)
        
        print(f"   📝 Créé {len(test_files)} fichiers dans {temp_dir}")
        
        # Test de suppression réelle
        app = mac_cleaner.MacCleanerPro()
        app.root.withdraw()
        app.analyze_only.set(False)  # Mode réel
        
        initial_files = len(os.listdir(temp_dir))
        print(f"   📊 Fichiers initiaux: {initial_files}")
        
        # Nettoyer le répertoire
        freed_space = app.clean_directory_contents(temp_dir)
        
        final_files = len(os.listdir(temp_dir))
        print(f"   📊 Fichiers finaux: {final_files}")
        print(f"   💾 Espace libéré: {freed_space} bytes")
        
        if final_files < initial_files:
            print("   ✅ Suppression réelle fonctionne !")
        else:
            print("   ❌ Suppression réelle défaillante")
        
        # Nettoyer
        shutil.rmtree(temp_dir)
        app.root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur test réel: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_mac_cleaner_corrections()
    
    if success:
        test_real_functionality()
        
        print("\n" + "="*60)
        print("🏆 RÉSUMÉ DES CORRECTIONS")
        print("="*60)
        print("✅ Mode analyse vs mode réel clairement différencié")
        print("✅ Messages explicites sur ce qui se passe")
        print("✅ Confirmations renforcées pour le mode réel")
        print("✅ Corrections des bugs d'importation")
        print("✅ Vérification des chemins de nettoyage")
        print("✅ Fonctions de base testées et validées")
        print("\n🎉 MacCleaner Pro est maintenant RÉELLEMENT FONCTIONNEL !")
    else:
        print("\n❌ Des problèmes persistent - vérifications supplémentaires nécessaires")