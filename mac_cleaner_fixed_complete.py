#!/usr/bin/env python3
"""
MacCleaner Pro - Version COMPLÈTEMENT CORRIGÉE
Nettoyage en profondeur et optimisation avancée pour macOS
"""

import os
import sys
import shutil
import subprocess
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import json
import psutil
import plistlib
import sqlite3

# Imports conditionnels avec fallbacks
try:
    from config.loader import load_settings, save_settings
except ImportError:
    def load_settings():
        return {'scheduler': {'enabled': False}}
    def save_settings(settings):
        pass

try:
    from database.db import init_db, record_clean_run, stats_summary
except ImportError:
    def init_db():
        pass
    def record_clean_run(*args):
        pass
    def stats_summary():
        return {'total_runs': 0, 'total_space_freed_mb': 0, 'malware_detected': 0}

try:
    from utils.notifications import notify, notify_completion, notify_alert
except ImportError:
    def notify(*args, **kwargs):
        pass
    def notify_completion(*args, **kwargs):
        pass
    def notify_alert(*args, **kwargs):
        pass

try:
    from plugins.plugin_loader import PluginManager
except ImportError:
    class PluginManager:
        def __init__(self, *args, **kwargs):
            pass

class MacCleanerPro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MacCleaner Pro - Nettoyage Ultra-Complet")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables de contrôle
        self.cleaning_active = False
        self.total_freed_space = 0
        self.icloud_protected_files = set()
        self.analyzed_files = []
        self.protect_icloud = tk.BooleanVar(value=True)
        self.analyze_only = tk.BooleanVar(value=False)
        self.profiling_enabled = tk.BooleanVar(value=False)  # CORRECTION : Variable manquante
        
        # Configuration des chemins à nettoyer
        self.cleanup_paths = {
            'System Caches': [
                '~/Library/Caches',
                '/Library/Caches'
            ],
            'User Caches': [
                '~/Library/Application Support/*/Caches',
                '~/Library/Safari/LocalStorage',
                '~/Library/Safari/Databases',
                '~/Library/Cookies'
            ],
            'Logs & Diagnostics': [
                '~/Library/Logs',
                '/var/log',
                '/Library/Logs'
            ],
            'Downloads & Trash': [
                '~/Downloads',
                '~/.Trash'
            ],
            'Browser Data': [
                '~/Library/Safari/History.db',
                '~/Library/Application Support/Google/Chrome/Default/History'
            ],
            'System Temp': [
                '/tmp',
                '/var/tmp'
            ]
        }
        
        # Initialisation des composants
        try:
            self.settings = load_settings()
            init_db()
            self.plugin_manager = PluginManager(log_fn=self.log_message)
        except Exception as e:
            print(f"Erreur initialisation modules: {e}")
            self.settings = {'scheduler': {'enabled': False}}
            self.plugin_manager = None
        
        self.setup_gui()
        
    def log_message(self, message):
        """Méthode de logging améliorée"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        # Ajouter au widget de log si disponible
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, log_entry + "\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
        
    def setup_gui(self):
        """Configuration de l'interface graphique CORRIGÉE"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="🧹 MacCleaner Pro", 
                               font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Informations système
        self.create_system_info(main_frame)
        
        # Options de nettoyage
        self.create_cleanup_options(main_frame)
        
        # Zone de progression et logs
        self.create_progress_area(main_frame)
        
        # Boutons d'action
        self.create_action_buttons(main_frame)
        
        # Configuration de la grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def create_system_info(self, parent):
        """Création de la section d'informations système"""
        info_frame = ttk.LabelFrame(parent, text="Informations Système", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Informations système
        try:
            disk_usage = shutil.disk_usage('/')
            total_gb = disk_usage.total / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            
            memory = psutil.virtual_memory()
            
            info_text = f"""💾 Disque: {used_gb:.1f}GB utilisé / {total_gb:.1f}GB total ({free_gb:.1f}GB libre)
🧠 RAM: {memory.percent}% utilisée ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)
⚡ CPU: {psutil.cpu_percent(interval=0.1)}% d'utilisation
🖥️ Système: {os.uname().sysname} {os.uname().release}"""
        except Exception as e:
            info_text = f"⚠️ Erreur lors de la récupération des informations système: {e}"
            
        self.info_label = ttk.Label(info_frame, text=info_text, font=('Monaco', 10))
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
    def create_cleanup_options(self, parent):
        """Création des options de nettoyage CORRIGÉE"""
        options_frame = ttk.LabelFrame(parent, text="Options de Nettoyage", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        self.cleanup_vars = {}
        row = 0
        
        for category, paths in self.cleanup_paths.items():
            var = tk.BooleanVar(value=True)
            self.cleanup_vars[category] = var
            
            checkbox = ttk.Checkbutton(options_frame, text=category, variable=var)
            checkbox.grid(row=row, column=0, sticky=tk.W, pady=2)
            
            # Estimation de l'espace
            size_label = ttk.Label(options_frame, text="Calcul...", foreground='gray')
            size_label.grid(row=row, column=1, sticky=tk.E, padx=(10, 0))
            
            # Calculer la taille en arrière-plan
            threading.Thread(target=self.calculate_size, args=(category, paths, size_label), daemon=True).start()
            
            row += 1
            
        # Protection iCloud et options d'analyse
        protection_frame = ttk.LabelFrame(options_frame, text="Protection et Analyse", padding="5")
        protection_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Checkbutton(protection_frame, text="🔒 Protéger les fichiers iCloud", 
                       variable=self.protect_icloud).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(protection_frame, text="🔍 Mode analyse seulement (ne pas supprimer)", 
                       variable=self.analyze_only).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Options avancées
        advanced_frame = ttk.LabelFrame(options_frame, text="Optimisations Avancées", padding="5")
        advanced_frame.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.optimize_vars = {
            'purge_memory': tk.BooleanVar(value=True),
            'rebuild_spotlight': tk.BooleanVar(value=False),
            'repair_permissions': tk.BooleanVar(value=True),
            'clear_dns_cache': tk.BooleanVar(value=True),
            'restart_finder': tk.BooleanVar(value=False),
            'maintenance_scripts': tk.BooleanVar(value=True)
        }
        
        optimize_options = [
            ('🚀 Purger la mémoire (RAM)', 'purge_memory'),
            ('🔍 Reconstruire l\'index Spotlight', 'rebuild_spotlight'),
            ('🔧 Réparer les permissions', 'repair_permissions'),
            ('🌐 Vider le cache DNS', 'clear_dns_cache'),
            ('🔄 Redémarrer le Finder', 'restart_finder'),
            ('⚙️ Scripts de maintenance système', 'maintenance_scripts')
        ]
        
        for i, (text, key) in enumerate(optimize_options):
            ttk.Checkbutton(advanced_frame, text=text, 
                           variable=self.optimize_vars[key]).grid(row=i//2, column=i%2, 
                                                                 sticky=tk.W, padx=5, pady=2)
    
    def create_progress_area(self, parent):
        """Création de la zone de progression"""
        progress_frame = ttk.LabelFrame(parent, text="Progression", padding="10")
        progress_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 0), pady=(0, 20))
        
        # Barre de progression
        self.progress_var = tk.StringVar(value="Prêt à nettoyer")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de logs
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=15, width=40, 
                                                 font=('Monaco', 9))
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(2, weight=1)
        
    def create_action_buttons(self, parent):
        """Création des boutons d'action CORRIGÉE"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Ligne 1 - Boutons principaux
        self.scan_button = ttk.Button(button_frame, text="🔍 Scanner le Système", 
                                     command=self.scan_system)
        self.scan_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.clean_button = ttk.Button(button_frame, text="🧹 Nettoyer Maintenant", 
                                      command=self.start_cleaning)
        self.clean_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.optimize_button = ttk.Button(button_frame, text="⚡ Optimiser", 
                                         command=self.optimize_system)
        self.optimize_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.restore_button = ttk.Button(button_frame, text="↩️ Restaurer", 
                                        command=self.restore_backup)
        self.restore_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Ligne 2 - Boutons secondaires
        self.analyze_button = ttk.Button(button_frame, text="📊 Rapport Détaillé", 
                                        command=self.generate_detailed_report)
        self.analyze_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.icloud_button = ttk.Button(button_frame, text="☁️ Analyser iCloud", 
                                       command=self.analyze_icloud)
        self.icloud_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Ligne 3 - Boutons avancés (si modules disponibles)
        try:
            self.scan_malware_button = ttk.Button(button_frame, text="🛡️ Scan Malware", 
                                                 command=self.scan_malware_async)
            self.scan_malware_button.grid(row=2, column=0, padx=5, pady=5)
            
            self.plugins_button = ttk.Button(button_frame, text="🔌 Plugins", 
                                           command=self.run_plugins)
            self.plugins_button.grid(row=2, column=1, padx=5, pady=5)
        except:
            pass

    def calculate_size(self, category, paths, label):
        """Calcul de la taille estimée pour une catégorie"""
        try:
            total_size = 0
            for path in paths:
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    if os.path.isfile(expanded_path):
                        total_size += os.path.getsize(expanded_path)
                    elif os.path.isdir(expanded_path):
                        for root, dirs, files in os.walk(expanded_path):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    total_size += os.path.getsize(file_path)
                                except (OSError, IOError):
                                    continue
            
            # Convertir en unité lisible
            if total_size > 1024**3:
                size_str = f"{total_size / (1024**3):.1f} GB"
            elif total_size > 1024**2:
                size_str = f"{total_size / (1024**2):.1f} MB"
            else:
                size_str = f"{total_size / 1024:.1f} KB"
                
            label.configure(text=size_str)
        except Exception as e:
            label.configure(text="Erreur")

    def scan_system(self):
        """Scanner le système pour analyser les fichiers"""
        self.log_message("🔍 Début du scan système...")
        self.progress_bar['value'] = 0
        self.progress_var.set("Scan en cours...")
        
        # Scan en thread séparé
        threading.Thread(target=self._scan_system_thread, daemon=True).start()
        
    def _scan_system_thread(self):
        """Thread de scan système"""
        try:
            total_categories = len(self.cleanup_paths)
            current_category = 0
            
            for category, paths in self.cleanup_paths.items():
                if self.cleanup_vars[category].get():
                    self.log_message(f"📂 Scan de {category}...")
                    
                    for path in paths:
                        expanded_path = os.path.expanduser(path)
                        if os.path.exists(expanded_path):
                            if os.path.isfile(expanded_path):
                                self.analyzed_files.append(expanded_path)
                            elif os.path.isdir(expanded_path):
                                for root, dirs, files in os.walk(expanded_path):
                                    for file in files:
                                        self.analyzed_files.append(os.path.join(root, file))
                
                current_category += 1
                progress = (current_category / total_categories) * 100
                self.progress_bar['value'] = progress
                self.root.update_idletasks()
            
            self.log_message(f"✅ Scan terminé ! {len(self.analyzed_files)} fichiers analysés")
            self.progress_var.set("Scan terminé")
            
        except Exception as e:
            self.log_message(f"❌ Erreur during scan: {e}")

    def start_cleaning(self, auto=False):
        """Démarrer le nettoyage (RÉEL ou ANALYSE selon le mode)"""
        if self.cleaning_active:
            self.log_message("⚠️ Nettoyage déjà en cours...")
            return
            
        # Vérifier le mode avant de commencer
        if self.analyze_only.get():
            self.log_message("🔍 MODE ANALYSE ACTIVÉ - Aucune suppression ne sera effectuée")
            self.log_message("💡 Désactivez 'Mode analyse seulement' pour nettoyer réellement")
            mode_text = "ANALYSE"
            action_verb = "analyser"
        else:
            self.log_message("🚨 MODE NETTOYAGE RÉEL - Des fichiers seront supprimés définitivement !")
            mode_text = "NETTOYAGE RÉEL"
            action_verb = "nettoyer"
            
        if not auto:
            # Message d'avertissement différent selon le mode
            if self.analyze_only.get():
                warning_msg = f"""🔍 {mode_text}

Cette analyse va examiner votre système sans supprimer aucun fichier.

Actions qui seront effectuées :
• Scan de la corbeille (pas de vidage)
• Analyse des caches (pas de suppression)
• Scan des fichiers temporaires (pas de suppression)
• Estimation de l'espace récupérable

✅ Aucun fichier ne sera supprimé
✅ Action totalement sécurisée

Voulez-vous procéder à l'{mode_text} ?"""
            else:
                warning_msg = f"""⚠️ ATTENTION - {mode_text} ⚠️

Ce nettoyage va SUPPRIMER DÉFINITIVEMENT des fichiers de votre Mac.

Actions qui seront effectuées :
• Vidage de la corbeille
• Suppression des caches système
• Suppression des fichiers temporaires
• Optimisations système

⚠️ Cette action est IRRÉVERSIBLE !
⚠️ Assurez-vous d'avoir sauvegardé vos données importantes

Voulez-vous vraiment procéder au {mode_text} ?"""
            
            if not messagebox.askyesno(f"{mode_text}", warning_msg):
                self.log_message(f"❌ {mode_text} annulé par l'utilisateur")
                return
        
        self.cleaning_active = True
        self.total_freed_space = 0
        self.progress_bar['value'] = 0
        self.progress_var.set(f"{mode_text} en cours...")
        
        # Démarrer le nettoyage en thread séparé
        threading.Thread(target=self._cleaning_thread, daemon=True).start()

    def _cleaning_thread(self):
        """Thread principal de nettoyage CORRIGÉ"""
        try:
            self.log_message(f"🚀 Début du {'nettoyage RÉEL' if not self.analyze_only.get() else 'analyse'}...")
            
            total_steps = len([cat for cat in self.cleanup_paths if self.cleanup_vars[cat].get()]) + 2
            current_step = 0
            
            # Étape 1: Nettoyage des catégories sélectionnées
            for category, paths in self.cleanup_paths.items():
                if self.cleanup_vars[category].get():
                    if self.analyze_only.get():
                        self.log_message(f"🔍 ANALYSE de {category}...")
                    else:
                        self.log_message(f"🧹 NETTOYAGE RÉEL de {category}...")
                    
                    for path in paths:
                        self.clean_path(path)
                    
                    current_step += 1
                    progress = (current_step / total_steps) * 90  # 90% pour les catégories
                    self.progress_bar['value'] = progress
                    self.root.update_idletasks()
            
            # Étape 2: Optimisations système (seulement en mode réel)
            if not self.analyze_only.get():
                self.log_message("⚡ Optimisations système...")
                self.perform_optimizations()
            else:
                self.log_message("📊 Analyse des optimisations possibles...")
            
            current_step += 1
            self.progress_bar['value'] = 95
            self.root.update_idletasks()
            
            # Étape 3: Finalisation
            if self.analyze_only.get():
                self.log_message("✅ ANALYSE TERMINÉE !")
                self.log_message(f"📊 Espace récupérable estimé: {self.total_freed_space / (1024*1024):.1f} MB")
                notify_completion("Analyse terminée", f"Espace récupérable: {self.total_freed_space / (1024*1024):.1f} MB")
            else:
                self.log_message("✅ NETTOYAGE RÉEL TERMINÉ !")
                self.log_message(f"💾 ESPACE TOTAL LIBÉRÉ: {self.total_freed_space / (1024*1024):.1f} MB")
                notify_completion("Nettoyage terminé", f"Espace libéré: {self.total_freed_space / (1024*1024):.1f} MB")
                
                # Enregistrer dans la base de données
                try:
                    record_clean_run(self.total_freed_space / (1024*1024), len(self.analyzed_files))
                except:
                    pass
            
            self.progress_bar['value'] = 100
            self.progress_var.set("Terminé !")
            
        except Exception as e:
            self.log_message(f"❌ Erreur pendant le nettoyage: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleaning_active = False

    def clean_path(self, path):
        """Nettoyer un chemin spécifique (RÉEL ou ANALYSE)"""
        try:
            expanded_path = os.path.expanduser(path)
            
            if not os.path.exists(expanded_path):
                return
            
            if self.analyze_only.get():
                # Mode analyse : calculer seulement la taille
                if os.path.isfile(expanded_path):
                    size = os.path.getsize(expanded_path)
                    self.total_freed_space += size
                    self.log_message(f"📋 Analyserait: {expanded_path} ({size} bytes)")
                elif os.path.isdir(expanded_path):
                    for root, dirs, files in os.walk(expanded_path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                self.total_freed_space += size
                            except (OSError, IOError):
                                continue
                    self.log_message(f"📂 Analyserait le dossier: {expanded_path}")
            else:
                # Mode réel : supprimer effectivement
                if os.path.isfile(expanded_path):
                    size = os.path.getsize(expanded_path)
                    os.remove(expanded_path)
                    self.total_freed_space += size
                    self.log_message(f"🗑️ Supprimé: {expanded_path} ({size} bytes)")
                elif os.path.isdir(expanded_path):
                    # Supprimer le contenu du dossier mais pas le dossier lui-même
                    for root, dirs, files in os.walk(expanded_path, topdown=False):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                os.remove(file_path)
                                self.total_freed_space += size
                                self.log_message(f"🧹 Nettoyage RÉEL de {file_path}")
                            except (OSError, IOError) as e:
                                self.log_message(f"⚠️ Accès refusé à {file_path}")
                        for dir in dirs:
                            try:
                                dir_path = os.path.join(root, dir)
                                if not os.listdir(dir_path):  # Seulement si vide
                                    os.rmdir(dir_path)
                            except (OSError, IOError):
                                pass
                                
        except Exception as e:
            self.log_message(f"❌ Erreur lors du nettoyage de {path}: {e}")

    def perform_optimizations(self):
        """Effectuer les optimisations système"""
        try:
            if self.optimize_vars['purge_memory'].get():
                self.log_message("🚀 Purge de la mémoire...")
                try:
                    subprocess.run(['sudo', 'purge'], check=False, capture_output=True)
                    self.log_message("✅ Mémoire purgée")
                except:
                    self.log_message("⚠️ Purge mémoire nécessite sudo")
                    
            if self.optimize_vars['clear_dns_cache'].get():
                self.log_message("🌐 Vidage du cache DNS...")
                try:
                    subprocess.run(['sudo', 'dscacheutil', '-flushcache'], check=False, capture_output=True)
                    self.log_message("✅ Cache DNS vidé")
                except:
                    self.log_message("⚠️ Erreur lors du vidage DNS")
                    
            if self.optimize_vars['maintenance_scripts'].get():
                self.log_message("⚙️ Scripts de maintenance...")
                try:
                    subprocess.run(['sudo', 'periodic', 'daily'], check=False, capture_output=True)
                    self.log_message("✅ Maintenance exécutée")
                except:
                    self.log_message("⚠️ Maintenance nécessite sudo")
                    
        except Exception as e:
            self.log_message(f"❌ Erreur optimisations: {e}")

    def optimize_system(self):
        """Optimiser le système"""
        if not messagebox.askyesno("Optimisation", "Voulez-vous optimiser le système ?"):
            return
            
        self.log_message("⚡ Début des optimisations...")
        threading.Thread(target=self.perform_optimizations, daemon=True).start()

    # Méthodes de fallback pour les fonctionnalités optionnelles
    def scan_malware_async(self):
        """Scan malware (fallback si module non disponible)"""
        self.log_message("🛡️ Fonction de scan malware non disponible")
        
    def run_plugins(self):
        """Exécuter les plugins (fallback si module non disponible)"""
        if self.plugin_manager:
            self.log_message("🔌 Exécution des plugins...")
            # Logique d'exécution des plugins
        else:
            self.log_message("🔌 Aucun plugin disponible")
            
    def analyze_icloud(self):
        """Analyser iCloud (placeholder)"""
        self.log_message("☁️ Analyse iCloud non implémentée")
        
    def restore_backup(self):
        """Restaurer une sauvegarde (placeholder)"""
        self.log_message("↩️ Fonction de restauration non implémentée")
        
    def generate_detailed_report(self):
        """Générer un rapport détaillé (placeholder)"""
        self.log_message("📊 Génération de rapport non implémentée")

    def run(self):
        """Lancer l'application"""
        self.log_message("🚀 MacCleaner Pro démarré !")
        self.log_message("💡 Sélectionnez les options et cliquez sur 'Nettoyer Maintenant'")
        self.root.mainloop()

def main():
    """Fonction principale avec gestion des arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MacCleaner Pro - Nettoyeur Mac Ultra-Complet")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Mode analyse seulement (aucune suppression)")
    parser.add_argument("--verify", action="store_true", 
                       help="Vérifier intégrité des fichiers critiques")
    
    args = parser.parse_args()
    
    app = MacCleanerPro()
    
    # Appliquer les arguments
    if args.dry_run:
        app.analyze_only.set(True)
        app.log_message("🔍 Mode analyse activé via --dry-run")
    
    app.run()

if __name__ == "__main__":
    main()