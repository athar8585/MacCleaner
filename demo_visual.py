#!/usr/bin/env python3
"""
MacCleaner Pro - Version de démonstration visuelle
Montre l'interface sans les fonctionnalités complexes
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os
from pathlib import Path

class MacCleanerDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MacCleaner Pro v3.5+ - Interface de Démonstration")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables de démonstration
        self.cleaning_active = False
        self.total_freed_space = 0
        
        self.setup_gui()
    
    def setup_gui(self):
        """Configuration de l'interface graphique"""
        # Configuration du grid principal
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titre principal
        title_label = tk.Label(main_frame, text="🚀 MacCleaner Pro", 
                              font=('SF Pro Display', 24, 'bold'),
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Informations système
        self.create_system_info(main_frame)
        
        # Options de nettoyage
        self.create_cleanup_options(main_frame)
        
        # Zone de progression
        self.create_progress_area(main_frame)
        
        # Boutons d'action
        self.create_action_buttons(main_frame)
    
    def create_system_info(self, parent):
        """Créer la section informations système"""
        info_frame = ttk.LabelFrame(parent, text="📊 Informations Système", padding=10)
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=5)
        
        # Informations de démonstration
        info_text = """
💾 Espace disque: 234.5 GB libre / 500 GB
🧠 Mémoire: 8.2 GB utilisés / 16 GB
⚡ CPU: 23% d'utilisation
🔄 Processus: 142 actifs
📁 Fichiers analysés: 12,456
🗑️ Dernière analyse: Aujourd'hui 14:30
        """.strip()
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=('SF Pro Display', 11),
                             bg='#34495e', fg='#ecf0f1',
                             justify=tk.LEFT, anchor='nw')
        info_label.pack(fill=tk.BOTH, expand=True)
    
    def create_cleanup_options(self, parent):
        """Créer les options de nettoyage"""
        options_frame = ttk.LabelFrame(parent, text="🧹 Options de Nettoyage", padding=10)
        options_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=5)
        
        # Options de nettoyage avec cases à cocher
        cleanup_options = [
            ("✅ System Caches", "1.2 GB"),
            ("✅ User Caches", "456 MB"),
            ("✅ Logs & Diagnostics", "234 MB"),
            ("✅ Downloads & Trash", "2.1 GB"),
            ("✅ Browser Data", "123 MB"),
            ("✅ System Temp", "89 MB")
        ]
        
        for i, (option, size) in enumerate(cleanup_options):
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(options_frame, text=f"{option} ({size})",
                               variable=var, font=('SF Pro Display', 10),
                               bg='#34495e', fg='#ecf0f1',
                               selectcolor='#3498db',
                               activebackground='#34495e')
            cb.pack(anchor='w', pady=2)
    
    def create_progress_area(self, parent):
        """Créer la zone de progression"""
        progress_frame = ttk.LabelFrame(parent, text="📋 Progression & Logs", padding=10)
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        # Barre de progression
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress_bar['value'] = 65  # Demo: 65% de progression
        
        # Zone de logs
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=12, width=70,
                                                  font=('Monaco', 10),
                                                  bg='#1e1e1e', fg='#00ff00',
                                                  insertbackground='#00ff00')
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Messages de démonstration
        demo_logs = [
            "🚀 MacCleaner Pro v3.5+ démarré",
            "🔍 Analyse des fichiers système...",
            "✅ System Caches: 1.2 GB détectés",
            "✅ User Caches: 456 MB détectés",
            "🧹 Nettoyage en cours...",
            "  ✅ Supprimé: ~/Library/Caches/com.apple.Safari (45 MB)",
            "  ✅ Supprimé: /var/folders/temp_files (123 MB)",
            "  🔒 Protégé (iCloud): Documents/Important.pdf",
            "🔍 Surveillance heuristique active",
            "📊 Profiling de performance: CPU 23%, RAM 8.2GB",
            "🔔 Notification: Nettoyage en cours...",
            "⏰ Temps écoulé: 00:02:34",
            "📈 Espace libéré: 1.8 GB",
            "🎉 Nettoyage terminé avec succès!"
        ]
        
        for log in demo_logs:
            self.log_text.insert(tk.END, f"[{self.get_time()}] {log}\n")
        
        self.log_text.see(tk.END)
    
    def create_action_buttons(self, parent):
        """Créer les boutons d'action"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Style des boutons
        buttons = [
            ("🧹 Nettoyer", self.demo_clean, '#e74c3c'),
            ("🛡️ Scan Malware", self.demo_scan, '#f39c12'),
            ("📊 Profiling", self.demo_profile, '#9b59b6'),
            ("🔍 Surveillance", self.demo_monitor, '#2ecc71'),
            ("🔔 Test Notifs", self.demo_notify, '#3498db'),
            ("🔄 MAJ Complète", self.demo_update, '#34495e')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(btn_frame, text=text, command=command,
                           font=('SF Pro Display', 11, 'bold'),
                           bg=color, fg='white',
                           width=15, height=2,
                           relief='flat',
                           cursor='hand2')
            btn.grid(row=row, column=col, padx=5, pady=4, sticky='ew')
    
    def get_time(self):
        """Obtenir l'heure actuelle pour les logs"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def log_message(self, message):
        """Ajouter un message au log"""
        self.log_text.insert(tk.END, f"[{self.get_time()}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    # Méthodes de démonstration
    def demo_clean(self):
        self.log_message("🧹 Démonstration: Nettoyage lancé")
        self.log_message("📊 Interface moderne avec thème sombre")
        
    def demo_scan(self):
        self.log_message("🛡️ Démonstration: Scan de sécurité")
        self.log_message("🔍 Scanner heuristique activé")
        
    def demo_profile(self):
        self.log_message("📊 Démonstration: Profiling de performance")
        self.log_message("⚡ Surveillance CPU/RAM/Disque active")
        
    def demo_monitor(self):
        self.log_message("🔍 Démonstration: Surveillance temps réel")
        self.log_message("🚨 Détection comportements suspects")
        
    def demo_notify(self):
        self.log_message("🔔 Démonstration: Test des notifications")
        self.log_message("✅ Système de notifications macOS intégré")
        
    def demo_update(self):
        self.log_message("🔄 Démonstration: Mise à jour complète")
        self.log_message("📦 Vérification des nouvelles versions")
    
    def run(self):
        """Lancer l'application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Fermeture de la démonstration")

def main():
    print("🎨 MacCleaner Pro - Démonstration Visuelle")
    print("=" * 45)
    print("🖥️ Lancement de l'interface...")
    print("👀 Regardez la fenêtre qui s'ouvre pour voir l'apparence")
    print("🔴 Fermez la fenêtre pour terminer la démonstration")
    
    app = MacCleanerDemo()
    app.run()

if __name__ == "__main__":
    main()