#!/usr/bin/env python3
"""
MacCleaner Pro - Lanceur Final
Script simplifié pour lancer l'interface native
"""

import os
import sys
import subprocess

def main():
    print("🍎 MacCleaner Pro - Interface Native macOS")
    print("=" * 50)
    
    # Changer vers le bon répertoire
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Vérifier l'environnement PyObjC
    env = os.environ.copy()
    env['PYTHONPATH'] = './native_env/lib/python3.13/site-packages'
    
    print("🚀 Lancement de l'interface native...")
    print("✨ Design authentique macOS comme CleanMyMac X")
    
    try:
        # Lancer l'interface native
        subprocess.run([sys.executable, "native_simple.py"], env=env)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("🔄 Fallback vers interface Tkinter...")
        try:
            subprocess.run([sys.executable, "demo_visual.py"])
        except:
            print("❌ Aucune interface disponible")

if __name__ == "__main__":
    main()