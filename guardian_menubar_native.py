#!/usr/bin/env python3
"""
MacCleaner Guardian - INDICATEUR BARRE DE MENU NATIF
Version utilisant les APIs natives macOS sans dépendances externes
"""

import subprocess
import threading
import time
import json
import os
from datetime import datetime
from pathlib import Path

class MacCleanerMenuBarNative:
    """Indicateur barre de menu natif pour MacCleaner Guardian"""
    
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.log_file = Path.home() / '.maccleaner_guardian.log'
        self.status_file = Path.home() / '.maccleaner_status.json'
        self.monitoring_active = True
        self.current_icon = "🛡️"
        
        # Configuration par défaut
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 30,
            'auto_cleanup_threshold': 85,
            'memory_threshold': 80,
            'notifications_enabled': True,
            'last_cleanup': None
        }
        
        self.load_config()
        self.create_status_bar_app()
        self.start_monitoring()
    
    def load_config(self):
        """Charge la configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except:
            pass
    
    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def update_status_file(self, status_data):
        """Met à jour le fichier de statut pour l'app SwiftUI"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
        except:
            pass
    
    def create_status_bar_app(self):
        """Crée l'application barre de statut avec SwiftUI"""
        
        # Code Swift pour l'application barre de statut
        swift_code = '''
import SwiftUI
import AppKit
import Foundation

@main
struct MacCleanerMenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate, ObservableObject {
    private var statusItem: NSStatusItem!
    private var timer: Timer?
    @Published var systemStatus = SystemStatus()
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusBar()
        startMonitoring()
    }
    
    private func setupStatusBar() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = "🛡️"
            button.target = self
            button.action = #selector(statusBarButtonClicked)
        }
        
        updateMenu()
    }
    
    @objc private func statusBarButtonClicked() {
        // Le menu s'affiche automatiquement
    }
    
    private func updateMenu() {
        let menu = NSMenu()
        
        // Status principal
        let statusItem = NSMenuItem(title: systemStatus.statusText, action: nil, keyEquivalent: "")
        statusItem.isEnabled = false
        menu.addItem(statusItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Métriques
        let diskItem = NSMenuItem(title: "💾 Disque: \\(systemStatus.diskPercent)% (\\(systemStatus.diskFree) libre)", action: nil, keyEquivalent: "")
        diskItem.isEnabled = false
        menu.addItem(diskItem)
        
        let memoryItem = NSMenuItem(title: "🧠 Mémoire: \\(systemStatus.memoryPercent)% (\\(systemStatus.memoryFreeMB)MB libre)", action: nil, keyEquivalent: "")
        memoryItem.isEnabled = false
        menu.addItem(memoryItem)
        
        let cpuItem = NSMenuItem(title: "⚡ CPU: \\(systemStatus.cpuPercent)%", action: nil, keyEquivalent: "")
        cpuItem.isEnabled = false
        menu.addItem(cpuItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Actions
        let cleanupItem = NSMenuItem(title: "🧹 Nettoyage Rapide", action: #selector(quickCleanup), keyEquivalent: "")
        cleanupItem.target = self
        menu.addItem(cleanupItem)
        
        let optimizeItem = NSMenuItem(title: "⚡ Optimisation", action: #selector(quickOptimization), keyEquivalent: "")
        optimizeItem.target = self
        menu.addItem(optimizeItem)
        
        let refreshItem = NSMenuItem(title: "🔄 Actualiser", action: #selector(forceUpdate), keyEquivalent: "")
        refreshItem.target = self
        menu.addItem(refreshItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Configuration
        let autoCleanupTitle = systemStatus.autoCleanupEnabled ? "✅ Nettoyage Automatique" : "❌ Nettoyage Automatique"
        let autoCleanupItem = NSMenuItem(title: autoCleanupTitle, action: #selector(toggleAutoCleanup), keyEquivalent: "")
        autoCleanupItem.target = self
        menu.addItem(autoCleanupItem)
        
        let notificationsTitle = systemStatus.notificationsEnabled ? "🔔 Notifications" : "🔕 Notifications"
        let notificationsItem = NSMenuItem(title: notificationsTitle, action: #selector(toggleNotifications), keyEquivalent: "")
        notificationsItem.target = self
        menu.addItem(notificationsItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Autres options
        let fullPanelItem = NSMenuItem(title: "📊 Ouvrir Panneau Complet", action: #selector(openFullPanel), keyEquivalent: "")
        fullPanelItem.target = self
        menu.addItem(fullPanelItem)
        
        let viewLogsItem = NSMenuItem(title: "📝 Voir Logs", action: #selector(viewLogs), keyEquivalent: "")
        viewLogsItem.target = self
        menu.addItem(viewLogsItem)
        
        menu.addItem(NSMenuItem.separator())
        
        let quitItem = NSMenuItem(title: "❌ Quitter Guardian", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    private func startMonitoring() {
        timer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { _ in
            self.updateSystemStatus()
        }
        updateSystemStatus() // Initial update
    }
    
    private func updateSystemStatus() {
        // Lire le fichier de statut mis à jour par Python
        if let data = try? Data(contentsOf: URL(fileURLWithPath: NSHomeDirectory() + "/.maccleaner_status.json")),
           let status = try? JSONDecoder().decode(SystemStatus.self, from: data) {
            DispatchQueue.main.async {
                self.systemStatus = status
                self.updateStatusBarIcon()
                self.updateMenu()
            }
        }
    }
    
    private func updateStatusBarIcon() {
        if let button = statusItem.button {
            if systemStatus.diskPercent > 85 || systemStatus.memoryPercent > 80 {
                button.title = "⚠️"
            } else if systemStatus.diskPercent > 70 || systemStatus.memoryPercent > 65 {
                button.title = "🟡"
            } else {
                button.title = "🛡️"
            }
        }
    }
    
    @objc private func quickCleanup() {
        executeCommand("python3", args: ["guardian_menubar.py", "--cleanup"])
    }
    
    @objc private func quickOptimization() {
        executeCommand("python3", args: ["guardian_menubar.py", "--optimize"])
    }
    
    @objc private func forceUpdate() {
        updateSystemStatus()
    }
    
    @objc private func toggleAutoCleanup() {
        executeCommand("python3", args: ["guardian_menubar.py", "--toggle-cleanup"])
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.updateSystemStatus()
        }
    }
    
    @objc private func toggleNotifications() {
        executeCommand("python3", args: ["guardian_menubar.py", "--toggle-notifications"])
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.updateSystemStatus()
        }
    }
    
    @objc private func openFullPanel() {
        executeCommand("python3", args: ["maccleaner_guardian.py"])
    }
    
    @objc private func viewLogs() {
        executeCommand("open", args: ["-a", "TextEdit", NSHomeDirectory() + "/.maccleaner_guardian.log"])
    }
    
    private func executeCommand(_ command: String, args: [String] = []) {
        let process = Process()
        process.launchPath = "/usr/bin/env"
        process.arguments = [command] + args
        try? process.run()
    }
}

struct SystemStatus: Codable {
    var statusText: String = "📊 Analyse en cours..."
    var diskPercent: Int = 0
    var diskFree: String = "--"
    var memoryPercent: Int = 0
    var memoryFreeMB: Int = 0
    var cpuPercent: Int = 0
    var autoCleanupEnabled: Bool = true
    var notificationsEnabled: Bool = true
    var lastUpdate: String = ""
}
'''
        
        # Sauvegarder le code Swift
        swift_file = Path('/Users/loicdeloison/Desktop/MacCleaner/MenuBarApp.swift')
        with open(swift_file, 'w') as f:
            f.write(swift_code)
        
        print("📁 Code Swift créé pour l'application barre de menu")
    
    def get_system_metrics(self):
        """Récupère les métriques système"""
        try:
            metrics = {}
            
            # Disque via df
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        metrics['disk_percent'] = int(float(fields[4].replace('%', '')))
                        metrics['disk_free'] = fields[3]
            
            # Mémoire via vm_stat
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\\n')
                free_pages = 0
                active_pages = 0
                
                for line in lines:
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                total_pages = free_pages + active_pages
                if total_pages > 0:
                    metrics['memory_percent'] = int((active_pages / total_pages) * 100)
                    metrics['memory_free_mb'] = int((free_pages * 4096) // (1024 * 1024))
            
            # CPU via uptime
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            if uptime_result.returncode == 0:
                output = uptime_result.stdout
                if 'load averages:' in output:
                    load_avg_str = output.split('load averages:')[-1].strip().split()[0]
                    load_avg_str = load_avg_str.replace(',', '.')
                    metrics['cpu_percent'] = int(min(float(load_avg_str) * 25, 100))
            
            return metrics
            
        except Exception as e:
            print(f"Erreur métriques: {e}")
            return {}
    
    def update_status_display(self):
        """Met à jour l'affichage du statut"""
        metrics = self.get_system_metrics()
        
        if not metrics:
            return
        
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        # Déterminer le statut
        if disk_percent > 85 or memory_percent > 80:
            status_text = "⚠️  Attention requise"
            self.current_icon = "⚠️"
        elif disk_percent > 70 or memory_percent > 65:
            status_text = "🟡 Surveillance active"
            self.current_icon = "🟡"
        else:
            status_text = "✅ Système optimal"
            self.current_icon = "🛡️"
        
        # Créer le statut pour l'app Swift
        status_data = {
            'statusText': f"{status_text} ({datetime.now().strftime('%H:%M')})",
            'diskPercent': disk_percent,
            'diskFree': metrics.get('disk_free', '--'),
            'memoryPercent': memory_percent,
            'memoryFreeMB': metrics.get('memory_free_mb', 0),
            'cpuPercent': cpu_percent,
            'autoCleanupEnabled': self.config['auto_cleanup_enabled'],
            'notificationsEnabled': self.config['notifications_enabled'],
            'lastUpdate': datetime.now().isoformat()
        }
        
        self.update_status_file(status_data)
        
        # Vérifier si nettoyage automatique nécessaire
        if self.config['auto_cleanup_enabled'] and disk_percent > self.config['auto_cleanup_threshold']:
            self.schedule_auto_cleanup(disk_percent)
        
        print(f"🛡️  Status: {status_text} | Disque: {disk_percent}% | RAM: {memory_percent}% | CPU: {cpu_percent}%")
    
    def schedule_auto_cleanup(self, disk_percent):
        """Programme un nettoyage automatique"""
        if self.config['notifications_enabled']:
            self.send_notification(
                "MacCleaner Guardian",
                f"Nettoyage automatique dans 30 secondes (disque {disk_percent}%)"
            )
        
        def delayed_cleanup():
            time.sleep(30)
            self.perform_auto_cleanup()
        
        threading.Thread(target=delayed_cleanup, daemon=True).start()
    
    def perform_auto_cleanup(self):
        """Effectue le nettoyage automatique"""
        try:
            print("🧹 Démarrage nettoyage automatique...")
            actions = []
            
            # Vider la corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists():
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=30, capture_output=True)
                actions.append("Corbeille vidée")
            
            # Nettoyer caches sécurisés
            cache_paths = [
                Path.home() / 'Library/Caches/com.apple.Safari/WebKitCache',
                Path('/tmp')
            ]
            
            for cache_path in cache_paths:
                if cache_path.exists():
                    try:
                        subprocess.run([
                            'find', str(cache_path), 
                            '-type', 'f', '-mtime', '+7', 
                            '-delete'
                        ], timeout=60, capture_output=True)
                        actions.append(f"Cache {cache_path.name} nettoyé")
                    except:
                        pass
            
            # Purge mémoire
            try:
                subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
                actions.append("Mémoire purgée")
            except:
                pass
            
            # Mettre à jour config
            self.config['last_cleanup'] = datetime.now().isoformat()
            self.save_config()
            
            # Notification de succès
            if actions and self.config['notifications_enabled']:
                self.send_notification(
                    "Nettoyage terminé",
                    f"{len(actions)} optimisations appliquées"
                )
            
            print(f"✅ Nettoyage terminé: {len(actions)} actions")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage auto: {e}")
    
    def send_notification(self, title, message):
        """Envoie une notification macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" sound name "Funk"
            '''
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def monitoring_loop(self):
        """Boucle de surveillance principale"""
        print("🔍 Démarrage surveillance système...")
        
        while self.monitoring_active:
            try:
                self.update_status_display()
                time.sleep(self.config['monitoring_interval'])
            except Exception as e:
                print(f"❌ Erreur surveillance: {e}")
                time.sleep(60)
    
    def start_monitoring(self):
        """Démarre la surveillance en arrière-plan"""
        monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        monitoring_thread.start()
    
    def run_daemon(self):
        """Lance le daemon de surveillance"""
        try:
            print("🛡️  MacCleaner Guardian MenuBar - Démarrage...")
            self.update_status_display()  # Mise à jour initiale
            
            while self.monitoring_active:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\\n🛡️  MacCleaner Guardian arrêté.")
            self.monitoring_active = False

def handle_command_line():
    """Gère les commandes en ligne de commande"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        guardian = MacCleanerMenuBarNative()
        
        if command == '--cleanup':
            guardian.perform_auto_cleanup()
        elif command == '--optimize':
            # Optimisation rapide
            try:
                subprocess.run(['sudo', 'dscacheutil', '-flushcache'], timeout=10, capture_output=True)
                subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
                guardian.send_notification("Optimisation terminée", "Système optimisé")
                print("⚡ Optimisation terminée")
            except Exception as e:
                print(f"❌ Erreur optimisation: {e}")
        
        elif command == '--toggle-cleanup':
            guardian.config['auto_cleanup_enabled'] = not guardian.config['auto_cleanup_enabled']
            guardian.save_config()
            print(f"🔧 Nettoyage automatique: {'ON' if guardian.config['auto_cleanup_enabled'] else 'OFF'}")
        
        elif command == '--toggle-notifications':
            guardian.config['notifications_enabled'] = not guardian.config['notifications_enabled']
            guardian.save_config()
            print(f"🔔 Notifications: {'ON' if guardian.config['notifications_enabled'] else 'OFF'}")
        
        elif command == '--daemon':
            guardian.run_daemon()
        
        return True
    
    return False

def main():
    """Point d'entrée principal"""
    
    # Vérifier commandes ligne de commande
    if handle_command_line():
        return
    
    # Mode GUI par défaut
    guardian = MacCleanerMenuBarNative()
    guardian.run_daemon()

if __name__ == "__main__":
    main()