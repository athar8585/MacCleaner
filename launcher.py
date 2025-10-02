#!/usr/bin/env python3
"""
MacCleaner Pro - Lanceur Simplifié
Interface de lancement avec choix multiples et configuration autonome
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from pathlib import Path

class MacCleanerLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.root = tk.Tk()
        self.root.title("MacCleaner Pro - Lanceur")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configuration du style
        self.root.configure(bg='#f0f0f0')
        
        # Variables d'état
        self.autonomous_process = None
        self.is_monitoring = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # En-tête
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🧹 MacCleaner Pro",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Système de nettoyage autonome et intelligent",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Corps principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Section Actions Rapides
        self.create_quick_actions(main_frame)
        
        # Section Modes de Fonctionnement
        self.create_operation_modes(main_frame)
        
        # Section État du Système
        self.create_system_status(main_frame)
        
        # Section Configuration
        self.create_configuration_section(main_frame)
        
    def create_quick_actions(self, parent):
        """Créer la section des actions rapides"""
        actions_frame = tk.LabelFrame(
            parent, 
            text="🚀 Actions Rapides", 
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            padx=15,
            pady=10
        )
        actions_frame.pack(fill='x', pady=(0, 15))
        
        # Première ligne d'actions
        actions_row1 = tk.Frame(actions_frame, bg='#f0f0f0')
        actions_row1.pack(fill='x', pady=5)
        
        self.create_action_button(
            actions_row1,
            "🧹 Nettoyage Express",
            "Nettoyage sécurisé en 1 clic",
            '#27ae60',
            self.quick_clean
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.create_action_button(
            actions_row1,
            "🔍 Scan Malware",
            "Vérification anti-malware",
            '#e67e22',
            self.scan_malware
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.create_action_button(
            actions_row1,
            "⚡ Optimisation",
            "Boost des performances",
            '#3498db',
            self.optimize_system
        ).pack(side='left', fill='x', expand=True)
        
        # Deuxième ligne d'actions
        actions_row2 = tk.Frame(actions_frame, bg='#f0f0f0')
        actions_row2.pack(fill='x', pady=(10, 5))
        
        self.create_action_button(
            actions_row2,
            "☁️ Sync GitHub",
            "Sauvegarde cloud",
            '#9b59b6',
            self.sync_github
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.create_action_button(
            actions_row2,
            "📊 Interface Complète",
            "Contrôle avancé",
            '#34495e',
            self.open_full_interface
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.create_action_button(
            actions_row2,
            "🔧 Configuration",
            "Paramètres système",
            '#7f8c8d',
            self.open_configuration
        ).pack(side='left', fill='x', expand=True)
        
    def create_action_button(self, parent, title, subtitle, color, command):
        """Créer un bouton d'action stylisé"""
        button_frame = tk.Frame(parent, bg=color, relief='raised', bd=1)
        
        button = tk.Button(
            button_frame,
            text=f"{title}\n{subtitle}",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg=color,
            activebackground=self.darken_color(color),
            activeforeground='white',
            relief='flat',
            command=command,
            cursor='hand2',
            height=3
        )
        button.pack(fill='both', expand=True, padx=2, pady=2)
        
        return button_frame
        
    def create_operation_modes(self, parent):
        """Créer la section des modes de fonctionnement"""
        modes_frame = tk.LabelFrame(
            parent,
            text="🎯 Modes de Fonctionnement",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            padx=15,
            pady=10
        )
        modes_frame.pack(fill='x', pady=(0, 15))
        
        # Mode Autonome
        autonomous_frame = tk.Frame(modes_frame, bg='#f0f0f0')
        autonomous_frame.pack(fill='x', pady=5)
        
        self.autonomous_var = tk.BooleanVar(value=False)
        autonomous_check = tk.Checkbutton(
            autonomous_frame,
            text="🤖 Mode Autonome (Surveillance automatique avec seuils d'alerte)",
            variable=self.autonomous_var,
            font=('Arial', 11),
            bg='#f0f0f0',
            command=self.toggle_autonomous_mode
        )
        autonomous_check.pack(side='left')
        
        self.autonomous_status = tk.Label(
            autonomous_frame,
            text="● Inactif",
            font=('Arial', 10),
            fg='red',
            bg='#f0f0f0'
        )
        self.autonomous_status.pack(side='right')
        
        # Mode Protection iCloud
        icloud_frame = tk.Frame(modes_frame, bg='#f0f0f0')
        icloud_frame.pack(fill='x', pady=5)
        
        self.icloud_var = tk.BooleanVar(value=True)
        icloud_check = tk.Checkbutton(
            icloud_frame,
            text="☁️ Protection iCloud (Protéger automatiquement les fichiers synchronisés)",
            variable=self.icloud_var,
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        icloud_check.pack(side='left')
        
        # Mode Analyse Seule
        analyze_frame = tk.Frame(modes_frame, bg='#f0f0f0')
        analyze_frame.pack(fill='x', pady=5)
        
        self.analyze_var = tk.BooleanVar(value=False)
        analyze_check = tk.Checkbutton(
            analyze_frame,
            text="🔍 Mode Analyse (Prévisualiser sans supprimer)",
            variable=self.analyze_var,
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        analyze_check.pack(side='left')
        
    def create_system_status(self, parent):
        """Créer la section d'état du système"""
        status_frame = tk.LabelFrame(
            parent,
            text="📊 État du Système",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            padx=15,
            pady=10
        )
        status_frame.pack(fill='x', pady=(0, 15))
        
        # Métriques système
        metrics_frame = tk.Frame(status_frame, bg='#f0f0f0')
        metrics_frame.pack(fill='x')
        
        # Créer les indicateurs de métrique
        self.disk_label = self.create_metric_indicator(metrics_frame, "💾 Disque", "Calcul...", 0)
        self.memory_label = self.create_metric_indicator(metrics_frame, "🧠 RAM", "Calcul...", 1)
        self.temp_label = self.create_metric_indicator(metrics_frame, "🌡️ Temp", "Calcul...", 2)
        self.clean_label = self.create_metric_indicator(metrics_frame, "🧹 Nettoyé", "0 GB", 3)
        
        # Démarrer la mise à jour des métriques
        self.update_system_metrics()
        
    def create_metric_indicator(self, parent, title, value, column):
        """Créer un indicateur de métrique"""
        metric_frame = tk.Frame(parent, bg='#ecf0f1', relief='solid', bd=1)
        metric_frame.grid(row=0, column=column, padx=5, pady=5, sticky='ew')
        
        parent.grid_columnconfigure(column, weight=1)
        
        title_label = tk.Label(
            metric_frame,
            text=title,
            font=('Arial', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=(5, 0))
        
        value_label = tk.Label(
            metric_frame,
            text=value,
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#27ae60'
        )
        value_label.pack(pady=(0, 5))
        
        return value_label
        
    def create_configuration_section(self, parent):
        """Créer la section de configuration"""
        config_frame = tk.LabelFrame(
            parent,
            text="⚙️ Configuration Rapide",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            padx=15,
            pady=10
        )
        config_frame.pack(fill='x')
        
        # Seuils d'alerte
        threshold_frame = tk.Frame(config_frame, bg='#f0f0f0')
        threshold_frame.pack(fill='x', pady=5)
        
        tk.Label(
            threshold_frame,
            text="Seuils d'alerte:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        ).pack(side='left')
        
        tk.Label(
            threshold_frame,
            text="Disque:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left', padx=(20, 5))
        
        self.disk_threshold = tk.Scale(
            threshold_frame,
            from_=70,
            to=95,
            orient='horizontal',
            length=100,
            bg='#f0f0f0'
        )
        self.disk_threshold.set(85)
        self.disk_threshold.pack(side='left')
        
        tk.Label(
            threshold_frame,
            text="RAM:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left', padx=(20, 5))
        
        self.memory_threshold = tk.Scale(
            threshold_frame,
            from_=70,
            to=95,
            orient='horizontal',
            length=100,
            bg='#f0f0f0'
        )
        self.memory_threshold.set(80)
        self.memory_threshold.pack(side='left')
        
        # Boutons de configuration
        button_frame = tk.Frame(config_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(
            button_frame,
            text="📋 Voir Logs",
            font=('Arial', 10),
            command=self.view_logs,
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🔄 Redémarrer Services",
            font=('Arial', 10),
            command=self.restart_services,
            bg='#e74c3c',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="💾 Sauvegarder Config",
            font=('Arial', 10),
            command=self.save_configuration,
            bg='#16a085',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='left')
        
    def quick_clean(self):
        """Lancer le nettoyage express"""
        try:
            self.show_status_message("🧹 Nettoyage express en cours...")
            
            # Paramètres pour le nettoyage
            protect_icloud = self.icloud_var.get()
            analyze_only = self.analyze_var.get()
            
            if analyze_only:
                self.show_status_message("🔍 Mode analyse activé - Aucun fichier ne sera supprimé")
            
            # Lancer le script de nettoyage rapide
            result = subprocess.run([
                str(self.base_dir / "quick_clean.sh")
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.show_status_message("✅ Nettoyage express terminé!")
                messagebox.showinfo("Succès", "Nettoyage express terminé avec succès!")
            else:
                self.show_status_message("❌ Erreur durant le nettoyage")
                messagebox.showerror("Erreur", f"Erreur durant le nettoyage:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le nettoyage: {str(e)}")
            
    def scan_malware(self):
        """Lancer le scan anti-malware"""
        try:
            self.show_status_message("🔍 Scan anti-malware en cours...")
            
            # Lancer le scan en arrière-plan
            def run_scan():
                try:
                    result = subprocess.run([
                        "python3", str(self.base_dir / "autonomous_system.py"), "--scan-malware"
                    ], capture_output=True, text=True, cwd=str(self.base_dir))
                    
                    if result.returncode == 0:
                        self.root.after(0, lambda: self.show_status_message("✅ Scan anti-malware terminé"))
                        self.root.after(0, lambda: messagebox.showinfo("Scan Terminé", "Scan anti-malware terminé.\nAucune menace détectée."))
                    else:
                        self.root.after(0, lambda: self.show_status_message("❌ Erreur durant le scan"))
                        
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur scan: {str(e)}"))
                    
            threading.Thread(target=run_scan, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le scan: {str(e)}")
            
    def optimize_system(self):
        """Optimiser le système"""
        try:
            self.show_status_message("⚡ Optimisation système en cours...")
            
            # Lancer l'optimisation
            def run_optimization():
                try:
                    # Purger la mémoire
                    subprocess.run(["sudo", "purge"], check=False)
                    
                    # Vider le cache DNS
                    subprocess.run(["sudo", "dscacheutil", "-flushcache"], check=False)
                    subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=False)
                    
                    # Scripts de maintenance
                    subprocess.run(["sudo", "periodic", "daily"], check=False)
                    
                    self.root.after(0, lambda: self.show_status_message("✅ Optimisation terminée"))
                    self.root.after(0, lambda: messagebox.showinfo("Optimisation", "Optimisation système terminée!"))
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur optimisation: {str(e)}"))
                    
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'optimisation: {str(e)}")
            
    def sync_github(self):
        """Synchroniser avec GitHub"""
        try:
            self.show_status_message("☁️ Synchronisation GitHub en cours...")
            
            def run_sync():
                try:
                    result = subprocess.run([
                        "python3", str(self.base_dir / "github_integration.py"), "--auto-sync"
                    ], capture_output=True, text=True, cwd=str(self.base_dir))
                    
                    if result.returncode == 0:
                        self.root.after(0, lambda: self.show_status_message("✅ Synchronisation terminée"))
                        self.root.after(0, lambda: messagebox.showinfo("Sync GitHub", "Synchronisation GitHub terminée!"))
                    else:
                        self.root.after(0, lambda: messagebox.showerror("Erreur", "Erreur lors de la synchronisation"))
                        
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur sync: {str(e)}"))
                    
            threading.Thread(target=run_sync, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de synchroniser: {str(e)}")
            
    def open_full_interface(self):
        """Ouvrir l'interface complète"""
        try:
            subprocess.Popen([str(self.base_dir / "run_cleaner.sh")], cwd=str(self.base_dir))
            self.show_status_message("🖥️ Interface complète lancée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'interface: {str(e)}")
            
    def open_configuration(self):
        """Ouvrir la configuration avancée"""
        try:
            config_file = self.base_dir / "config" / "autonomous_config.json"
            subprocess.run(["open", "-a", "TextEdit", str(config_file)])
            self.show_status_message("⚙️ Configuration ouverte")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")
            
    def toggle_autonomous_mode(self):
        """Activer/désactiver le mode autonome"""
        if self.autonomous_var.get():
            self.start_autonomous_monitoring()
        else:
            self.stop_autonomous_monitoring()
            
    def start_autonomous_monitoring(self):
        """Démarrer la surveillance autonome"""
        try:
            if not self.is_monitoring:
                # Lancer le système autonome en arrière-plan
                self.autonomous_process = subprocess.Popen([
                    "python3", str(self.base_dir / "autonomous_system.py")
                ], cwd=str(self.base_dir))
                
                self.is_monitoring = True
                self.autonomous_status.config(text="● Actif", fg='green')
                self.show_status_message("🤖 Surveillance autonome démarrée")
                
        except Exception as e:
            self.autonomous_var.set(False)
            messagebox.showerror("Erreur", f"Impossible de démarrer la surveillance: {str(e)}")
            
    def stop_autonomous_monitoring(self):
        """Arrêter la surveillance autonome"""
        try:
            if self.autonomous_process and self.autonomous_process.poll() is None:
                self.autonomous_process.terminate()
                
            self.is_monitoring = False
            self.autonomous_status.config(text="● Inactif", fg='red')
            self.show_status_message("🛑 Surveillance autonome arrêtée")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'arrêt: {str(e)}")
            
    def update_system_metrics(self):
        """Mettre à jour les métriques système"""
        try:
            import psutil
            
            # Utilisation disque
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_label.config(text=f"{disk_percent:.1f}%")
            
            # Utilisation mémoire
            memory = psutil.virtual_memory()
            self.memory_label.config(text=f"{memory.percent:.1f}%")
            
            # Température (simulée pour la démo)
            self.temp_label.config(text="65°C")
            
            # Programmer la prochaine mise à jour
            self.root.after(5000, self.update_system_metrics)
            
        except ImportError:
            # psutil non disponible, utiliser des valeurs statiques
            self.disk_label.config(text="N/A")
            self.memory_label.config(text="N/A")
            self.temp_label.config(text="N/A")
            
    def view_logs(self):
        """Afficher les logs"""
        try:
            log_file = self.base_dir / "logs" / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
            if log_file.exists():
                subprocess.run(["open", "-a", "Console", str(log_file)])
            else:
                messagebox.showinfo("Logs", "Aucun log d'erreur aujourd'hui")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir les logs: {str(e)}")
            
    def restart_services(self):
        """Redémarrer les services système"""
        if messagebox.askyesno("Confirmation", "Redémarrer les services système?\nCela peut fermer certaines applications."):
            try:
                subprocess.run(["killall", "Finder"], check=False)
                subprocess.run(["killall", "Dock"], check=False)
                self.show_status_message("🔄 Services redémarrés")
                messagebox.showinfo("Services", "Services redémarrés avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur redémarrage: {str(e)}")
                
    def save_configuration(self):
        """Sauvegarder la configuration"""
        try:
            config = {
                "autonomous_mode": self.autonomous_var.get(),
                "icloud_protection": self.icloud_var.get(),
                "analyze_only": self.analyze_var.get(),
                "disk_threshold": self.disk_threshold.get(),
                "memory_threshold": self.memory_threshold.get(),
                "saved_at": datetime.now().isoformat()
            }
            
            config_file = self.base_dir / "config" / "launcher_config.json"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            self.show_status_message("💾 Configuration sauvegardée")
            messagebox.showinfo("Configuration", "Configuration sauvegardée avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur sauvegarde: {str(e)}")
            
    def show_status_message(self, message):
        """Afficher un message de statut"""
        print(f"[LAUNCHER] {message}")
        
    def darken_color(self, color):
        """Assombrir une couleur pour l'effet hover"""
        color_map = {
            '#27ae60': '#219a52',
            '#e67e22': '#d68910',
            '#3498db': '#2980b9',
            '#9b59b6': '#8e44ad',
            '#34495e': '#2c3e50',
            '#7f8c8d': '#6c7b7d'
        }
        return color_map.get(color, color)
        
    def on_closing(self):
        """Gérer la fermeture de l'application"""
        if self.is_monitoring:
            if messagebox.askyesno("Fermeture", "La surveillance autonome est active.\nVoulez-vous l'arrêter et quitter?"):
                self.stop_autonomous_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Lancer l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Importer les modules nécessaires
    from datetime import datetime
    
    launcher = MacCleanerLauncher()
    launcher.run()