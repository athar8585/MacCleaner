#!/usr/bin/env python3
"""
MacCleaner Pro - Lanceur pour Interface Native macOS
Gère le lancement avec gestion des dépendances
"""

import sys
import os
import subprocess
import importlib.util

def check_pyobjc():
    """Vérifier l'installation de PyObjC"""
    try:
        import objc
        from Foundation import NSObject
        from AppKit import NSApplication
        from Cocoa import NSWindow
        print("✅ PyObjC détecté - Interface native disponible")
        return True
    except ImportError as e:
        print(f"❌ PyObjC manquant: {e}")
        return False

def check_dependencies():
    """Vérifier toutes les dépendances"""
    dependencies = {
        'psutil': 'Informations système',
        'objc': 'Interface native macOS',
        'Foundation': 'Frameworks macOS',
        'AppKit': 'Interface utilisateur macOS'
    }
    
    missing = []
    for dep, desc in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {desc}")
        except ImportError:
            print(f"❌ {dep}: {desc} - MANQUANT")
            missing.append(dep)
    
    return len(missing) == 0

def install_missing_deps():
    """Installer les dépendances manquantes"""
    print("\n🔧 Installation des dépendances manquantes...")
    
    packages = [
        'psutil',
        'pyobjc-framework-Cocoa', 
        'pyobjc-framework-AppKit',
        'pyobjc-framework-Foundation'
    ]
    
    for package in packages:
        try:
            print(f"📦 Installation de {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package
            ])
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError:
            print(f"❌ Échec installation {package}")
            return False
    
    return True

def launch_native_interface():
    """Lancer l'interface native macOS"""
    print("\n🚀 Lancement de l'interface native macOS...")
    
    try:
        # Importer et lancer
        import mac_cleaner_native
        mac_cleaner_native.main()
        
    except Exception as e:
        print(f"❌ Erreur interface native: {e}")
        print("🔄 Fallback vers interface Tkinter...")
        launch_fallback()

def launch_fallback():
    """Lancer l'interface de fallback Tkinter"""
    fallback_files = [
        "demo_visual.py",
        "macos_interface.py", 
        "mac_cleaner_gui.py"
    ]
    
    for fallback in fallback_files:
        if os.path.exists(fallback):
            print(f"🔄 Lancement de {fallback}...")
            try:
                subprocess.run([sys.executable, fallback])
                return
            except Exception as e:
                print(f"❌ Échec {fallback}: {e}")
                continue
    
    print("❌ Aucune interface disponible")

def main():
    """Point d'entrée principal"""
    print("🍎 MacCleaner Pro - Lanceur Interface Native")
    print("=" * 50)
    
    # Vérifier les dépendances
    if check_dependencies():
        print("\n✅ Toutes les dépendances sont présentes")
        launch_native_interface()
    else:
        print("\n⚠️ Dépendances manquantes détectées")
        
        response = input("Installer automatiquement? (y/n): ").lower()
        if response in ['y', 'yes', 'oui', '']:
            if install_missing_deps():
                print("\n✅ Installation terminée")
                launch_native_interface()
            else:
                print("\n❌ Installation échouée")
                launch_fallback()
        else:
            launch_fallback()

if __name__ == "__main__":
    main()