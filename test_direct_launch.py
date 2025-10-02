#!/usr/bin/env python3

"""
Test direct - MacCleaner Pro
Lance l'interface directement pour tester
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

def test_launch():
    try:
        # Aller dans le bon répertoire
        app_dir = "/Users/loicdeloison/Desktop/MacCleaner"
        
        if not os.path.exists(app_dir):
            messagebox.showerror("Erreur", f"Répertoire non trouvé: {app_dir}")
            return
            
        os.chdir(app_dir)
        
        # Vérifier que le fichier existe
        main_file = "mac_cleaner_tkinter.py"
        if not os.path.exists(main_file):
            messagebox.showerror("Erreur", f"Fichier non trouvé: {main_file}")
            return
            
        # Importer et lancer
        sys.path.insert(0, app_dir)
        
        # Lancer directement le module
        exec(open(main_file).read())
        
    except Exception as e:
        messagebox.showerror("Erreur MacCleaner Pro", f"Erreur de lancement:\n{str(e)}")

if __name__ == "__main__":
    test_launch()