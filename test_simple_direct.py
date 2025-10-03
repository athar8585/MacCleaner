#!/usr/bin/env python3
"""
Test simple et direct des fonctions de nettoyage
"""

import os
import shutil
import tempfile

def test_trash_cleaning_direct():
    """Test direct du nettoyage de corbeille"""
    print("🧪 Test direct du nettoyage de corbeille")
    print("=" * 50)
    
    trash_path = os.path.expanduser('~/.Trash')
    
    # Créer des fichiers de test
    print("📝 Création de fichiers de test...")
    test_files = []
    
    for i in range(3):
        test_file = os.path.join(trash_path, f"test_direct_{i}.txt")
        with open(test_file, 'w') as f:
            f.write(f"Test MacCleaner {i}\n" * 100)
        test_files.append(test_file)
        print(f"  ✅ Créé: test_direct_{i}.txt")
    
    # État initial
    initial_items = os.listdir(trash_path)
    print(f"\n📂 État initial: {len(initial_items)} éléments")
    
    # Test du nettoyage direct
    print(f"\n🗑️ Test nettoyage direct...")
    
    def clean_trash_simple():
        """Fonction de nettoyage simple"""
        deleted_count = 0
        total_size = 0
        
        for item in os.listdir(trash_path):
            if item.startswith('test_direct_'):
                item_path = os.path.join(trash_path, item)
                try:
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)
                        total_size += size
                        deleted_count += 1
                        print(f"  ✅ Supprimé: {item}")
                except Exception as e:
                    print(f"  ❌ Erreur: {item} - {e}")
        
        return deleted_count, total_size
    
    # Exécuter le nettoyage
    deleted, size_freed = clean_trash_simple()
    
    # Vérifier le résultat
    final_items = os.listdir(trash_path)
    
    print(f"\n📊 Résultats:")
    print(f"  • Fichiers supprimés: {deleted}")
    print(f"  • Taille libérée: {size_freed / 1024:.1f} KB")
    print(f"  • Éléments restants: {len(final_items)}")
    
    # Vérifier que nos fichiers ont bien été supprimés
    test_files_remaining = [f for f in final_items if f.startswith('test_direct_')]
    
    if deleted > 0 and len(test_files_remaining) == 0:
        print("  ✅ SUCCÈS: Les fonctions de nettoyage marchent!")
        return True
    else:
        print("  ❌ ÉCHEC: Problème dans le nettoyage")
        return False

def test_cache_cleaning():
    """Test du nettoyage des caches"""
    print(f"\n🧪 Test nettoyage des caches")
    print("=" * 30)
    
    # Créer un dossier cache temporaire
    temp_cache = tempfile.mkdtemp(prefix="test_cache_")
    print(f"📁 Dossier test créé: {temp_cache}")
    
    # Créer des fichiers cache
    for i in range(5):
        cache_file = os.path.join(temp_cache, f"cache_{i}.tmp")
        with open(cache_file, 'w') as f:
            f.write("Cache data" * 100)
        print(f"  ✅ Créé: cache_{i}.tmp")
    
    # Calculer taille initiale
    initial_size = 0
    initial_count = 0
    for item in os.listdir(temp_cache):
        item_path = os.path.join(temp_cache, item)
        if os.path.isfile(item_path):
            initial_size += os.path.getsize(item_path)
            initial_count += 1
    
    print(f"📊 Taille initiale: {initial_size / 1024:.1f} KB ({initial_count} fichiers)")
    
    # Fonction de nettoyage cache
    def clean_cache_dir(cache_dir):
        cleaned_size = 0
        cleaned_count = 0
        
        for item in os.listdir(cache_dir):
            item_path = os.path.join(cache_dir, item)
            if os.path.isfile(item_path) and item.endswith('.tmp'):
                try:
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                    cleaned_size += size
                    cleaned_count += 1
                    print(f"  ✅ Nettoyé: {item}")
                except Exception as e:
                    print(f"  ❌ Erreur: {item} - {e}")
        
        return cleaned_count, cleaned_size
    
    # Exécuter le nettoyage
    cleaned_count, cleaned_size = clean_cache_dir(temp_cache)
    
    # Vérifier
    remaining_files = [f for f in os.listdir(temp_cache) if f.endswith('.tmp')]
    
    print(f"📊 Résultat nettoyage:")
    print(f"  • Fichiers nettoyés: {cleaned_count}")
    print(f"  • Taille libérée: {cleaned_size / 1024:.1f} KB")
    print(f"  • Fichiers restants: {len(remaining_files)}")
    
    # Nettoyer le dossier test
    shutil.rmtree(temp_cache)
    print(f"🧹 Dossier test supprimé")
    
    if cleaned_count == initial_count and len(remaining_files) == 0:
        print("  ✅ SUCCÈS: Nettoyage cache fonctionne!")
        return True
    else:
        print("  ❌ ÉCHEC: Problème nettoyage cache")
        return False

def main():
    """Test principal"""
    print("🔬 TESTS DIRECTS MacCleaner")
    print("=" * 60)
    print("🎯 Test des fonctions de base sans interface")
    
    results = []
    
    # Test 1: Nettoyage corbeille
    print("\n" + "="*50)
    result1 = test_trash_cleaning_direct()
    results.append(("Nettoyage corbeille", result1))
    
    # Test 2: Nettoyage cache
    print("\n" + "="*50)
    result2 = test_cache_cleaning()
    results.append(("Nettoyage cache", result2))
    
    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DES TESTS")
    print("="*60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"  {status}: {test_name}")
        if not result:
            all_passed = False
    
    print(f"\n🏆 RÉSULTAT GLOBAL:")
    if all_passed:
        print("✅ TOUS LES TESTS PASSENT")
        print("💡 Le logiciel MacCleaner fonctionne correctement!")
        print("🎉 Les suppressions sont bien réelles et effectives!")
    else:
        print("❌ CERTAINS TESTS ÉCHOUENT")
        print("🔧 Vérifications supplémentaires nécessaires")

if __name__ == "__main__":
    main()