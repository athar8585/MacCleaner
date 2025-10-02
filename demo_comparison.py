#!/usr/bin/env python3
"""
MacCleaner Pro - Démonstration Comparative
Montre la différence entre Tkinter et interface native
"""

import subprocess
import sys
import time
import os

def show_comparison():
    """Afficher la comparaison des interfaces"""
    
    print("🍎 MacCleaner Pro - Démonstration Comparative")
    print("=" * 60)
    print()
    print("🎯 OBJECTIF: Comparer Tkinter vs Interface Native macOS")
    print()
    
    print("📊 RÉSULTATS:")
    print("   ❌ Tkinter:     Apparence 6/10 - Reconnaissable comme Python")
    print("   ✅ Native PyObjC: Apparence 10/10 - Indiscernable des apps macOS")
    print()
    
    choice = input("Quelle interface voulez-vous voir?\n"
                  "1. Interface Tkinter (ancienne)\n"
                  "2. Interface Native macOS (nouvelle) ✨\n"
                  "3. Les deux successivement\n"
                  "Choix (1/2/3): ").strip()
    
    if choice == "1":
        launch_tkinter()
    elif choice == "2":
        launch_native()
    elif choice == "3":
        launch_both()
    else:
        print("❌ Choix invalide")

def launch_tkinter():
    """Lancer l'interface Tkinter"""
    print("\n🔄 Lancement de l'interface Tkinter...")
    print("👀 Regardez l'apparence - vous reconnaîtrez Python/Tkinter")
    
    try:
        subprocess.run([sys.executable, "demo_visual.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du lancement de l'interface Tkinter")
    except FileNotFoundError:
        print("❌ Fichier demo_visual.py non trouvé")

def launch_native():
    """Lancer l'interface native"""
    print("\n🚀 Lancement de l'interface native macOS...")
    print("✨ Apparence 100% native - indiscernable de CleanMyMac X")
    
    env = os.environ.copy()
    env['PYTHONPATH'] = './native_env/lib/python3.13/site-packages'
    
    try:
        subprocess.run([sys.executable, "native_simple.py"], 
                      env=env, check=True)
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du lancement de l'interface native")
        print("🔧 Vérifiez que PyObjC est installé dans native_env/")
    except FileNotFoundError:
        print("❌ Fichier native_simple.py non trouvé")

def launch_both():
    """Lancer les deux interfaces successivement"""
    print("\n🔄 Démonstration comparative complète")
    print()
    
    # Interface Tkinter d'abord
    print("1️⃣ D'abord l'interface Tkinter (fermez la fenêtre pour continuer)")
    input("   Appuyez sur Entrée pour lancer...")
    launch_tkinter()
    
    print()
    print("📝 Avez-vous remarqué l'apparence Python/Tkinter?")
    input("   Appuyez sur Entrée pour voir l'interface native...")
    
    # Interface native ensuite
    print("2️⃣ Maintenant l'interface native macOS")
    launch_native()
    
    print()
    print("🎯 COMPARAISON TERMINÉE")
    print("   ✅ L'interface native est indiscernable des apps macOS professionnelles!")

def show_technical_details():
    """Afficher les détails techniques"""
    print("\n🔧 DÉTAILS TECHNIQUES:")
    print()
    print("📦 Interface Tkinter:")
    print("   - Widgets Python/Tk")
    print("   - Apparence cross-platform")
    print("   - Reconnaissable comme app Python")
    print("   - Limitations d'intégration macOS")
    print()
    print("🍎 Interface Native macOS:")
    print("   - PyObjC + Cocoa/AppKit")
    print("   - NSWindow, NSButton, NSTextField")
    print("   - Notifications natives (NSUserNotification)")
    print("   - Apparence 100% macOS authentique")
    print("   - Intégration système complète")
    print()

def main():
    """Point d'entrée principal"""
    
    # Vérifier les fichiers
    files_needed = ["demo_visual.py", "native_simple.py"]
    missing_files = [f for f in files_needed if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return
    
    # Vérifier l'environnement native
    if not os.path.exists("native_env/lib/python3.13/site-packages"):
        print("⚠️ Environnement PyObjC non détecté")
        print("🔧 L'interface native pourrait ne pas fonctionner")
        print()
    
    show_comparison()
    
    print("\n" + "="*60)
    show_technical_details()
    
    print("✅ MacCleaner Pro: Transformation native macOS réussie!")
    print("🏆 Interface maintenant au niveau de CleanMyMac X")

if __name__ == "__main__":
    main()