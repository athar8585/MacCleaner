#!/usr/bin/env python3
"""
MacCleaner Pro - Lanceur Principal
Retour à l'interface Tkinter stable et fonctionnelle
"""

import sys
import os
import subprocess

def check_dependencies():
    """Vérifier les dépendances nécessaires"""
    dependencies = ['psutil', 'tkinter']
    missing = []
    
    for dep in dependencies:
        try:
            if dep == 'tkinter':
                import tkinter
            else:
                __import__(dep)
        except ImportError:
            missing.append(dep)
    
    return missing

def install_dependencies(missing):
    """Installer les dépendances manquantes"""
    if not missing:
        return True
    
    print(f"📦 Installation des dépendances manquantes: {missing}")
    
    for dep in missing:
        if dep == 'tkinter':
            print("❌ Tkinter manquant - veuillez l'installer via votre gestionnaire de paquets")
            return False
        else:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', dep])
                print(f"✅ {dep} installé")
            except subprocess.CalledProcessError:
                print(f"❌ Échec installation {dep}")
                return False
    
    return True

def main():
    """Point d'entrée principal"""
    print("🚀 MacCleaner Pro - Lanceur")
    print("=" * 40)
    print("🔄 Retour à l'interface Tkinter stable")
    print()
    
    # Vérifier les dépendances
    missing = check_dependencies()
    
    if missing:
        print("⚠️ Dépendances manquantes détectées")
        if not install_dependencies(missing):
            print("❌ Installation échouée")
            return
    
    # Lancer l'interface Tkinter
    print("🎨 Lancement de l'interface Tkinter...")
    
    try:
        import mac_cleaner_tkinter
        mac_cleaner_tkinter.main()
    except ImportError:
        # Fallback vers le script direct
        script_path = os.path.join(os.path.dirname(__file__), 'mac_cleaner_tkinter.py')
        subprocess.run([sys.executable, script_path])
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()