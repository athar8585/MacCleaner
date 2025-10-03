#!/usr/bin/env python3
"""
MacCleaner Pro - Version Corrigée et Simplifiée
Nettoyage RÉEL en profondeur pour macOS
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
import glob

class MacCleanerPro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MacCleaner Pro - Nettoyage RÉEL")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables de contrôle
        self.cleaning_active = False
        self.total_freed_space = 0
        self.icloud_protected_files = set()
        self.analyzed_files = []
        self.protect_icloud = tk.BooleanVar(value=True)
        self.analyze_only = tk.BooleanVar(value=False)
        
        # Configuration des chemins à nettoyer - RÉELS ET VÉRIFIÉS
        self.cleanup_paths = {
            'Corbeille': [
                '~/.Trash'
            ],
            'Caches Système': [
                '~/Library/Caches',
                '/Library/Caches'
            ],
            'Caches Utilisateur': [
                '~/Library/Application Support/*/Caches',
                '~/Library/Safari/LocalStorage',
                '~/Library/Safari/Databases',
                '~/Library/Cookies'
            ],
            'Logs & Diagnostics': [
                '~/Library/Logs',
                '~/Library/DiagnosticReports'
            ],
            'Fichiers Temporaires': [
                '/tmp/*',
                '/var/tmp/*',
                '~/Library/Application Support/*/tmp'
            ],
            'Téléchargements Anciens': [
                '~/Downloads'
            ]
        }
        
        # Options d'optimisation système
        self.optimize_vars = {}
        self.cleanup_vars = {}
        
        # Interface de log simple mais efficace
        self.create_log_area()
        
    def create_log_area(self):
        """Créer la zone de log principale"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Titre avec statut
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="🧹 MacCleaner Pro - Nettoyage RÉEL", 
                               font=('SF Pro Display', 16, 'bold'))
        title_label.pack(side='left')
        
        self.status_label = ttk.Label(title_frame, text="Prêt", foreground='green')
        self.status_label.pack(side='right')
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="🔍 Journal en Temps Réel", padding="10")
        log_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, 
                                                font=('Monaco', 10),
                                                bg='#1e1e1e', fg='#ffffff')
        self.log_text.pack(fill='both', expand=True)
        
        # Boutons de contrôle
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        # Bouton principal
        self.main_button = ttk.Button(button_frame, text="🚀 ANALYSER D'ABORD", 
                                     command=self.start_analysis,
                                     style='Accent.TButton')
        self.main_button.pack(side='left', padx=(0, 10))
        
        # Bouton nettoyage réel
        self.clean_button = ttk.Button(button_frame, text="🗑️ NETTOYER RÉELLEMENT", 
                                      command=self.start_real_cleaning,
                                      style='Accent.TButton')
        self.clean_button.pack(side='left', padx=(0, 10))
        
        # Bouton stop
        self.stop_button = ttk.Button(button_frame, text="🛑 ARRÊTER", 
                                     command=self.stop_cleaning)
        self.stop_button.pack(side='left', padx=(0, 10))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="5")
        options_frame.pack(fill='x', pady=10)
        
        ttk.Checkbutton(options_frame, text="🔒 Protéger les fichiers iCloud", 
                       variable=self.protect_icloud).pack(side='left', padx=5)
        
        # Barre de progression
        self.progress_var = tk.StringVar(value="En attente...")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.pack(fill='x', pady=5)
        
    def log_message(self, message):
        """Afficher un message dans le log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, full_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
        # Aussi l'afficher dans la console
        print(full_message.strip())
        
    def start_analysis(self):
        """Démarrer l'analyse (mode sécurisé)"""
        if self.cleaning_active:
            return
            
        self.log_message("🔍 DÉBUT DE L'ANALYSE - Aucune suppression")
        self.analyze_only.set(True)
        self.cleaning_active = True
        self.main_button.configure(text="🔄 Analyse...", state='disabled')
        self.status_label.configure(text="Analyse en cours", foreground='orange')
        
        threading.Thread(target=self._analysis_thread, daemon=True).start()
        
    def start_real_cleaning(self):
        """Démarrer le nettoyage RÉEL avec confirmation"""
        if self.cleaning_active:
            return
            
        # Double confirmation pour le nettoyage réel
        warning = """⚠️ ATTENTION - NETTOYAGE RÉEL ⚠️

CE NETTOYAGE VA SUPPRIMER DÉFINITIVEMENT DES FICHIERS !

Actions qui seront effectuées :
• Vider complètement la corbeille (suppression définitive)
• Supprimer les caches système et utilisateur
• Supprimer les fichiers temporaires
• Supprimer les logs anciens

⚠️ CETTE ACTION EST IRRÉVERSIBLE ⚠️

Tapez 'CONFIRMER' pour procéder :"""
        
        # Première confirmation
        response1 = messagebox.askyesno("⚠️ NETTOYAGE RÉEL", 
                                       "Voulez-vous procéder au NETTOYAGE RÉEL ?\n\n⚠️ Les fichiers seront supprimés définitivement !")
        if not response1:
            return
            
        # Deuxième confirmation avec saisie
        from tkinter import simpledialog
        confirmation = simpledialog.askstring("🔐 CONFIRMATION FINALE", 
                                             "Tapez 'CONFIRMER' en majuscules pour procéder :")
        
        if confirmation != "CONFIRMER":
            self.log_message("❌ Nettoyage annulé - confirmation incorrecte")
            return
            
        self.log_message("🚨 DÉBUT DU NETTOYAGE RÉEL - Suppressions définitives !")
        self.analyze_only.set(False)
        self.cleaning_active = True
        self.clean_button.configure(text="🔄 Nettoyage...", state='disabled')
        self.status_label.configure(text="Nettoyage RÉEL", foreground='red')
        
        threading.Thread(target=self._cleaning_thread, daemon=True).start()
        
    def stop_cleaning(self):
        """Arrêter le nettoyage"""
        self.cleaning_active = False
        self.log_message("🛑 Arrêt demandé par l'utilisateur")
        
    def _analysis_thread(self):
        """Thread d'analyse (pas de suppression)"""
        try:
            self.total_freed_space = 0
            self.analyzed_files = []
            
            total_categories = len(self.cleanup_paths)
            current_category = 0
            
            for category, paths in self.cleanup_paths.items():
                if not self.cleaning_active:
                    break
                    
                current_category += 1
                progress = (current_category / total_categories) * 100
                self.progress_bar['value'] = progress
                self.progress_var.set(f"Analyse: {category}")
                
                self.log_message(f"📊 Analyse de {category}...")
                category_size = self.analyze_category(category, paths)
                
                if category_size > 0:
                    self.log_message(f"  📏 {category}: {category_size / (1024*1024):.1f} MB trouvés")
                else:
                    self.log_message(f"  ✅ {category}: Rien à nettoyer")
                    
            self.log_message(f"📊 ANALYSE TERMINÉE")
            self.log_message(f"📏 Espace total récupérable: {self.total_freed_space / (1024*1024):.1f} MB")
            self.log_message(f"📝 {len(self.analyzed_files)} fichiers analysés")
            
            if self.total_freed_space > 0:
                self.log_message("💡 Utilisez 'NETTOYER RÉELLEMENT' pour supprimer ces fichiers")
            
        except Exception as e:
            self.log_message(f"❌ Erreur durant l'analyse: {str(e)}")
        finally:
            self.cleaning_active = False
            self.main_button.configure(text="🚀 ANALYSER D'ABORD", state='normal')
            self.status_label.configure(text="Analyse terminée", foreground='blue')
            self.progress_var.set("Analyse terminée")
            
    def _cleaning_thread(self):
        """Thread de nettoyage RÉEL"""
        try:
            self.total_freed_space = 0
            
            total_categories = len(self.cleanup_paths)
            current_category = 0
            
            for category, paths in self.cleanup_paths.items():
                if not self.cleaning_active:
                    break
                    
                current_category += 1
                progress = (current_category / total_categories) * 100
                self.progress_bar['value'] = progress
                self.progress_var.set(f"Nettoyage: {category}")
                
                self.log_message(f"🗑️ NETTOYAGE RÉEL de {category}...")
                freed_space = self.clean_category_real(category, paths)
                
                if freed_space > 0:
                    self.log_message(f"  ✅ {category}: {freed_space / (1024*1024):.1f} MB libérés")
                else:
                    self.log_message(f"  ℹ️ {category}: Rien à nettoyer")
                    
            self.log_message(f"🎉 NETTOYAGE RÉEL TERMINÉ !")
            self.log_message(f"💾 Espace total libéré: {self.total_freed_space / (1024*1024):.1f} MB")
            
        except Exception as e:
            self.log_message(f"❌ Erreur durant le nettoyage: {str(e)}")
        finally:
            self.cleaning_active = False
            self.clean_button.configure(text="🗑️ NETTOYER RÉELLEMENT", state='normal')
            self.status_label.configure(text="Nettoyage terminé", foreground='green')
            self.progress_var.set("Nettoyage terminé")
            
    def analyze_category(self, category, paths):
        """Analyser une catégorie (pas de suppression)"""
        total_size = 0
        
        for path_pattern in paths:
            if not self.cleaning_active:
                break
                
            expanded_path = os.path.expanduser(path_pattern)
            
            try:
                if '*' in expanded_path:
                    # Gérer les wildcards
                    matching_paths = glob.glob(expanded_path)
                    for path in matching_paths:
                        if os.path.exists(path):
                            size = self.get_path_size(path)
                            total_size += size
                            
                            if size > 0:
                                self.analyzed_files.append({
                                    'path': path,
                                    'size': size,
                                    'category': category
                                })
                else:
                    # Chemin direct
                    if os.path.exists(expanded_path):
                        size = self.get_path_size(expanded_path)
                        total_size += size
                        
                        if size > 0:
                            self.analyzed_files.append({
                                'path': expanded_path,
                                'size': size,
                                'category': category
                            })
                            
            except Exception as e:
                self.log_message(f"  ⚠️ Erreur analyse {expanded_path}: {str(e)}")
                
        self.total_freed_space += total_size
        return total_size
        
    def clean_category_real(self, category, paths):
        """Nettoyer RÉELLEMENT une catégorie"""
        total_freed = 0
        
        for path_pattern in paths:
            if not self.cleaning_active:
                break
                
            expanded_path = os.path.expanduser(path_pattern)
            
            try:
                if '*' in expanded_path:
                    # Gérer les wildcards
                    matching_paths = glob.glob(expanded_path)
                    for path in matching_paths:
                        if os.path.exists(path):
                            freed = self.clean_path_real(path, category)
                            total_freed += freed
                else:
                    # Chemin direct
                    if os.path.exists(expanded_path):
                        freed = self.clean_path_real(expanded_path, category)
                        total_freed += freed
                        
            except Exception as e:
                self.log_message(f"  ❌ Erreur nettoyage {expanded_path}: {str(e)}")
                
        self.total_freed_space += total_freed
        return total_freed
        
    def clean_path_real(self, path, category):
        """Nettoyer RÉELLEMENT un chemin spécifique"""
        if not os.path.exists(path):
            return 0
            
        # Traitement spécial pour la corbeille
        if category == 'Corbeille' or path.endswith('.Trash'):
            return self.empty_trash_completely()
            
        try:
            initial_size = self.get_path_size(path)
            
            if os.path.isfile(path):
                # Vérifier les protections
                if self.should_protect_file(path):
                    self.log_message(f"    🔒 Protégé: {os.path.basename(path)}")
                    return 0
                    
                # Supprimer le fichier
                os.remove(path)
                self.log_message(f"    ✅ Supprimé: {os.path.basename(path)}")
                return initial_size
                
            elif os.path.isdir(path):
                # Nettoyer le contenu du dossier
                return self.clean_directory_contents(path)
                
        except Exception as e:
            self.log_message(f"    ❌ Erreur: {os.path.basename(path)} - {str(e)}")
            return 0
            
        return 0
        
    def empty_trash_completely(self):
        """Vider complètement et définitivement la corbeille"""
        trash_path = os.path.expanduser('~/.Trash')
        
        if not os.path.exists(trash_path):
            self.log_message("    ✅ Corbeille déjà vide")
            return 0
            
        items = os.listdir(trash_path)
        if not items:
            self.log_message("    ✅ Corbeille déjà vide")
            return 0
            
        total_freed = 0
        items_deleted = 0
        
        self.log_message(f"    🗑️ Suppression définitive de {len(items)} éléments...")
        
        for item in items:
            if not self.cleaning_active:
                break
                
            item_path = os.path.join(trash_path, item)
            
            try:
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                    total_freed += size
                    items_deleted += 1
                    self.log_message(f"      ✅ SUPPRIMÉ: {item}")
                    
                elif os.path.isdir(item_path):
                    size = self.get_path_size(item_path)
                    shutil.rmtree(item_path)
                    total_freed += size
                    items_deleted += 1
                    self.log_message(f"      ✅ DOSSIER SUPPRIMÉ: {item}/")
                    
            except Exception as e:
                self.log_message(f"      ⚠️ Permission refusée: {item}")
                # Essayer avec sudo si nécessaire
                try:
                    subprocess.run(['rm', '-rf', item_path], check=True, capture_output=True)
                    items_deleted += 1
                    self.log_message(f"      ✅ FORCÉ: {item}")
                except:
                    self.log_message(f"      ❌ IMPOSSIBLE: {item}")
                    
        # Vérification finale
        remaining = os.listdir(trash_path) if os.path.exists(trash_path) else []
        
        if remaining:
            self.log_message(f"    📊 {items_deleted}/{len(items)} supprimés, {len(remaining)} restants")
        else:
            self.log_message(f"    🎉 CORBEILLE COMPLÈTEMENT VIDE !")
            
        self.log_message(f"    💾 {total_freed / (1024*1024):.1f} MB libérés de la corbeille")
        
        return total_freed
        
    def clean_directory_contents(self, directory):
        """Nettoyer le contenu d'un répertoire"""
        total_freed = 0
        
        try:
            items = os.listdir(directory)
            for item in items:
                if not self.cleaning_active:
                    break
                    
                item_path = os.path.join(directory, item)
                
                try:
                    if os.path.isfile(item_path):
                        if self.should_clean_file(item_path):
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            total_freed += size
                            self.log_message(f"      ✅ {item}")
                            
                    elif os.path.isdir(item_path):
                        # Récursion pour les sous-dossiers
                        sub_freed = self.clean_directory_contents(item_path)
                        total_freed += sub_freed
                        
                        # Supprimer le dossier s'il est vide
                        try:
                            if not os.listdir(item_path):
                                os.rmdir(item_path)
                                self.log_message(f"      ✅ Dossier vide supprimé: {item}/")
                        except:
                            pass
                            
                except Exception as e:
                    self.log_message(f"      ⚠️ {item}: {str(e)}")
                    
        except Exception as e:
            self.log_message(f"    ❌ Erreur répertoire: {str(e)}")
            
        return total_freed
        
    def should_protect_file(self, filepath):
        """Déterminer si un fichier doit être protégé"""
        # Protection iCloud
        if self.protect_icloud.get() and self.is_icloud_file(filepath):
            return True
            
        # Fichiers système critiques
        critical_patterns = [
            '/System/',
            '/usr/bin/',
            '/bin/',
            'com.apple.',
            '.app/Contents/MacOS/'
        ]
        
        for pattern in critical_patterns:
            if pattern in filepath:
                return True
                
        # Fichiers importants récents
        try:
            if os.path.getmtime(filepath) > time.time() - (7 * 24 * 60 * 60):  # 7 jours
                important_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.mp4', '.mov']
                if any(filepath.lower().endswith(ext) for ext in important_extensions):
                    return True
        except:
            pass
            
        return False
        
    def should_clean_file(self, filepath):
        """Déterminer si un fichier doit être nettoyé"""
        if self.should_protect_file(filepath):
            return False
            
        filename = os.path.basename(filepath).lower()
        
        # Extensions à nettoyer
        clean_extensions = [
            '.tmp', '.temp', '.cache', '.log', '.old', '.bak',
            '.crash', '.dmp', '.traces', '.diagnostic'
        ]
        
        # Patterns de fichiers à nettoyer
        clean_patterns = [
            'cache', 'temp', 'tmp', 'log', 'diagnostic'
        ]
        
        # Vérifier les extensions
        for ext in clean_extensions:
            if filename.endswith(ext):
                return True
                
        # Vérifier les patterns
        for pattern in clean_patterns:
            if pattern in filename:
                return True
                
        return False
        
    def is_icloud_file(self, filepath):
        """Détecter si un fichier est synchronisé avec iCloud"""
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
        
    def get_path_size(self, path):
        """Calculer la taille d'un fichier ou dossier"""
        total_size = 0
        
        try:
            if os.path.isfile(path):
                total_size = os.path.getsize(path)
            elif os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        try:
                            filepath = os.path.join(dirpath, filename)
                            total_size += os.path.getsize(filepath)
                        except:
                            pass
        except:
            pass
            
        return total_size
        
    def run(self):
        """Lancer l'application"""
        self.log_message("🚀 MacCleaner Pro - Version Corrigée et Réelle")
        self.log_message("💡 Cliquez sur 'ANALYSER D'ABORD' pour voir ce qui peut être nettoyé")
        self.log_message("⚠️ Puis 'NETTOYER RÉELLEMENT' pour supprimer définitivement")
        self.root.mainloop()

def main():
    """Point d'entrée principal"""
    print("🚀 Lancement de MacCleaner Pro - Version Corrigée")
    
    app = MacCleanerPro()
    app.run()

if __name__ == "__main__":
    main()