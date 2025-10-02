#!/usr/bin/env python3
"""
MacCleaner Guardian - ASSISTANT INTELLIGENT
Assistant de notification et surveillance en temps réel
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
import subprocess
from pathlib import Path

class GuardianAssistant:
    """Assistant intelligent flottant pour MacCleaner Guardian"""
    
    def __init__(self):
        self.root = None
        self.is_visible = True
        self.last_update = datetime.now()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface assistant"""
        self.root = tk.Tk()
        self.root.title("Guardian Assistant")
        
        # Fenêtre flottante, toujours au-dessus
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.root.overrideredirect(True)  # Supprime la barre de titre
        
        # Position en haut à droite
        self.root.geometry("320x180+1000+50")
        
        # Style moderne
        self.root.configure(bg='#1e1e1e')
        
        # Frame principal avec bordure arrondie (simulée)
        self.main_frame = tk.Frame(self.root, bg='#1e1e1e', relief='solid', bd=1)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Header avec titre et boutons
        self.header_frame = tk.Frame(self.main_frame, bg='#2d2d2d', height=30)
        self.header_frame.pack(fill=tk.X, padx=2, pady=(2, 0))
        self.header_frame.pack_propagate(False)
        
        # Titre
        self.title_label = tk.Label(
            self.header_frame, 
            text="🛡️ Guardian Assistant",
            bg='#2d2d2d', fg='#ffffff', 
            font=('SF Pro Display', 10, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=8, pady=5)
        
        # Bouton minimiser/restaurer
        self.toggle_btn = tk.Button(
            self.header_frame,
            text="−", bg='#3d3d3d', fg='#ffffff',
            font=('Arial', 8, 'bold'),
            relief='flat', bd=0,
            command=self.toggle_visibility,
            width=2, height=1
        )
        self.toggle_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Bouton fermer
        self.close_btn = tk.Button(
            self.header_frame,
            text="×", bg='#e74c3c', fg='#ffffff',
            font=('Arial', 8, 'bold'),
            relief='flat', bd=0,
            command=self.close_assistant,
            width=2, height=1
        )
        self.close_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Zone de contenu
        self.content_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statut système
        self.status_label = tk.Label(
            self.content_frame,
            text="📊 Analyse en cours...",
            bg='#1e1e1e', fg='#00ff88',
            font=('SF Pro Display', 9),
            justify=tk.LEFT, anchor='w'
        )
        self.status_label.pack(fill=tk.X, pady=(0, 5))
        
        # Métriques système
        self.metrics_label = tk.Label(
            self.content_frame,
            text="",
            bg='#1e1e1e', fg='#cccccc',
            font=('SF Mono', 8),
            justify=tk.LEFT, anchor='w'
        )
        self.metrics_label.pack(fill=tk.X, pady=(0, 5))
        
        # Barre d'actions
        self.actions_frame = tk.Frame(self.content_frame, bg='#1e1e1e')
        self.actions_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Bouton nettoyage rapide
        self.quick_clean_btn = tk.Button(
            self.actions_frame,
            text="🧹 Nettoyage",
            bg='#3498db', fg='white',
            font=('SF Pro Display', 8, 'bold'),
            relief='flat', bd=0,
            command=self.quick_clean,
            height=1
        )
        self.quick_clean_btn.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Bouton optimisation
        self.optimize_btn = tk.Button(
            self.actions_frame,
            text="⚡ Optimiser",
            bg='#27ae60', fg='white',
            font=('SF Pro Display', 8, 'bold'),
            relief='flat', bd=0,
            command=self.quick_optimize,
            height=1
        )
        self.optimize_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Rendre la fenêtre déplaçable
        self.make_draggable()
        
        # Démarrer mise à jour automatique
        self.start_monitoring()
    
    def make_draggable(self):
        """Rend la fenêtre déplaçable"""
        def start_move(event):
            self.root.x = event.x
            self.root.y = event.y
        
        def do_move(event):
            x = (event.x_root - self.root.x)
            y = (event.y_root - self.root.y)
            self.root.geometry(f"+{x}+{y}")
        
        self.header_frame.bind('<Button-1>', start_move)
        self.header_frame.bind('<B1-Motion>', do_move)
        self.title_label.bind('<Button-1>', start_move)
        self.title_label.bind('<B1-Motion>', do_move)
    
    def toggle_visibility(self):
        """Basculer entre minimisé/restauré"""
        if self.is_visible:
            # Minimiser (montrer seulement header)
            self.content_frame.pack_forget()
            self.root.geometry("320x35+1000+50")
            self.toggle_btn.config(text="□")
            self.is_visible = False
        else:
            # Restaurer
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.root.geometry("320x180+1000+50")
            self.toggle_btn.config(text="−")
            self.is_visible = True
    
    def close_assistant(self):
        """Fermer l'assistant"""
        self.root.quit()
        self.root.destroy()
    
    def update_metrics(self):
        """Met à jour les métriques système"""
        try:
            # Récupérer métriques via outils système
            # Disque via df
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            disk_percent = 0
            disk_free_gb = 0
            
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        disk_percent = float(fields[4].replace('%', ''))
                        disk_free = fields[3]
                        # Extraire les GB de "123Gi" ou "45G"
                        disk_free_gb = float(''.join(filter(str.isdigit, disk_free)))
            
            # Mémoire via vm_stat
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            memory_percent = 0
            memory_free_mb = 0
            
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\n')
                free_pages = 0
                active_pages = 0
                page_size = 4096  # 4KB par page
                
                for line in lines:
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                total_pages = free_pages + active_pages
                if total_pages > 0:
                    memory_percent = (active_pages / total_pages) * 100
                    memory_free_mb = (free_pages * page_size) // (1024 * 1024)
            
            # CPU via uptime
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            cpu_percent = 0
            
            if uptime_result.returncode == 0:
                output = uptime_result.stdout
                if 'load averages:' in output:
                    load_avg_str = output.split('load averages:')[-1].strip().split()[0]
                    # Gérer format français avec virgule
                    load_avg_str = load_avg_str.replace(',', '.')
                    cpu_percent = min(float(load_avg_str) * 25, 100)  # Approximation
            
            # Statut général
            if disk_percent > 85 or memory_percent > 80:
                status_text = "⚠️  Attention requise"
                status_color = '#ff6b6b'
            elif disk_percent > 70 or memory_percent > 60:
                status_text = "💛 Surveillance active"
                status_color = '#ffa726'
            else:
                status_text = "✅ Système optimal"
                status_color = '#00ff88'
            
            self.status_label.config(text=status_text, fg=status_color)
            
            # Métriques détaillées
            metrics_text = f"""💾 Disque: {disk_percent:.0f}% ({disk_free_gb:.0f}GB libre)
🧠 Mémoire: {memory_percent:.0f}% ({memory_free_mb:.0f}MB libre)
⚡ CPU: {cpu_percent:.0f}%
🕒 {datetime.now().strftime('%H:%M:%S')}"""
            
            self.metrics_label.config(text=metrics_text)
            
            # Coloration boutons selon état
            if disk_percent > 80:
                self.quick_clean_btn.config(bg='#e74c3c')
            else:
                self.quick_clean_btn.config(bg='#3498db')
            
            if memory_percent > 75:
                self.optimize_btn.config(bg='#f39c12')
            else:
                self.optimize_btn.config(bg='#27ae60')
                
        except Exception as e:
            self.status_label.config(text=f"❌ Erreur: {str(e)[:20]}...", fg='#ff6b6b')
    
    def quick_clean(self):
        """Lancement nettoyage rapide"""
        self.status_label.config(text="🧹 Nettoyage en cours...", fg='#ffa726')
        self.root.update()
        
        def cleanup_thread():
            try:
                # Import du guardian pour nettoyage
                import subprocess
                import os
                
                # Nettoyage rapide sécurisé
                subprocess.run(['rm', '-rf', os.path.expanduser('~/.Trash/*')], 
                             shell=True, capture_output=True, timeout=10)
                
                # Mise à jour interface
                self.root.after(0, lambda: self.status_label.config(
                    text="✅ Nettoyage terminé", fg='#00ff88'
                ))
                
                # Retour à la normale après 3 secondes
                self.root.after(3000, self.update_metrics)
                
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"❌ Erreur nettoyage", fg='#ff6b6b'
                ))
        
        threading.Thread(target=cleanup_thread, daemon=True).start()
    
    def quick_optimize(self):
        """Lancement optimisation rapide"""
        self.status_label.config(text="⚡ Optimisation...", fg='#ffa726')
        self.root.update()
        
        def optimize_thread():
            try:
                # Optimisations rapides
                import subprocess
                
                # Purge mémoire
                subprocess.run(['sudo', 'purge'], capture_output=True, timeout=5)
                
                # Mise à jour interface
                self.root.after(0, lambda: self.status_label.config(
                    text="✅ Optimisation OK", fg='#00ff88'
                ))
                
                # Retour à la normale après 3 secondes
                self.root.after(3000, self.update_metrics)
                
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"❌ Erreur optimisation", fg='#ff6b6b'
                ))
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def start_monitoring(self):
        """Démarre la surveillance automatique"""
        def monitor_loop():
            while True:
                try:
                    self.root.after(0, self.update_metrics)
                    time.sleep(5)  # Mise à jour toutes les 5 secondes
                except:
                    break
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def run(self):
        """Lance l'assistant"""
        self.root.mainloop()

def main():
    """Point d'entrée"""
    print("🛡️  Démarrage Guardian Assistant...")
    
    assistant = GuardianAssistant()
    assistant.run()

if __name__ == "__main__":
    main()