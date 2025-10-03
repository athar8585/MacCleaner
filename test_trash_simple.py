#!/usr/bin/env python3
"""
Test simple du vidage de corbeille sans GUI
"""

import os
import shutil
import subprocess

def test_trash_content():
    """Voir le contenu de la corbeille"""
    trash_path = os.path.expanduser('~/.Trash')
    
    if not os.path.exists(trash_path):
        print("📂 Corbeille vide ou inexistante")
        return False
    
    items = os.listdir(trash_path)
    print(f"📂 Éléments dans la corbeille: {len(items)}")
    
    total_size = 0
    for item in items:
        item_path = os.path.join(trash_path, item)
        try:
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                total_size += size
                print(f"  📄 {item} ({size/1024:.1f} KB)")
            elif os.path.isdir(item_path):
                # Calculer taille du dossier
                dir_size = 0
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        try:
                            dir_size += os.path.getsize(os.path.join(root, file))
                        except (OSError, PermissionError):
                            pass
                total_size += dir_size
                print(f"  📁 {item}/ ({dir_size/1024:.1f} KB)")
        except (OSError, PermissionError) as e:
            print(f"  ❌ {item} (erreur: {e})")
    
    print(f"📊 Taille totale: {total_size/(1024*1024):.1f} MB")
    return len(items) > 0

def empty_trash_simple():
    """Vider la corbeille de manière simple et efficace"""
    trash_path = os.path.expanduser('~/.Trash')
    
    if not os.path.exists(trash_path):
        print("✅ Corbeille déjà vide")
        return True
    
    items = os.listdir(trash_path)
    if not items:
        print("✅ Corbeille déjà vide")
        return True
    
    print(f"🗑️ Suppression de {len(items)} éléments...")
    
    deleted_count = 0
    total_freed = 0
    
    for item in items:
        item_path = os.path.join(trash_path, item)
        try:
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                os.remove(item_path)
                total_freed += size
                deleted_count += 1
                print(f"  ✅ Supprimé: {item}")
                
            elif os.path.isdir(item_path):
                # Calculer taille avant suppression
                dir_size = 0
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        try:
                            dir_size += os.path.getsize(os.path.join(root, file))
                        except (OSError, PermissionError):
                            pass
                
                shutil.rmtree(item_path)
                total_freed += dir_size
                deleted_count += 1
                print(f"  ✅ Dossier supprimé: {item}/")
                
        except (OSError, PermissionError) as e:
            print(f"  ❌ Impossible de supprimer {item}: {e}")
            # Essayer avec rm -rf en dernier recours
            try:
                result = subprocess.run(['rm', '-rf', item_path], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    deleted_count += 1
                    print(f"  ✅ Forcé la suppression: {item}")
                else:
                    print(f"  ❌ Échec rm -rf: {result.stderr}")
            except Exception as rm_error:
                print(f"  ❌ Erreur rm: {rm_error}")
    
    print(f"\n📊 Résultat:")
    print(f"   - Éléments supprimés: {deleted_count}/{len(items)}")
    print(f"   - Espace libéré: {total_freed/(1024*1024):.1f} MB")
    
    # Vérifier le résultat
    remaining = os.listdir(trash_path) if os.path.exists(trash_path) else []
    if remaining:
        print(f"   - ⚠️ Éléments restants: {len(remaining)}")
        for item in remaining:
            print(f"     • {item}")
    else:
        print("   - ✅ Corbeille complètement vide!")
    
    return deleted_count > 0

if __name__ == "__main__":
    print("🧪 Test simple du vidage de corbeille\n")
    
    print("1️⃣ État actuel de la corbeille:")
    has_items = test_trash_content()
    
    if has_items:
        print("\n❓ Voulez-vous vider la corbeille ? (oui/non):", end=" ")
        response = input().strip().lower()
        
        if response in ['oui', 'o', 'yes', 'y']:
            print("\n2️⃣ Vidage de la corbeille:")
            success = empty_trash_simple()
            
            print("\n3️⃣ Vérification finale:")
            test_trash_content()
        else:
            print("❌ Opération annulée")
    else:
        print("\n💡 Rien à supprimer!")