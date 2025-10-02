#!/usr/bin/env python3
"""
MacCleaner Pro - Script de lancement principal
Version 3.5+ avec surveillance heuristique et profiling avancé
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire de l'application au path
app_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(app_dir))

def check_dependencies():
    """Vérifier les dépendances nécessaires"""
    try:
        import psutil
        import tkinter as tk
        import sqlite3
        
        # Test optionnel pour pync
        try:
            import pync
        except ImportError:
            print("⚠️ pync non installé - notifications limitées")
        
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installez avec: pip install -r requirements.txt")
        return False

def main():
    """Point d'entrée principal"""
    print("🚀 MacCleaner Pro v3.5+")
    print("=" * 40)
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Importer et lancer l'application
        from mac_cleaner import MacCleanerPro
        
        print("🖥️ Lancement de l'interface...")
        app = MacCleanerPro()
        app.root.mainloop()
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt de l'application")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print("📝 Consultez les logs pour plus de détails")
        sys.exit(1)

if __name__ == "__main__":
    main()