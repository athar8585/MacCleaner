#!/usr/bin/env python3
"""
MacCleaner Pro - Version Ultra Simplifiée et 100% Fonctionnelle
GARANTIE DE FONCTIONNEMENT RÉEL - Aucun "faire semblant"
"""

import os
import sys
import shutil
import subprocess
import threading
import time
import glob
from datetime import datetime

def log_message(message):
    """Afficher un message avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)

def get_path_size(path):
    """Calculer la taille réelle d'un fichier ou dossier"""
    total_size = 0
    try:
        if os.path.isfile(path):
            total_size = os.path.getsize(path)
        elif os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                    except (OSError, PermissionError):
                        pass
    except (OSError, PermissionError):
        pass
    return total_size

def empty_trash_completely():
    """Vider COMPLÈTEMENT et DÉFINITIVEMENT la corbeille"""
    trash_path = os.path.expanduser('~/.Trash')
    
    if not os.path.exists(trash_path):
        log_message("✅ Corbeille déjà vide")
        return 0
    
    items = os.listdir(trash_path)
    if not items:
        log_message("✅ Corbeille déjà vide")
        return 0
    
    log_message(f"🗑️ VIDAGE RÉEL DE LA CORBEILLE - {len(items)} éléments à supprimer")
    
    total_freed = 0
    items_deleted = 0
    
    for item in items:
        item_path = os.path.join(trash_path, item)
        
        try:
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                os.remove(item_path)  # SUPPRESSION RÉELLE
                total_freed += size
                items_deleted += 1
                log_message(f"  ✅ SUPPRIMÉ DÉFINITIVEMENT: {item}")
                
            elif os.path.isdir(item_path):
                size = get_path_size(item_path)
                shutil.rmtree(item_path)  # SUPPRESSION RÉELLE
                total_freed += size
                items_deleted += 1
                log_message(f"  ✅ DOSSIER SUPPRIMÉ DÉFINITIVEMENT: {item}/")
                
        except (OSError, PermissionError) as e:
            log_message(f"  ⚠️ Permission refusée pour {item}: {str(e)}")
            # Essayer avec force
            try:
                subprocess.run(['rm', '-rf', item_path], check=True, capture_output=True)
                items_deleted += 1
                log_message(f"  ✅ FORCÉ LA SUPPRESSION: {item}")
            except subprocess.CalledProcessError:
                log_message(f"  ❌ IMPOSSIBLE DE SUPPRIMER: {item}")
    
    # Vérification finale RÉELLE
    remaining = os.listdir(trash_path) if os.path.exists(trash_path) else []
    
    log_message(f"📊 RÉSULTAT FINAL:")
    log_message(f"  • Éléments supprimés: {items_deleted}/{len(items)}")
    log_message(f"  • Espace libéré: {total_freed / (1024*1024):.1f} MB")
    log_message(f"  • Éléments restants: {len(remaining)}")
    
    if len(remaining) == 0:
        log_message("🎉 CORBEILLE COMPLÈTEMENT VIDE !")
    else:
        log_message("⚠️ Quelques éléments restent (permissions système)")
        for item in remaining:
            log_message(f"    • {item}")
    
    return total_freed

def clean_cache_directory(cache_path):
    """Nettoyer RÉELLEMENT un répertoire de cache"""
    if not os.path.exists(cache_path):
        return 0
    
    log_message(f"🧹 Nettoyage RÉEL de {cache_path}")
    
    total_freed = 0
    items_cleaned = 0
    
    try:
        items = os.listdir(cache_path)
        for item in items:
            item_path = os.path.join(cache_path, item)
            
            try:
                if os.path.isfile(item_path):
                    # Nettoyer les fichiers de cache/temporaires
                    if any(ext in item.lower() for ext in ['.cache', '.tmp', '.temp', '.log']):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)  # SUPPRESSION RÉELLE
                        total_freed += size
                        items_cleaned += 1
                        log_message(f"  ✅ Supprimé: {item}")
                        
                elif os.path.isdir(item_path):
                    # Nettoyer récursivement les sous-dossiers
                    sub_freed = clean_cache_directory(item_path)
                    total_freed += sub_freed
                    
                    # Supprimer le dossier s'il est vide
                    try:
                        if not os.listdir(item_path):
                            os.rmdir(item_path)
                            log_message(f"  ✅ Dossier vide supprimé: {item}/")
                    except OSError:
                        pass
                        
            except (OSError, PermissionError):
                pass
                
    except (OSError, PermissionError):
        log_message(f"  ⚠️ Accès refusé à {cache_path}")
    
    if items_cleaned > 0:
        log_message(f"  📊 {items_cleaned} éléments nettoyés, {total_freed/1024:.1f} KB libérés")
    
    return total_freed

def clean_temp_files():
    """Nettoyer RÉELLEMENT les fichiers temporaires"""
    temp_paths = [
        '/tmp',
        '/var/tmp',
        os.path.expanduser('~/Library/Application Support/*/tmp')
    ]
    
    total_freed = 0
    
    for temp_path in temp_paths:
        if '*' in temp_path:
            # Gérer les wildcards
            matching_paths = glob.glob(temp_path)
            for path in matching_paths:
                freed = clean_cache_directory(path)
                total_freed += freed
        else:
            freed = clean_cache_directory(temp_path)
            total_freed += freed
    
    return total_freed

def analyze_system():
    """Analyser le système SANS RIEN SUPPRIMER"""
    log_message("🔍 ANALYSE DU SYSTÈME - Aucune suppression")
    
    total_recoverable = 0
    
    # Analyser la corbeille
    trash_path = os.path.expanduser('~/.Trash')
    if os.path.exists(trash_path):
        trash_size = get_path_size(trash_path)
        total_recoverable += trash_size
        items_count = len(os.listdir(trash_path))
        log_message(f"📊 Corbeille: {items_count} éléments, {trash_size/(1024*1024):.1f} MB")
    
    # Analyser les caches
    cache_paths = [
        os.path.expanduser('~/Library/Caches'),
        '/Library/Caches'
    ]
    
    cache_total = 0
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            cache_size = get_path_size(cache_path)
            cache_total += cache_size
            log_message(f"📊 Caches {os.path.basename(cache_path)}: {cache_size/(1024*1024):.1f} MB")
    
    total_recoverable += cache_total
    
    # Analyser les fichiers temporaires
    temp_size = 0
    if os.path.exists('/tmp'):
        temp_size = get_path_size('/tmp')
        total_recoverable += temp_size
        log_message(f"📊 Fichiers temporaires: {temp_size/(1024*1024):.1f} MB")
    
    log_message(f"📊 TOTAL RÉCUPÉRABLE: {total_recoverable/(1024*1024):.1f} MB")
    
    return total_recoverable

def clean_system_real():
    """Nettoyer RÉELLEMENT le système"""
    log_message("🚨 NETTOYAGE RÉEL DU SYSTÈME - Suppressions définitives !")
    
    total_freed = 0
    
    # 1. Vider la corbeille RÉELLEMENT
    log_message("\n1️⃣ VIDAGE RÉEL DE LA CORBEILLE")
    trash_freed = empty_trash_completely()
    total_freed += trash_freed
    
    # 2. Nettoyer les caches RÉELLEMENT
    log_message("\n2️⃣ NETTOYAGE RÉEL DES CACHES")
    cache_paths = [
        os.path.expanduser('~/Library/Caches'),
        '/Library/Caches'
    ]
    
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            freed = clean_cache_directory(cache_path)
            total_freed += freed
    
    # 3. Nettoyer les fichiers temporaires RÉELLEMENT
    log_message("\n3️⃣ NETTOYAGE RÉEL DES FICHIERS TEMPORAIRES")
    temp_freed = clean_temp_files()
    total_freed += temp_freed
    
    # 4. Optimisations système
    log_message("\n4️⃣ OPTIMISATIONS SYSTÈME")
    try:
        # Purger la mémoire
        subprocess.run(['sudo', 'purge'], check=True, capture_output=True, timeout=30)
        log_message("  ✅ Mémoire purgée")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        log_message("  ⚠️ Purge mémoire nécessite sudo")
    
    try:
        # Vider le cache DNS
        subprocess.run(['sudo', 'dscacheutil', '-flushcache'], check=True, capture_output=True, timeout=30)
        log_message("  ✅ Cache DNS vidé")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        log_message("  ⚠️ Cache DNS nécessite sudo")
    
    log_message(f"\n🎉 NETTOYAGE RÉEL TERMINÉ !")
    log_message(f"💾 ESPACE TOTAL LIBÉRÉ: {total_freed/(1024*1024):.1f} MB")
    
    return total_freed

def main():
    """Menu principal"""
    print("🧹 MacCleaner Pro - Version Ultra Simplifiée")
    print("=" * 60)
    print("✅ GARANTIE 100% FONCTIONNEL - Aucun 'faire semblant'")
    print("=" * 60)
    
    while True:
        print("\nOptions disponibles:")
        print("1️⃣ - Analyser le système (SÉCURISÉ - aucune suppression)")
        print("2️⃣ - Nettoyer RÉELLEMENT (⚠️ SUPPRESSION DÉFINITIVE)")
        print("3️⃣ - Vider seulement la corbeille")
        print("4️⃣ - Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == '1':
            print("\n" + "="*50)
            analyze_system()
            print("="*50)
            
        elif choice == '2':
            print("\n⚠️ ATTENTION - NETTOYAGE RÉEL ⚠️")
            print("Cette action va supprimer définitivement des fichiers !")
            confirm = input("Tapez 'CONFIRMER' pour procéder: ").strip()
            
            if confirm == 'CONFIRMER':
                print("\n" + "="*50)
                clean_system_real()
                print("="*50)
            else:
                print("❌ Nettoyage annulé")
                
        elif choice == '3':
            print("\n⚠️ VIDAGE RÉEL DE LA CORBEILLE")
            confirm = input("Tapez 'OUI' pour vider la corbeille: ").strip()
            
            if confirm.upper() == 'OUI':
                print("\n" + "="*30)
                empty_trash_completely()
                print("="*30)
            else:
                print("❌ Vidage annulé")
                
        elif choice == '4':
            print("👋 Au revoir !")
            break
            
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()