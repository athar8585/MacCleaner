#!/usr/bin/env python3
"""
MacCleaner Pro - Daemon de Surveillance Autonome
Service système qui s'exécute en arrière-plan en permanence
"""

import os
import sys
import time
import signal
import json
import threading
import subprocess
from datetime import datetime
import psutil
import sqlite3
from autonomous_cleaner import AutonomousCleanerAgent

class MacCleanerDaemon:
    def __init__(self):
        self.daemon_dir = os.path.expanduser('~/Library/Application Support/MacCleaner Pro')
        self.pid_file = os.path.join(self.daemon_dir, 'daemon.pid')
        self.running = False
        self.agent = None
        
    def start_daemon(self):
        """Démarrer le daemon"""
        # Vérifier si le daemon est déjà en cours
        if self.is_running():
            print("🤖 MacCleaner Pro daemon déjà en cours d'exécution")
            return
            
        print("🚀 Démarrage du daemon MacCleaner Pro...")
        
        # Créer le fichier PID
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
            
        # Configurer les signaux
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Démarrer l'agent autonome
        self.agent = AutonomousCleanerAgent()
        self.running = True
        
        print("✅ Daemon MacCleaner Pro démarré (PID: {})".format(os.getpid()))
        print("📊 Surveillance autonome active")
        
        # Boucle principale du daemon
        try:
            while self.running:
                time.sleep(30)  # Vérifier toutes les 30 secondes
                
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
            
    def stop_daemon(self):
        """Arrêter le daemon"""
        if not self.is_running():
            print("⚠️ Aucun daemon MacCleaner Pro en cours")
            return
            
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                
            os.kill(pid, signal.SIGTERM)
            print("🛑 Daemon MacCleaner Pro arrêté")
            
        except (FileNotFoundError, ProcessLookupError, ValueError):
            print("⚠️ Erreur lors de l'arrêt du daemon")
            self.cleanup()
            
    def restart_daemon(self):
        """Redémarrer le daemon"""
        print("🔄 Redémarrage du daemon MacCleaner Pro...")
        self.stop_daemon()
        time.sleep(2)
        self.start_daemon()
        
    def is_running(self):
        """Vérifier si le daemon est en cours"""
        if not os.path.exists(self.pid_file):
            return False
            
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                
            # Vérifier si le processus existe
            os.kill(pid, 0)
            return True
            
        except (FileNotFoundError, ProcessLookupError, ValueError):
            self.cleanup()
            return False
            
    def signal_handler(self, signum, frame):
        """Gestionnaire de signaux"""
        print(f"\n🛑 Signal {signum} reçu, arrêt du daemon...")
        self.running = False
        
    def cleanup(self):
        """Nettoyage lors de l'arrêt"""
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
            
    def status(self):
        """Afficher le statut du daemon"""
        if self.is_running():
            print("✅ MacCleaner Pro daemon: EN COURS")
            
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                    
                process = psutil.Process(pid)
                print(f"📊 PID: {pid}")
                print(f"💾 Mémoire: {process.memory_info().rss / 1024 / 1024:.1f} MB")
                print(f"⏱️  Uptime: {datetime.now() - datetime.fromtimestamp(process.create_time())}")
                
            except Exception as e:
                print(f"⚠️ Erreur récupération info: {e}")
                
        else:
            print("❌ MacCleaner Pro daemon: ARRÊTÉ")

def create_launchd_plist():
    """Créer le fichier LaunchAgent pour démarrage automatique"""
    plist_dir = os.path.expanduser('~/Library/LaunchAgents')
    plist_file = os.path.join(plist_dir, 'com.maccleanerpro.daemon.plist')
    
    os.makedirs(plist_dir, exist_ok=True)
    
    # Chemin vers le script daemon
    daemon_script = os.path.join(os.path.dirname(__file__), 'daemon.py')
    python_path = sys.executable
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maccleanerpro.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{daemon_script}</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/maccleanerpro.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/maccleanerpro.err</string>
</dict>
</plist>"""
    
    with open(plist_file, 'w') as f:
        f.write(plist_content)
        
    print(f"✅ Fichier LaunchAgent créé: {plist_file}")
    print("🚀 Pour activer le démarrage automatique:")
    print(f"   launchctl load {plist_file}")
    
    return plist_file

def install_daemon():
    """Installer le daemon comme service système"""
    print("🔧 Installation du daemon MacCleaner Pro...")
    
    # Créer le fichier LaunchAgent
    plist_file = create_launchd_plist()
    
    # Charger le service
    try:
        subprocess.run(['launchctl', 'load', plist_file], check=True)
        print("✅ Daemon installé et démarré automatiquement")
        print("🎯 MacCleaner Pro sera maintenant actif au démarrage")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erreur installation: {e}")
        print("💡 Vous pouvez charger manuellement avec:")
        print(f"   launchctl load {plist_file}")

def uninstall_daemon():
    """Désinstaller le daemon"""
    print("🗑️ Désinstallation du daemon MacCleaner Pro...")
    
    plist_file = os.path.expanduser('~/Library/LaunchAgents/com.maccleanerpro.daemon.plist')
    
    # Décharger le service
    try:
        subprocess.run(['launchctl', 'unload', plist_file], check=True)
        print("🛑 Service déchargé")
    except subprocess.CalledProcessError:
        print("⚠️ Service non chargé")
        
    # Supprimer le fichier plist
    if os.path.exists(plist_file):
        os.remove(plist_file)
        print("🗑️ Fichier LaunchAgent supprimé")
        
    print("✅ Daemon désinstallé")

if __name__ == "__main__":
    daemon = MacCleanerDaemon()
    
    if len(sys.argv) < 2:
        print("Usage: python daemon.py {start|stop|restart|status|install|uninstall}")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == 'start':
        daemon.start_daemon()
    elif command == 'stop':
        daemon.stop_daemon()
    elif command == 'restart':
        daemon.restart_daemon()
    elif command == 'status':
        daemon.status()
    elif command == 'install':
        install_daemon()
    elif command == 'uninstall':
        uninstall_daemon()
    else:
        print("❌ Commande inconnue. Utilisez: start|stop|restart|status|install|uninstall")