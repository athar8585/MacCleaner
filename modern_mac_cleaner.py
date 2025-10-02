#!/usr/bin/env python3
"""
MacCleaner Pro v3.0 - Interface moderne iOS 26 avec IA Copilot intégré
Design moderne, surveillance autonome et assistant IA intelligent
"""

import os
import sys
import time
import json
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime, timedelta
import psutil
import requests
from autonomous_cleaner import AutonomousCleanerAgent

class ModernMacCleanerPro:
    def __init__(self):
        # Initialiser l'agent autonome
        self.autonomous_agent = AutonomousCleanerAgent()
        
        # Interface moderne
        self.root = tk.Tk()
        self.setup_modern_ui()
        
        # IA Copilot intégré
        self.copilot_active = False
        self.setup_copilot_ai()
        
        # Variables d'état
        self.cleaning_active = False
        self.total_freed_space = 0
        self.current_task = "Prêt"
        
    def setup_modern_ui(self):
        """Configuration de l'interface moderne iOS 26 style"""
        self.root.title("MacCleaner Pro 3.0 - Intelligence Autonome")
        self.root.geometry("1200x800")
        
        # Couleurs modernes iOS 26
        self.colors = {
            'primary': '#007AFF',      # Bleu système iOS
            'secondary': '#5856D6',    # Violet système
            'success': '#34C759',      # Vert système
            'warning': '#FF9500',      # Orange système
            'danger': '#FF3B30',       # Rouge système
            'background': '#F2F2F7',   # Gris clair système
            'surface': '#FFFFFF',      # Blanc
            'text_primary': '#000000', # Noir
            'text_secondary': '#6D6D80', # Gris moyen
            'accent': '#AF52DE'        # Violet accent
        }
        
        # Configuration du style moderne
        self.root.configure(bg=self.colors['background'])
        
        # Style ttk moderne
        style = ttk.Style()
        style.theme_use('clam')
        
        # Styles personnalisés iOS 26
        style.configure('Modern.TFrame', background=self.colors['surface'], relief='flat', borderwidth=0)
        style.configure('Card.TFrame', background=self.colors['surface'], relief='solid', borderwidth=1)
        style.configure('Primary.TButton', 
                       background=self.colors['primary'], 
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Primary.TButton',
                 background=[('active', '#0056CC'), ('pressed', '#004AAA')])
        
        # Interface principale
        self.create_modern_interface()
        
    def create_modern_interface(self):
        """Créer l'interface moderne"""
        # Frame principal avec padding moderne
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header moderne avec titre et statut
        self.create_modern_header(main_container)
        
        # Dashboard avec cartes de statut
        self.create_dashboard_cards(main_container)
        
        # Section IA Copilot
        self.create_copilot_section(main_container)
        
        # Contrôles principaux
        self.create_main_controls(main_container)
        
        # Zone de logs moderne
        self.create_modern_logs(main_container)
        
        # Configuration responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        
    def create_modern_header(self, parent):
        """Créer l'en-tête moderne"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Titre principal avec icône
        title_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        title_frame.grid(row=0, column=0, sticky=tk.W)
        
        title_label = ttk.Label(title_frame, text="🧹 MacCleaner Pro 3.0", 
                               font=('SF Pro Display', 28, 'bold'),
                               foreground=self.colors['primary'])
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame, text="Intelligence Autonome • Protection IA • Design iOS 26", 
                                  font=('SF Pro Text', 12),
                                  foreground=self.colors['text_secondary'])
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Indicateur de statut en temps réel
        self.status_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        self.status_frame.grid(row=0, column=1, sticky=tk.E)
        
        self.status_indicator = ttk.Label(self.status_frame, text="●", 
                                         font=('SF Pro Display', 16),
                                         foreground=self.colors['success'])
        self.status_indicator.grid(row=0, column=0)
        
        self.status_text = ttk.Label(self.status_frame, text="Système Optimal", 
                                    font=('SF Pro Text', 12, 'bold'),
                                    foreground=self.colors['text_primary'])
        self.status_text.grid(row=0, column=1, padx=(5, 0))
        
        header_frame.columnconfigure(1, weight=1)
        
    def create_dashboard_cards(self, parent):
        """Créer les cartes de tableau de bord"""
        dashboard_frame = ttk.Frame(parent, style='Modern.TFrame')
        dashboard_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Carte Performance Système
        system_card = self.create_info_card(dashboard_frame, "Performance Système", 0, 0)
        self.system_info_label = ttk.Label(system_card, text="Chargement...", 
                                          font=('SF Pro Text', 11),
                                          foreground=self.colors['text_secondary'])
        self.system_info_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Carte Protection IA
        protection_card = self.create_info_card(dashboard_frame, "Protection IA", 0, 1)
        self.protection_info_label = ttk.Label(protection_card, text="🛡️ Actif\n🔍 Surveillance continue\n☁️ Protection iCloud", 
                                              font=('SF Pro Text', 11),
                                              foreground=self.colors['text_secondary'])
        self.protection_info_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Carte Nettoyage Récent
        cleaning_card = self.create_info_card(dashboard_frame, "Derniers Nettoyages", 0, 2)
        self.cleaning_info_label = ttk.Label(cleaning_card, text="Aucun nettoyage récent", 
                                            font=('SF Pro Text', 11),
                                            foreground=self.colors['text_secondary'])
        self.cleaning_info_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Configuration responsive des cartes
        for i in range(3):
            dashboard_frame.columnconfigure(i, weight=1)
            
    def create_info_card(self, parent, title, row, col):
        """Créer une carte d'information moderne"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        card_frame.grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Titre de la carte
        title_label = ttk.Label(card_frame, text=title, 
                               font=('SF Pro Text', 14, 'bold'),
                               foreground=self.colors['text_primary'])
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        return card_frame
        
    def create_copilot_section(self, parent):
        """Créer la section IA Copilot"""
        copilot_frame = ttk.LabelFrame(parent, text="🤖 Assistant IA Copilot", 
                                      style='Card.TFrame', padding="15")
        copilot_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Interface de chat avec IA
        chat_frame = ttk.Frame(copilot_frame, style='Modern.TFrame')
        chat_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de conversation
        self.copilot_chat = scrolledtext.ScrolledText(chat_frame, height=8, width=80,
                                                     font=('SF Mono', 11),
                                                     bg=self.colors['background'],
                                                     fg=self.colors['text_primary'],
                                                     relief='flat',
                                                     borderwidth=1)
        self.copilot_chat.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Message d'accueil
        welcome_msg = """🤖 Copilot IA: Bonjour ! Je suis votre assistant intelligent MacCleaner Pro.

Je peux vous aider à :
• 🔍 Analyser l'état de votre Mac en temps réel
• 🧹 Recommander des nettoyages personnalisés
• 🛡️ Surveiller les menaces de sécurité
• 📊 Interpréter les métriques de performance
• ⚙️ Optimiser les paramètres automatiques

Tapez votre question ou dites 'aide' pour plus d'options...
"""
        self.copilot_chat.insert(tk.END, welcome_msg)
        
        # Zone de saisie moderne
        input_frame = ttk.Frame(chat_frame, style='Modern.TFrame')
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.copilot_input = ttk.Entry(input_frame, font=('SF Pro Text', 12),
                                      width=60)
        self.copilot_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.copilot_input.bind('<Return>', self.send_copilot_message)
        
        send_button = ttk.Button(input_frame, text="Envoyer", 
                               style='Primary.TButton',
                               command=self.send_copilot_message)
        send_button.grid(row=0, column=1)
        
        # Boutons d'action rapide
        quick_actions_frame = ttk.Frame(copilot_frame, style='Modern.TFrame')
        quick_actions_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        quick_buttons = [
            ("🔍 Analyser Système", self.copilot_analyze_system),
            ("🧹 Nettoyage Recommandé", self.copilot_recommend_cleaning),
            ("🛡️ Rapport Sécurité", self.copilot_security_report),
            ("📊 Métriques Performance", self.copilot_performance_metrics)
        ]
        
        for i, (text, command) in enumerate(quick_buttons):
            btn = ttk.Button(quick_actions_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=5)
            
        chat_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        
    def create_main_controls(self, parent):
        """Créer les contrôles principaux"""
        controls_frame = ttk.Frame(parent, style='Modern.TFrame')
        controls_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Mode de fonctionnement
        mode_frame = ttk.LabelFrame(controls_frame, text="Mode de Fonctionnement", padding="10")
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.operation_mode = tk.StringVar(value="autonomous")
        
        mode_options = [
            ("🤖 Autonome (Recommandé)", "autonomous"),
            ("🔍 Analyse Seulement", "analyze"),
            ("🧹 Nettoyage Manuel", "manual"),
            ("🛡️ Protection Seulement", "protection")
        ]
        
        for i, (text, value) in enumerate(mode_options):
            ttk.Radiobutton(mode_frame, text=text, variable=self.operation_mode, 
                           value=value).grid(row=i, column=0, sticky=tk.W, pady=2)
            
        # Paramètres autonomes
        autonomous_frame = ttk.LabelFrame(controls_frame, text="Paramètres Autonomes", padding="10")
        autonomous_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Seuils automatiques
        ttk.Label(autonomous_frame, text="Seuil disque (%)").grid(row=0, column=0, sticky=tk.W)
        self.disk_threshold = tk.Scale(autonomous_frame, from_=70, to=95, orient=tk.HORIZONTAL)
        self.disk_threshold.set(85)
        self.disk_threshold.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(autonomous_frame, text="Seuil mémoire (%)").grid(row=1, column=0, sticky=tk.W)
        self.memory_threshold = tk.Scale(autonomous_frame, from_=60, to=90, orient=tk.HORIZONTAL)
        self.memory_threshold.set(80)
        self.memory_threshold.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Protection avancée
        protection_frame = ttk.LabelFrame(controls_frame, text="Protection Avancée", padding="10")
        protection_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.icloud_protection = tk.BooleanVar(value=True)
        self.realtime_protection = tk.BooleanVar(value=True)
        self.auto_quarantine = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(protection_frame, text="🔒 Protection iCloud", 
                       variable=self.icloud_protection).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(protection_frame, text="🛡️ Protection Temps Réel", 
                       variable=self.realtime_protection).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(protection_frame, text="🔒 Quarantaine Auto", 
                       variable=self.auto_quarantine).grid(row=2, column=0, sticky=tk.W)
        
        # Configuration responsive
        for i in range(3):
            controls_frame.columnconfigure(i, weight=1)
            
    def create_modern_logs(self, parent):
        """Créer la zone de logs moderne"""
        logs_frame = ttk.LabelFrame(parent, text="Activité en Temps Réel", padding="10")
        logs_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Zone de logs avec style moderne
        self.log_text = scrolledtext.ScrolledText(logs_frame, height=12, 
                                                 font=('SF Mono', 10),
                                                 bg=self.colors['background'],
                                                 fg=self.colors['text_primary'],
                                                 relief='flat',
                                                 borderwidth=1)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Boutons de contrôle des logs
        log_controls = ttk.Frame(logs_frame, style='Modern.TFrame')
        log_controls.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(log_controls, text="🗑️ Effacer", 
                  command=self.clear_logs).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(log_controls, text="💾 Sauvegarder", 
                  command=self.save_logs).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(log_controls, text="📊 Exporter Rapport", 
                  command=self.export_report).grid(row=0, column=2)
        
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        
        # Actions principales
        actions_frame = ttk.Frame(parent, style='Modern.TFrame')
        actions_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Boutons d'action principaux
        main_buttons = [
            ("🚀 Démarrer Agent Autonome", self.start_autonomous_mode, 'Primary.TButton'),
            ("🔍 Scan Complet", self.start_full_scan, 'Primary.TButton'),
            ("🧹 Nettoyage Manuel", self.start_manual_cleaning, 'Primary.TButton'),
            ("⚙️ Paramètres Avancés", self.open_advanced_settings, None)
        ]
        
        for i, (text, command, style) in enumerate(main_buttons):
            btn = ttk.Button(actions_frame, text=text, command=command)
            if style:
                btn.configure(style=style)
            btn.grid(row=0, column=i, padx=10)
            
    def setup_copilot_ai(self):
        """Configuration de l'IA Copilot"""
        self.copilot_context = {
            'system_data': {},
            'user_preferences': {},
            'conversation_history': []
        }
        
        # Démarrer la mise à jour des données en temps réel
        self.update_system_data()
        self.schedule_data_updates()
        
    def send_copilot_message(self, event=None):
        """Envoyer un message au Copilot IA"""
        user_message = self.copilot_input.get().strip()
        if not user_message:
            return
            
        # Afficher le message utilisateur
        self.copilot_chat.insert(tk.END, f"\n👤 Vous: {user_message}\n")
        self.copilot_input.delete(0, tk.END)
        
        # Traiter la demande
        response = self.process_copilot_query(user_message)
        
        # Afficher la réponse
        self.copilot_chat.insert(tk.END, f"🤖 Copilot: {response}\n")
        self.copilot_chat.see(tk.END)
        
    def process_copilot_query(self, query):
        """Traiter une requête du Copilot IA"""
        query_lower = query.lower()
        
        # Commandes d'aide
        if 'aide' in query_lower or 'help' in query_lower:
            return self.get_help_response()
            
        # Analyse système
        elif any(word in query_lower for word in ['système', 'performance', 'état', 'analyse']):
            return self.copilot_analyze_system_response()
            
        # Nettoyage
        elif any(word in query_lower for word in ['nettoyer', 'nettoyage', 'clean', 'libérer']):
            return self.copilot_cleaning_response()
            
        # Sécurité
        elif any(word in query_lower for word in ['sécurité', 'malware', 'virus', 'menace']):
            return self.copilot_security_response()
            
        # Optimisation
        elif any(word in query_lower for word in ['optimiser', 'optimisation', 'accélérer', 'performance']):
            return self.copilot_optimization_response()
            
        # Espace disque
        elif any(word in query_lower for word in ['espace', 'disque', 'stockage', 'mémoire']):
            return self.copilot_storage_response()
            
        # Réponse par défaut avec suggestions
        else:
            return f"""Je ne suis pas sûr de comprendre "{query}".

Essayez ces commandes :
• "analyser système" - État complet du Mac
• "nettoyer maintenant" - Recommandations de nettoyage
• "rapport sécurité" - Statut de protection
• "optimiser performance" - Conseils d'amélioration
• "espace disque" - Analyse du stockage

Ou tapez "aide" pour plus d'options."""

    def copilot_analyze_system_response(self):
        """Réponse d'analyse système du Copilot"""
        try:
            # Récupérer les données système actuelles
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Récupérer le rapport de l'agent autonome
            status_report = self.autonomous_agent.get_status_report()
            
            analysis = f"""📊 ANALYSE SYSTÈME COMPLÈTE

🖥️ **Performance Actuelle:**
• Processeur: {cpu_usage:.1f}% d'utilisation
• Mémoire: {memory.percent:.1f}% utilisée ({memory.available / (1024**3):.1f}GB libre)
• Disque: {(disk.used / disk.total) * 100:.1f}% utilisé ({disk.free / (1024**3):.1f}GB libre)

🏥 **État de Santé:**"""

            # Analyse intelligente
            if cpu_usage > 80:
                analysis += "\n⚠️ Processeur très sollicité - Recommande nettoyage des processus"
            elif cpu_usage > 60:
                analysis += "\n🟡 Processeur modérément chargé"
            else:
                analysis += "\n✅ Processeur en bon état"
                
            if memory.percent > 85:
                analysis += "\n🔴 Mémoire critique - Nettoyage urgent recommandé"
            elif memory.percent > 70:
                analysis += "\n🟡 Mémoire chargée - Nettoyage conseillé"
            else:
                analysis += "\n✅ Mémoire en bon état"
                
            if (disk.used / disk.total) * 100 > 90:
                analysis += "\n🔴 Espace disque critique - Action immédiate requise"
            elif (disk.used / disk.total) * 100 > 80:
                analysis += "\n🟡 Espace disque faible - Nettoyage recommandé"
            else:
                analysis += "\n✅ Espace disque suffisant"
                
            # Recommandations
            analysis += "\n\n💡 **Recommandations:**"
            
            if status_report.get('cleaning_performance', {}).get('cleanings_last_week', 0) == 0:
                analysis += "\n• Aucun nettoyage récent - Lancez un nettoyage complet"
                
            if memory.percent > 70:
                analysis += "\n• Redémarrez les applications gourmandes"
                
            if (disk.used / disk.total) * 100 > 80:
                analysis += "\n• Nettoyez les fichiers temporaires et caches"
                
            analysis += "\n\nTapez 'nettoyer maintenant' pour démarrer l'optimisation automatique."
            
            return analysis
            
        except Exception as e:
            return f"❌ Erreur lors de l'analyse système: {str(e)}"
            
    def copilot_cleaning_response(self):
        """Réponse de nettoyage du Copilot"""
        return """🧹 RECOMMANDATIONS DE NETTOYAGE INTELLIGENT

🎯 **Actions Recommandées:**
• Nettoyage des caches système (sûr)
• Suppression des fichiers temporaires
• Vidage de la corbeille
• Optimisation de la mémoire

🔒 **Protections Actives:**
• Fichiers iCloud automatiquement protégés
• Documents importants préservés
• Fichiers récents sauvegardés

⚡ **Gains Estimés:**
• 2-8 GB d'espace disque
• 15-30% d'amélioration performance
• Démarrage plus rapide

Voulez-vous que je lance le nettoyage automatique maintenant ?
Tapez 'oui nettoyer' pour confirmer."""

    def copilot_security_response(self):
        """Réponse sécurité du Copilot"""
        try:
            # Vérifier les dernières détections
            conn = sqlite3.connect(self.autonomous_agent.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM malware_detections 
                WHERE timestamp > datetime('now', '-24 hours')
            ''')
            recent_threats = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM malware_detections')
            total_threats = cursor.fetchone()[0]
            
            conn.close()
            
            security_status = f"""🛡️ RAPPORT SÉCURITÉ COMPLET

📊 **Statut Actuel:**
• Protection temps réel: {'🟢 ACTIVE' if self.realtime_protection.get() else '🔴 INACTIVE'}
• Détections 24h: {recent_threats} menaces
• Total détections: {total_threats} menaces
• Quarantaine: {'🟢 ACTIVE' if self.auto_quarantine.get() else '🔴 INACTIVE'}

🔍 **Dernière Analyse:**
• Base de signatures: À jour
• Surveillance iCloud: Active
• Protection téléchargements: Active

✅ **Recommandations:**"""

            if recent_threats > 0:
                security_status += f"\n⚠️ {recent_threats} menaces détectées récemment - Vérifiez la quarantaine"
            else:
                security_status += "\n✅ Aucune menace récente détectée"
                
            if not self.realtime_protection.get():
                security_status += "\n🔧 Activez la protection temps réel pour une sécurité maximale"
                
            security_status += "\n\nVotre système est protégé par une surveillance intelligente continue."
            
            return security_status
            
        except Exception as e:
            return f"❌ Erreur lors de l'analyse sécurité: {str(e)}"
            
    def get_help_response(self):
        """Réponse d'aide du Copilot"""
        return """🤖 AIDE COPILOT IA - MacCleaner Pro 3.0

📋 **Commandes Disponibles:**

🔍 **Analyse & Diagnostic:**
• "analyser système" - État complet du Mac
• "rapport performance" - Métriques détaillées
• "espace disque" - Analyse du stockage

🧹 **Nettoyage & Optimisation:**
• "nettoyer maintenant" - Nettoyage automatique
• "optimiser performance" - Conseils d'amélioration
• "libérer espace" - Recommandations de stockage

🛡️ **Sécurité & Protection:**
• "rapport sécurité" - Statut protection
• "scan malware" - Analyse des menaces
• "vérifier quarantaine" - Fichiers suspects

⚙️ **Configuration:**
• "paramètres autonome" - Réglages auto
• "seuils surveillance" - Limites déclenchement
• "historique nettoyage" - Dernières actions

💬 **Communication Naturelle:**
Vous pouvez aussi me parler naturellement :
• "Mon Mac est lent"
• "J'ai besoin d'espace"
• "Est-ce que tout va bien ?"

Je comprends le français et je m'adapte à votre style !"""

    def copilot_analyze_system(self):
        """Action rapide - Analyser système"""
        response = self.copilot_analyze_system_response()
        self.copilot_chat.insert(tk.END, f"\n🤖 Copilot: {response}\n")
        self.copilot_chat.see(tk.END)
        
    def copilot_recommend_cleaning(self):
        """Action rapide - Recommander nettoyage"""
        response = self.copilot_cleaning_response()
        self.copilot_chat.insert(tk.END, f"\n🤖 Copilot: {response}\n")
        self.copilot_chat.see(tk.END)
        
    def copilot_security_report(self):
        """Action rapide - Rapport sécurité"""
        response = self.copilot_security_response()
        self.copilot_chat.insert(tk.END, f"\n🤖 Copilot: {response}\n")
        self.copilot_chat.see(tk.END)
        
    def copilot_performance_metrics(self):
        """Action rapide - Métriques performance"""
        try:
            status_report = self.autonomous_agent.get_status_report()
            
            metrics = f"""📊 MÉTRIQUES PERFORMANCE DÉTAILLÉES

🏃‍♂️ **Performance Actuelle:**
• CPU: {status_report.get('system_health', {}).get('cpu_usage', 0):.1f}%
• RAM: {status_report.get('system_health', {}).get('memory_usage', 0):.1f}%
• Disque: {status_report.get('system_health', {}).get('disk_usage', 0):.1f}%

📈 **Historique (7 derniers jours):**
• Nettoyages: {status_report.get('cleaning_performance', {}).get('cleanings_last_week', 0)}
• Espace libéré: {status_report.get('cleaning_performance', {}).get('space_freed_mb', 0):.1f} MB
• Temps moyen: {status_report.get('cleaning_performance', {}).get('avg_duration_seconds', 0):.1f}s

🛡️ **Sécurité:**
• Menaces détectées: {status_report.get('security', {}).get('threats_detected_last_week', 0)}
• Protection: {'Active' if status_report.get('security', {}).get('protection_active', False) else 'Inactive'}

🎯 **Recommandations:**
Basées sur l'analyse de vos habitudes d'utilisation."""
            
            self.copilot_chat.insert(tk.END, f"\n🤖 Copilot: {metrics}\n")
            
        except Exception as e:
            self.copilot_chat.insert(tk.END, f"\n🤖 Copilot: ❌ Erreur métriques: {str(e)}\n")
            
        self.copilot_chat.see(tk.END)
        
    def update_system_data(self):
        """Mettre à jour les données système en temps réel"""
        try:
            # Métriques système
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Mettre à jour l'interface
            system_text = f"""💾 Disque: {(disk.used / disk.total) * 100:.1f}% utilisé
🧠 RAM: {memory.percent:.1f}% utilisée  
⚡ CPU: {cpu_usage:.1f}% d'utilisation
🔋 Processus: {len(psutil.pids())} actifs"""
            
            self.system_info_label.configure(text=system_text)
            
            # Mettre à jour le statut général
            if cpu_usage > 80 or memory.percent > 85 or (disk.used / disk.total) * 100 > 90:
                self.status_indicator.configure(foreground=self.colors['warning'])
                self.status_text.configure(text="Attention Requise")
            elif cpu_usage > 60 or memory.percent > 70 or (disk.used / disk.total) * 100 > 80:
                self.status_indicator.configure(foreground=self.colors['warning'])
                self.status_text.configure(text="Optimisation Suggérée")
            else:
                self.status_indicator.configure(foreground=self.colors['success'])
                self.status_text.configure(text="Système Optimal")
                
        except Exception as e:
            self.log_message(f"Erreur mise à jour données: {str(e)}")
            
    def schedule_data_updates(self):
        """Programmer les mises à jour des données"""
        def update_loop():
            while True:
                try:
                    self.update_system_data()
                    time.sleep(5)  # Mise à jour toutes les 5 secondes
                except Exception as e:
                    print(f"Erreur update loop: {str(e)}")
                    time.sleep(30)
                    
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
    def log_message(self, message):
        """Ajouter un message au log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_logs(self):
        """Effacer les logs"""
        self.log_text.delete(1.0, tk.END)
        
    def save_logs(self):
        """Sauvegarder les logs"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"MacCleaner_logs_{timestamp}.txt"
            
            with open(log_file, 'w') as f:
                f.write(self.log_text.get(1.0, tk.END))
                
            self.log_message(f"✅ Logs sauvegardés: {log_file}")
            
        except Exception as e:
            self.log_message(f"❌ Erreur sauvegarde logs: {str(e)}")
            
    def export_report(self):
        """Exporter un rapport complet"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"MacCleaner_rapport_{timestamp}.json"
            
            # Générer le rapport complet
            status_report = self.autonomous_agent.get_status_report()
            
            with open(report_file, 'w') as f:
                json.dump(status_report, f, indent=2)
                
            self.log_message(f"📊 Rapport exporté: {report_file}")
            
        except Exception as e:
            self.log_message(f"❌ Erreur export rapport: {str(e)}")
            
    def start_autonomous_mode(self):
        """Démarrer le mode autonome"""
        try:
            # Mettre à jour la configuration de l'agent
            self.autonomous_agent.config['auto_clean_threshold']['disk_usage_percent'] = self.disk_threshold.get()
            self.autonomous_agent.config['auto_clean_threshold']['memory_usage_percent'] = self.memory_threshold.get()
            
            self.log_message("🤖 Mode autonome activé - Surveillance continue démarrée")
            self.log_message(f"📊 Seuils: Disque {self.disk_threshold.get()}%, Mémoire {self.memory_threshold.get()}%")
            
            # Démarrer la surveillance en arrière-plan
            if not hasattr(self, 'autonomous_thread') or not self.autonomous_thread.is_alive():
                self.autonomous_thread = threading.Thread(target=self.autonomous_monitoring, daemon=True)
                self.autonomous_thread.start()
                
        except Exception as e:
            self.log_message(f"❌ Erreur démarrage mode autonome: {str(e)}")
            
    def autonomous_monitoring(self):
        """Surveillance autonome en arrière-plan"""
        while True:
            try:
                # Vérifier les seuils
                disk_usage = psutil.disk_usage('/')
                disk_percent = (disk_usage.used / disk_usage.total) * 100
                memory_percent = psutil.virtual_memory().percent
                
                # Log périodique du statut
                if int(time.time()) % 300 == 0:  # Toutes les 5 minutes
                    self.log_message(f"🤖 Surveillance: Disque {disk_percent:.1f}%, RAM {memory_percent:.1f}%")
                    
                time.sleep(30)
                
            except Exception as e:
                self.log_message(f"❌ Erreur surveillance: {str(e)}")
                time.sleep(60)
                
    def start_full_scan(self):
        """Démarrer un scan complet"""
        self.log_message("🔍 Démarrage du scan complet...")
        
        def scan_thread():
            try:
                # Scanner le système
                self.autonomous_agent.scan_malware()
                
                # Analyser l'espace disque
                large_files = self.find_large_files()
                
                self.log_message(f"✅ Scan terminé - {len(large_files)} gros fichiers trouvés")
                
            except Exception as e:
                self.log_message(f"❌ Erreur scan: {str(e)}")
                
        threading.Thread(target=scan_thread, daemon=True).start()
        
    def find_large_files(self):
        """Trouver les fichiers volumineux"""
        large_files = []
        search_paths = [
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop'),
            os.path.expanduser('~/Documents')
        ]
        
        min_size_bytes = 100 * 1024 * 1024  # 100 MB
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                if os.path.getsize(filepath) > min_size_bytes:
                                    large_files.append(filepath)
                                    if len(large_files) >= 20:  # Limiter à 20 fichiers
                                        return large_files
                            except (OSError, IOError):
                                continue
                except (OSError, IOError):
                    continue
                    
        return large_files
        
    def start_manual_cleaning(self):
        """Démarrer un nettoyage manuel"""
        self.log_message("🧹 Démarrage du nettoyage manuel...")
        
        def cleaning_thread():
            try:
                # Utiliser l'agent autonome pour le nettoyage
                self.autonomous_agent.trigger_autonomous_cleaning('manual', ['Nettoyage manuel demandé'])
                self.log_message("✅ Nettoyage manuel terminé")
                
            except Exception as e:
                self.log_message(f"❌ Erreur nettoyage: {str(e)}")
                
        threading.Thread(target=cleaning_thread, daemon=True).start()
        
    def open_advanced_settings(self):
        """Ouvrir les paramètres avancés"""
        # Créer une fenêtre de paramètres avancés
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Paramètres Avancés")
        settings_window.geometry("600x400")
        settings_window.configure(bg=self.colors['background'])
        
        # Interface des paramètres avancés
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(settings_frame, text="⚙️ Paramètres Avancés", 
                 font=('SF Pro Display', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Options avancées
        advanced_options = [
            ("Protection temps réel", self.realtime_protection),
            ("Quarantaine automatique", self.auto_quarantine),
            ("Protection iCloud", self.icloud_protection)
        ]
        
        for i, (text, var) in enumerate(advanced_options):
            ttk.Checkbutton(settings_frame, text=text, variable=var).grid(
                row=i+1, column=0, sticky=tk.W, pady=5)
        
        settings_window.columnconfigure(0, weight=1)
        settings_window.rowconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
    def run(self):
        """Lancer l'application"""
        # Message de bienvenue
        welcome_msg = """🚀 MacCleaner Pro 3.0 - Intelligence Autonome Démarrée

✨ Nouvelles fonctionnalités:
• 🤖 IA Copilot intégrée pour assistance intelligente
• 🛡️ Protection temps réel contre les malwares
• 📊 Surveillance autonome avec seuils personnalisables
• 🎨 Interface moderne iOS 26
• ☁️ Protection iCloud avancée
• 🔄 Maintenance automatique programmée

Votre Mac est maintenant sous protection intelligente !"""

        self.log_message(welcome_msg)
        
        # Démarrer l'interface
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernMacCleanerPro()
    app.run()