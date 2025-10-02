#!/usr/bin/env python3
"""
MacCleaner Pro - Nettoyeur Mac Ultra-Complet
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

class MacCleanerPro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MacCleaner Pro - Nettoyage Ultra-Complet")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables de contrôle
        self.cleaning_active = False
        self.total_freed_space = 0
        self.icloud_protected_files = set()
        self.analyzed_files = []
        self.protect_icloud = tk.BooleanVar(value=True)
        self.analyze_only = tk.BooleanVar(value=False)
        
        # Configuration des chemins à nettoyer
        self.cleanup_paths = {
            'System Caches': [
                '~/Library/Caches',
                '/Library/Caches',
                '/System/Library/Caches',
                '/var/folders'  # Dossiers temp système
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
                '/Library/Logs',
                '~/Library/DiagnosticReports',
                '/Library/DiagnosticReports'
            ],
            'Downloads & Trash': [
                '~/Downloads',
                '~/.Trash',
                '/Volumes/*/.Trashes'
            ],
            'Browser Data': [
                '~/Library/Safari/History.db',
                '~/Library/Application Support/Google/Chrome/Default/History',
                '~/Library/Application Support/Firefox/Profiles/*/places.sqlite'
            ],
            'System Temp': [
                '/tmp',
                '/var/tmp',
                '/private/tmp',
                '/private/var/tmp'
            ]
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configuration de l'interface graphique"""
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
        disk_usage = shutil.disk_usage('/')
        total_gb = disk_usage.total / (1024**3)
        used_gb = disk_usage.used / (1024**3)
        free_gb = disk_usage.free / (1024**3)
        
        memory = psutil.virtual_memory()
        
        info_text = f"""
💾 Disque: {used_gb:.1f}GB utilisé / {total_gb:.1f}GB total ({free_gb:.1f}GB libre)
🧠 RAM: {memory.percent}% utilisée ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)
⚡ CPU: {psutil.cpu_percent(interval=1)}% d'utilisation
🖥️ Système: {os.uname().sysname} {os.uname().release}
        """
        
        self.info_label = ttk.Label(info_frame, text=info_text, font=('Monaco', 10))
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
    def create_cleanup_options(self, parent):
        """Création des options de nettoyage"""
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
        """Création des boutons d'action"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bouton de scan
        self.scan_button = ttk.Button(button_frame, text="🔍 Scanner le Système", 
                                     command=self.scan_system, style='Accent.TButton')
        self.scan_button.grid(row=0, column=0, padx=5)
        
        # Bouton de nettoyage
        self.clean_button = ttk.Button(button_frame, text="🧹 Nettoyer Maintenant", 
                                      command=self.start_cleaning, style='Accent.TButton')
        self.clean_button.grid(row=0, column=1, padx=5)
        
        # Bouton d'optimisation
        self.optimize_button = ttk.Button(button_frame, text="⚡ Optimiser", 
                                         command=self.optimize_system)
        self.optimize_button.grid(row=0, column=2, padx=5)
        
        # Bouton d'analyse iCloud
        self.icloud_button = ttk.Button(button_frame, text="☁️ Analyser iCloud", 
                                       command=self.analyze_icloud)
        self.icloud_button.grid(row=0, column=3, padx=5)
        
        # Bouton de restauration
        self.restore_button = ttk.Button(button_frame, text="↩️ Restaurer", 
                                        command=self.restore_backup)
        self.restore_button.grid(row=0, column=4, padx=5)
        
        # Bouton d'analyse détaillée
        self.analyze_button = ttk.Button(button_frame, text="📊 Rapport Détaillé", 
                                        command=self.generate_detailed_report)
        self.analyze_button.grid(row=0, column=5, padx=5)
        
    def log_message(self, message):
        """Ajouter un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def calculate_size(self, category, paths, label):
        """Calculer la taille des fichiers à nettoyer"""
        try:
            total_size = 0
            for path_pattern in paths:
                expanded_path = os.path.expanduser(path_pattern)
                if os.path.exists(expanded_path):
                    if os.path.isfile(expanded_path):
                        total_size += os.path.getsize(expanded_path)
                    elif os.path.isdir(expanded_path):
                        total_size += self.get_directory_size(expanded_path)
            
            size_mb = total_size / (1024 * 1024)
            if size_mb > 1024:
                size_text = f"{size_mb/1024:.1f} GB"
            else:
                size_text = f"{size_mb:.1f} MB"
                
            label.configure(text=size_text, foreground='green')
        except Exception as e:
            label.configure(text="Erreur", foreground='red')
            
    def get_directory_size(self, path):
        """Calculer la taille d'un répertoire"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
        return total_size
        
    def scan_system(self):
        """Scanner le système pour détecter les problèmes"""
        self.log_message("🔍 Début du scan système...")
        self.progress_var.set("Scan en cours...")
        self.progress_bar['value'] = 0
        
        threading.Thread(target=self._scan_system_thread, daemon=True).start()
        
    def _scan_system_thread(self):
        """Thread de scan système"""
        scan_results = []
        
        # Vérification de l'espace disque
        disk_usage = shutil.disk_usage('/')
        free_percent = (disk_usage.free / disk_usage.total) * 100
        
        if free_percent < 10:
            scan_results.append("⚠️  Espace disque critique (< 10%)")
        elif free_percent < 20:
            scan_results.append("⚠️  Espace disque faible (< 20%)")
            
        self.progress_bar['value'] = 25
        
        # Vérification de la mémoire
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            scan_results.append("⚠️  Utilisation mémoire élevée (> 80%)")
            
        self.progress_bar['value'] = 50
        
        # Vérification des processus
        high_cpu_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 20:
                    high_cpu_processes.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        if high_cpu_processes:
            scan_results.append(f"⚠️  Processus gourmands: {', '.join(high_cpu_processes[:3])}")
            
        self.progress_bar['value'] = 75
        
        # Vérification des fichiers volumineux
        large_files = self.find_large_files()
        if large_files:
            scan_results.append(f"📁 {len(large_files)} fichiers volumineux détectés")
            
        self.progress_bar['value'] = 100
        
        # Affichage des résultats
        if scan_results:
            self.log_message("Problèmes détectés:")
            for result in scan_results:
                self.log_message(f"  {result}")
        else:
            self.log_message("✅ Aucun problème majeur détecté")
            
        self.progress_var.set("Scan terminé")
        
    def find_large_files(self, min_size_gb=1):
        """Trouver les fichiers volumineux"""
        large_files = []
        search_paths = [
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop'),
            os.path.expanduser('~/Documents')
        ]
        
        min_size_bytes = min_size_gb * 1024 * 1024 * 1024
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                if os.path.getsize(filepath) > min_size_bytes:
                                    large_files.append(filepath)
                            except (OSError, IOError):
                                continue
                except (OSError, IOError):
                    continue
                    
        return large_files[:10]  # Limiter à 10 fichiers
        
    def start_cleaning(self):
        """Démarrer le processus de nettoyage"""
        if self.cleaning_active:
            return
            
        response = messagebox.askyesno("Confirmation", 
                                     "Êtes-vous sûr de vouloir procéder au nettoyage ?\n"
                                     "Cette action est irréversible.")
        if not response:
            return
            
        self.cleaning_active = True
        self.clean_button.configure(text="🛑 Arrêter", command=self.stop_cleaning)
        self.total_freed_space = 0
        
        threading.Thread(target=self._cleaning_thread, daemon=True).start()
        
    def _cleaning_thread(self):
        """Thread principal de nettoyage"""
        try:
            self.log_message("🧹 Début du nettoyage approfondi...")
            self.progress_var.set("Nettoyage en cours...")
            
            total_steps = len([k for k, v in self.cleanup_vars.items() if v.get()])
            current_step = 0
            
            # Créer une sauvegarde des préférences importantes
            self.create_backup()
            
            # Nettoyage par catégorie
            for category, var in self.cleanup_vars.items():
                if not var.get() or not self.cleaning_active:
                    continue
                    
                self.log_message(f"Nettoyage: {category}")
                self.clean_category(category)
                
                current_step += 1
                self.progress_bar['value'] = (current_step / total_steps) * 100
                
            # Optimisations avancées
            if self.cleaning_active:
                self.apply_optimizations()
                
            self.log_message(f"✅ Nettoyage terminé! Espace libéré: {self.total_freed_space / (1024*1024):.1f} MB")
            self.progress_var.set("Nettoyage terminé")
            
        except Exception as e:
            self.log_message(f"❌ Erreur: {str(e)}")
        finally:
            self.cleaning_active = False
            self.clean_button.configure(text="🧹 Nettoyer Maintenant", command=self.start_cleaning)
            
    def clean_category(self, category):
        """Nettoyer une catégorie spécifique"""
        paths = self.cleanup_paths.get(category, [])
        
        for path_pattern in paths:
            if not self.cleaning_active:
                break
                
            try:
                expanded_path = os.path.expanduser(path_pattern)
                
                if '*' in expanded_path:
                    # Gérer les patterns avec wildcards
                    self.clean_wildcard_path(expanded_path)
                else:
                    # Nettoyage direct
                    self.clean_path(expanded_path)
                    
            except Exception as e:
                self.log_message(f"Erreur {path_pattern}: {str(e)}")
                
    def clean_path(self, path):
        """Nettoyer un chemin spécifique avec protection iCloud"""
        if not os.path.exists(path):
            return
            
        try:
            if os.path.isfile(path):
                # Vérifier si le fichier est protégé par iCloud
                if self.protect_icloud.get() and self.is_icloud_file(path):
                    self.log_message(f"  🔒 Protégé (iCloud): {os.path.basename(path)}")
                    self.icloud_protected_files.add(path)
                    return
                
                # Mode analyse seulement
                if self.analyze_only.get():
                    size = os.path.getsize(path)
                    self.analyzed_files.append({
                        'path': path,
                        'size': size,
                        'type': 'file',
                        'protected': self.is_icloud_file(path) if self.protect_icloud.get() else False
                    })
                    self.log_message(f"  📊 Analysé: {os.path.basename(path)} ({size/1024:.1f} KB)")
                    return
                
                # Suppression normale
                size = os.path.getsize(path)
                os.remove(path)
                self.total_freed_space += size
                self.log_message(f"  ✅ Supprimé: {os.path.basename(path)}")
                
            elif os.path.isdir(path):
                # Pour les dossiers, analyser le contenu intelligemment
                self.clean_directory_smart(path)
                    
        except OSError as e:
            self.log_message(f"  ❌ Erreur: {str(e)}")
            
    def clean_directory_smart(self, path):
        """Nettoyage intelligent d'un répertoire avec protection iCloud"""
        try:
            for item in os.listdir(path):
                if not self.cleaning_active and not self.analyze_only.get():
                    break
                    
                item_path = os.path.join(path, item)
                
                if os.path.isfile(item_path):
                    # Vérifier protection iCloud
                    if self.protect_icloud.get() and self.is_icloud_file(item_path):
                        self.log_message(f"    🔒 Protégé (iCloud): {item}")
                        self.icloud_protected_files.add(item_path)
                        continue
                    
                    # Vérifier si c'est un fichier important
                    if self.is_important_file(item_path):
                        self.log_message(f"    ⚠️  Important (conservé): {item}")
                        continue
                    
                    if self.analyze_only.get():
                        size = os.path.getsize(item_path)
                        self.analyzed_files.append({
                            'path': item_path,
                            'size': size,
                            'type': 'file',
                            'protected': self.is_icloud_file(item_path) if self.protect_icloud.get() else False,
                            'important': self.is_important_file(item_path)
                        })
                    else:
                        try:
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            self.total_freed_space += size
                        except OSError:
                            pass
                            
                elif os.path.isdir(item_path):
                    if self.analyze_only.get():
                        dir_size = self.get_directory_size(item_path)
                        self.analyzed_files.append({
                            'path': item_path,
                            'size': dir_size,
                            'type': 'directory',
                            'protected': False,
                            'important': self.is_important_directory(item_path)
                        })
                    else:
                        try:
                            # Récursion pour nettoyer les sous-dossiers
                            self.clean_directory_smart(item_path)
                            # Supprimer le dossier s'il est vide
                            if not os.listdir(item_path):
                                os.rmdir(item_path)
                        except OSError:
                            pass
        except OSError:
            pass
            
    def clean_wildcard_path(self, pattern):
        """Nettoyer les chemins avec wildcards"""
        import glob
        matching_paths = glob.glob(pattern)
        
        for path in matching_paths:
            if not self.cleaning_active:
                break
            self.clean_path(path)
            
    def create_backup(self):
        """Créer une sauvegarde des fichiers importants"""
        backup_dir = os.path.expanduser('~/Desktop/MacCleaner_Backup')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
        
        backup_data = {
            'timestamp': timestamp,
            'system_info': {
                'platform': os.uname(),
                'python_version': sys.version
            }
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
            
        self.log_message(f"Sauvegarde créée: {backup_file}")
        
    def apply_optimizations(self):
        """Appliquer les optimisations avancées"""
        self.log_message("⚡ Application des optimisations...")
        
        if self.optimize_vars['purge_memory'].get():
            self.purge_memory()
            
        if self.optimize_vars['clear_dns_cache'].get():
            self.clear_dns_cache()
            
        if self.optimize_vars['repair_permissions'].get():
            self.repair_permissions()
            
        if self.optimize_vars['rebuild_spotlight'].get():
            self.rebuild_spotlight()
            
        if self.optimize_vars['restart_finder'].get():
            self.restart_finder()
            
        if self.optimize_vars['maintenance_scripts'].get():
            self.run_maintenance_scripts()
            
    def purge_memory(self):
        """Purger la mémoire"""
        try:
            subprocess.run(['sudo', 'purge'], check=True, capture_output=True)
            self.log_message("  ✅ Mémoire purgée")
        except subprocess.CalledProcessError:
            self.log_message("  ❌ Erreur purge mémoire (sudo requis)")
            
    def clear_dns_cache(self):
        """Vider le cache DNS"""
        try:
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], check=True, capture_output=True)
            subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True, capture_output=True)
            self.log_message("  ✅ Cache DNS vidé")
        except subprocess.CalledProcessError:
            self.log_message("  ❌ Erreur cache DNS")
            
    def repair_permissions(self):
        """Réparer les permissions"""
        try:
            subprocess.run(['diskutil', 'resetUserPermissions', '/', '`id -u`'], 
                         shell=True, check=True, capture_output=True)
            self.log_message("  ✅ Permissions réparées")
        except subprocess.CalledProcessError:
            self.log_message("  ❌ Erreur réparation permissions")
            
    def rebuild_spotlight(self):
        """Reconstruire l'index Spotlight"""
        try:
            subprocess.run(['sudo', 'mdutil', '-E', '/'], check=True, capture_output=True)
            self.log_message("  ✅ Index Spotlight en reconstruction")
        except subprocess.CalledProcessError:
            self.log_message("  ❌ Erreur Spotlight")
            
    def restart_finder(self):
        """Redémarrer le Finder"""
        try:
            subprocess.run(['killall', 'Finder'], check=True, capture_output=True)
            self.log_message("  ✅ Finder redémarré")
        except subprocess.CalledProcessError:
            self.log_message("  ❌ Erreur redémarrage Finder")
            
    def run_maintenance_scripts(self):
        """Exécuter les scripts de maintenance système"""
        maintenance_commands = [
            ['sudo', 'periodic', 'daily'],
            ['sudo', 'periodic', 'weekly'],
            ['sudo', 'periodic', 'monthly']
        ]
        
        for cmd in maintenance_commands:
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                self.log_message(f"  ✅ Maintenance {cmd[2]} exécutée")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                self.log_message(f"  ❌ Erreur maintenance {cmd[2]}")
                
    def optimize_system(self):
        """Optimisations système rapides"""
        self.log_message("⚡ Optimisation express...")
        
        # Nettoyer les caches système rapidement
        cache_dirs = [
            os.path.expanduser('~/Library/Caches'),
            '/tmp'
        ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    for item in os.listdir(cache_dir):
                        item_path = os.path.join(cache_dir, item)
                        if os.path.isfile(item_path) and item.endswith(('.log', '.tmp')):
                            os.remove(item_path)
                except OSError:
                    pass
                    
        self.log_message("✅ Optimisation express terminée")
        
    def restore_backup(self):
        """Restaurer une sauvegarde"""
        backup_dir = os.path.expanduser('~/Desktop/MacCleaner_Backup')
        if not os.path.exists(backup_dir):
            messagebox.showwarning("Attention", "Aucune sauvegarde trouvée")
            return
            
        backups = [f for f in os.listdir(backup_dir) if f.startswith('backup_')]
        if not backups:
            messagebox.showwarning("Attention", "Aucune sauvegarde trouvée")
            return
            
        latest_backup = sorted(backups)[-1]
        messagebox.showinfo("Sauvegarde", f"Sauvegarde disponible: {latest_backup}")
        
    def stop_cleaning(self):
        """Arrêter le nettoyage"""
        self.cleaning_active = False
        self.log_message("🛑 Nettoyage arrêté par l'utilisateur")
        
    def is_icloud_file(self, filepath):
        """Détecter si un fichier est synchronisé avec iCloud"""
        try:
            # Vérifier les attributs étendus pour iCloud
            import xattr
            attrs = xattr.listxattr(filepath)
            
            # Chercher les attributs iCloud
            icloud_attrs = [
                'com.apple.clouddocs.sync',
                'com.apple.clouddocs',
                'com.apple.metadata:com_apple_backup_excludeItem'
            ]
            
            for attr in attrs:
                if any(icloud_attr in attr.decode('utf-8', errors='ignore') for icloud_attr in icloud_attrs):
                    return True
                    
            # Vérifier si le fichier est dans un dossier iCloud Drive
            icloud_paths = [
                os.path.expanduser('~/Library/Mobile Documents'),
                os.path.expanduser('~/iCloud Drive'),
                os.path.expanduser('~/Documents') # Peut être synchronisé
            ]
            
            for icloud_path in icloud_paths:
                if filepath.startswith(icloud_path):
                    return True
                    
        except Exception:
            # Si xattr n'est pas disponible, utiliser les chemins
            icloud_indicators = [
                '/Mobile Documents/',
                '/iCloud Drive/',
                '.icloud',
                'com~apple~CloudDocs'
            ]
            
            for indicator in icloud_indicators:
                if indicator in filepath:
                    return True
                    
        return False
        
    def is_important_file(self, filepath):
        """Détecter si un fichier est important et ne doit pas être supprimé"""
        filename = os.path.basename(filepath).lower()
        
        # Extensions de fichiers importants
        important_extensions = [
            '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.pptx', '.ppt',
            '.txt', '.rtf', '.pages', '.numbers', '.keynote',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic',
            '.mp4', '.mov', '.avi', '.mkv', '.mp3', '.wav', '.aac',
            '.zip', '.rar', '.7z', '.dmg', '.pkg',
            '.py', '.js', '.html', '.css', '.json', '.xml',
            '.sketch', '.fig', '.ai', '.psd'
        ]
        
        # Vérifier l'extension
        for ext in important_extensions:
            if filename.endswith(ext):
                return True
                
        # Mots-clés importants dans le nom
        important_keywords = [
            'backup', 'sauvegarde', 'important', 'projet', 'document',
            'photo', 'image', 'video', 'musique', 'personnel'
        ]
        
        for keyword in important_keywords:
            if keyword in filename:
                return True
                
        # Fichiers récents (moins de 7 jours)
        try:
            file_time = os.path.getmtime(filepath)
            seven_days_ago = time.time() - (7 * 24 * 60 * 60)
            if file_time > seven_days_ago:
                return True
        except OSError:
            pass
            
        return False
        
    def is_important_directory(self, dirpath):
        """Détecter si un répertoire est important"""
        dirname = os.path.basename(dirpath).lower()
        
        important_dirs = [
            'documents', 'desktop', 'downloads', 'pictures', 'movies',
            'music', 'projects', 'backup', 'important', 'work'
        ]
        
        return any(important_dir in dirname for important_dir in important_dirs)
        
    def analyze_icloud(self):
        """Analyser les fichiers iCloud et leur statut"""
        self.log_message("☁️ Analyse des fichiers iCloud...")
        
        threading.Thread(target=self._analyze_icloud_thread, daemon=True).start()
        
    def _analyze_icloud_thread(self):
        """Thread d'analyse iCloud"""
        try:
            icloud_paths = [
                os.path.expanduser('~/Library/Mobile Documents'),
                os.path.expanduser('~/Documents'),
                os.path.expanduser('~/Desktop')
            ]
            
            total_icloud_files = 0
            total_icloud_size = 0
            
            for base_path in icloud_paths:
                if os.path.exists(base_path):
                    for root, dirs, files in os.walk(base_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            if self.is_icloud_file(filepath):
                                total_icloud_files += 1
                                try:
                                    total_icloud_size += os.path.getsize(filepath)
                                except OSError:
                                    pass
                                    
            size_mb = total_icloud_size / (1024 * 1024)
            self.log_message(f"📊 Fichiers iCloud détectés: {total_icloud_files}")
            self.log_message(f"📊 Taille totale iCloud: {size_mb:.1f} MB")
            
            if total_icloud_files > 0:
                self.log_message("✅ Protection iCloud active - ces fichiers seront préservés")
            else:
                self.log_message("ℹ️  Aucun fichier iCloud détecté dans les dossiers analysés")
                
        except Exception as e:
            self.log_message(f"❌ Erreur analyse iCloud: {str(e)}")
            
    def generate_detailed_report(self):
        """Générer un rapport détaillé des fichiers analysés"""
        if not self.analyzed_files:
            self.log_message("⚠️  Aucune analyse disponible. Lancez d'abord une analyse.")
            return
            
        self.log_message("📊 Génération du rapport détaillé...")
        
        # Créer le rapport
        report_file = os.path.expanduser(f"~/Desktop/MacCleaner_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# MacCleaner Pro - Rapport Détaillé\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Statistiques générales
                total_files = len(self.analyzed_files)
                total_size = sum(item['size'] for item in self.analyzed_files)
                protected_files = len([item for item in self.analyzed_files if item.get('protected', False)])
                important_files = len([item for item in self.analyzed_files if item.get('important', False)])
                
                f.write(f"## Statistiques\n")
                f.write(f"- Fichiers analysés: {total_files}\n")
                f.write(f"- Taille totale: {total_size / (1024*1024):.1f} MB\n")
                f.write(f"- Fichiers protégés (iCloud): {protected_files}\n")
                f.write(f"- Fichiers importants: {important_files}\n\n")
                
                # Détail par catégorie
                f.write("## Détail des fichiers\n\n")
                
                for item in sorted(self.analyzed_files, key=lambda x: x['size'], reverse=True):
                    status = []
                    if item.get('protected', False):
                        status.append("iCloud")
                    if item.get('important', False):
                        status.append("Important")
                        
                    status_str = f" [{', '.join(status)}]" if status else ""
                    size_str = f"{item['size'] / (1024*1024):.2f} MB" if item['size'] > 1024*1024 else f"{item['size'] / 1024:.1f} KB"
                    
                    f.write(f"- {item['path']} ({size_str}){status_str}\n")
                    
            self.log_message(f"📄 Rapport généré: {report_file}")
            
            # Ouvrir le rapport
            subprocess.run(['open', report_file])
            
        except Exception as e:
            self.log_message(f"❌ Erreur génération rapport: {str(e)}")
        
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Vérifier les permissions
    if os.geteuid() == 0:
        print("⚠️  Ce script ne doit pas être lancé avec sudo")
        sys.exit(1)
        
    app = MacCleanerPro()
    app.run()