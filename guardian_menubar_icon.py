#!/usr/bin/env python3
"""
MacCleaner Guardian - VRAIE ICÔNE BARRE DE MENU
Application native macOS avec icône permanente dans la barre de menu
"""

import subprocess
import threading
import time
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

class MacCleanerMenuBarIcon:
    """Icône permanente dans la barre de menu macOS"""
    
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.monitoring_active = True
        self.current_status = "optimal"
        self.status_icons = {
            'optimal': '🛡️',
            'warning': '🟡', 
            'critical': '⚠️',
            'cleaning': '🧹',
            'optimizing': '⚡'
        }
        
        # Configuration
        self.config = {
            'auto_cleanup_enabled': True,
            'monitoring_interval': 30,
            'auto_cleanup_threshold': 85,
            'memory_threshold': 80,
            'notifications_enabled': True,
            'last_cleanup': None
        }
        
        self.load_config()
        self.create_permanent_menu_bar_app()
    
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
    
    def create_permanent_menu_bar_app(self):
        """Crée une vraie application barre de menu avec icône permanente"""
        
        # Créer le code Swift pour une vraie app barre de menu
        swift_menubar_code = '''
import Cocoa
import Foundation

@main
class MacCleanerMenuBarApp: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private var timer: Timer?
    private var currentIcon = "🛡️"
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Créer l'élément de la barre de statut
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = currentIcon
            button.font = NSFont.systemFont(ofSize: 16)
            button.target = self
            button.action = #selector(statusBarButtonClicked)
        }
        
        // Configurer le menu
        setupMenu()
        
        // Démarrer la surveillance
        startMonitoring()
        
        print("🛡️ MacCleaner Guardian - Icône barre de menu active")
    }
    
    @objc private func statusBarButtonClicked() {
        // Rafraîchir les données avant d'afficher le menu
        updateSystemData()
    }
    
    private func setupMenu() {
        let menu = NSMenu()
        
        // Titre avec statut
        let titleItem = NSMenuItem(title: "🛡️ MacCleaner Guardian", action: nil, keyEquivalent: "")
        titleItem.isEnabled = false
        menu.addItem(titleItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Statut système (sera mis à jour dynamiquement)
        let statusItem = NSMenuItem(title: "📊 Analyse en cours...", action: nil, keyEquivalent: "")
        statusItem.tag = 100 // Tag pour l'identifier
        statusItem.isEnabled = false
        menu.addItem(statusItem)
        
        // Métriques détaillées
        let diskItem = NSMenuItem(title: "💾 Disque: --", action: nil, keyEquivalent: "")
        diskItem.tag = 101
        diskItem.isEnabled = false
        menu.addItem(diskItem)
        
        let memoryItem = NSMenuItem(title: "🧠 Mémoire: --", action: nil, keyEquivalent: "")
        memoryItem.tag = 102
        memoryItem.isEnabled = false
        menu.addItem(memoryItem)
        
        let cpuItem = NSMenuItem(title: "⚡ CPU: --", action: nil, keyEquivalent: "")
        cpuItem.tag = 103
        cpuItem.isEnabled = false
        menu.addItem(cpuItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Actions
        let cleanupItem = NSMenuItem(title: "🧹 Nettoyage Rapide", action: #selector(performCleanup), keyEquivalent: "")
        cleanupItem.target = self
        menu.addItem(cleanupItem)
        
        let optimizeItem = NSMenuItem(title: "⚡ Optimisation", action: #selector(performOptimization), keyEquivalent: "")
        optimizeItem.target = self
        menu.addItem(optimizeItem)
        
        let refreshItem = NSMenuItem(title: "🔄 Actualiser", action: #selector(forceRefresh), keyEquivalent: "")
        refreshItem.target = self
        menu.addItem(refreshItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Configuration
        let configItem = NSMenuItem(title: "⚙️ Configuration", action: #selector(showConfiguration), keyEquivalent: "")
        configItem.target = self
        menu.addItem(configItem)
        
        let fullPanelItem = NSMenuItem(title: "📊 Panneau Complet", action: #selector(openFullPanel), keyEquivalent: "")
        fullPanelItem.target = self
        menu.addItem(fullPanelItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Quitter
        let quitItem = NSMenuItem(title: "❌ Quitter Guardian", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    private func startMonitoring() {
        // Timer pour mettre à jour l'icône et les données
        timer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { _ in
            self.updateSystemData()
        }
        
        // Première mise à jour
        updateSystemData()
    }
    
    private func updateSystemData() {
        // Lancer le script Python pour obtenir les données système
        DispatchQueue.global(qos: .background).async {
            let task = Process()
            task.launchPath = "/usr/bin/python3"
            task.arguments = ["guardian_menubar_icon.py", "--get-status"]
            
            let pipe = Pipe()
            task.standardOutput = pipe
            
            do {
                try task.run()
                task.waitUntilExit()
                
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                if let output = String(data: data, encoding: .utf8) {
                    DispatchQueue.main.async {
                        self.parseSystemData(output)
                    }
                }
            } catch {
                print("Erreur mise à jour données: \\(error)")
            }
        }
    }
    
    private func parseSystemData(_ data: String) {
        // Parser les données JSON du script Python
        guard let jsonData = data.data(using: .utf8),
              let systemData = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any] else {
            return
        }
        
        // Mettre à jour l'icône
        let status = systemData["status"] as? String ?? "optimal"
        let newIcon = getIconForStatus(status)
        
        if let button = statusItem.button {
            button.title = newIcon
        }
        
        // Mettre à jour le menu
        if let menu = statusItem.menu {
            // Statut principal
            if let statusItem = menu.item(withTag: 100) {
                let statusText = systemData["status_text"] as? String ?? "Système optimal"
                let timestamp = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .short)
                statusItem.title = "📊 \\(statusText) (\\(timestamp))"
            }
            
            // Métriques
            if let diskItem = menu.item(withTag: 101) {
                let diskPercent = systemData["disk_percent"] as? Int ?? 0
                let diskFree = systemData["disk_free"] as? String ?? "--"
                diskItem.title = "💾 Disque: \\(diskPercent)% (\\(diskFree) libre)"
            }
            
            if let memoryItem = menu.item(withTag: 102) {
                let memoryPercent = systemData["memory_percent"] as? Int ?? 0
                let memoryFree = systemData["memory_free_mb"] as? Int ?? 0
                memoryItem.title = "🧠 Mémoire: \\(memoryPercent)% (\\(memoryFree)MB libre)"
            }
            
            if let cpuItem = menu.item(withTag: 103) {
                let cpuPercent = systemData["cpu_percent"] as? Int ?? 0
                cpuItem.title = "⚡ CPU: \\(cpuPercent)%"
            }
        }
    }
    
    private func getIconForStatus(_ status: String) -> String {
        switch status {
        case "critical": return "⚠️"
        case "warning": return "🟡"
        case "cleaning": return "🧹"
        case "optimizing": return "⚡"
        default: return "🛡️"
        }
    }
    
    @objc private func performCleanup() {
        updateIcon("🧹")
        executeCommand("python3", args: ["guardian_menubar_icon.py", "--cleanup"])
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            self.updateSystemData()
        }
    }
    
    @objc private func performOptimization() {
        updateIcon("⚡")
        executeCommand("python3", args: ["guardian_menubar_icon.py", "--optimize"])
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            self.updateSystemData()
        }
    }
    
    @objc private func forceRefresh() {
        updateSystemData()
    }
    
    @objc private func showConfiguration() {
        executeCommand("python3", args: ["guardian_menubar_icon.py", "--config"])
    }
    
    @objc private func openFullPanel() {
        executeCommand("python3", args: ["maccleaner_guardian.py"])
    }
    
    @objc private func quitApp() {
        NSApplication.shared.terminate(nil)
    }
    
    private func updateIcon(_ icon: String) {
        if let button = statusItem.button {
            button.title = icon
        }
    }
    
    private func executeCommand(_ command: String, args: [String] = []) {
        DispatchQueue.global(qos: .background).async {
            let task = Process()
            task.launchPath = "/usr/bin/env"
            task.arguments = [command] + args
            do {
                try task.run()
            } catch {
                print("Erreur exécution commande: \\(error)")
            }
        }
    }
}

// Point d'entrée
let app = NSApplication.shared
let delegate = MacCleanerMenuBarApp()
app.delegate = delegate
app.setActivationPolicy(.accessory) // Pas d'icône dans le Dock
app.run()
'''
        
        # Sauvegarder le code Swift
        swift_file = Path('/Users/loicdeloison/Desktop/MacCleaner/MacCleanerMenuBarApp.swift')
        with open(swift_file, 'w') as f:
            f.write(swift_menubar_code)
        
        print("📁 Code Swift créé pour l'icône barre de menu")
        
        # Compiler l'application Swift
        self.compile_swift_app()
    
    def compile_swift_app(self):
        """Compile l'application Swift en binaire exécutable"""
        try:
            swift_file = '/Users/loicdeloison/Desktop/MacCleaner/MacCleanerMenuBarApp.swift'
            binary_path = '/Users/loicdeloison/Desktop/MacCleaner/MacCleanerMenuBarApp'
            
            # Compiler avec Swift
            compile_result = subprocess.run([
                'swiftc', 
                '-o', binary_path,
                swift_file,
                '-framework', 'Cocoa'
            ], capture_output=True, text=True, timeout=60)
            
            if compile_result.returncode == 0:
                # Rendre exécutable
                os.chmod(binary_path, 0o755)
                print("✅ Application Swift compilée avec succès")
                
                # Lancer l'application
                self.launch_menu_bar_app()
            else:
                print(f"❌ Erreur compilation Swift: {compile_result.stderr}")
                
        except Exception as e:
            print(f"❌ Erreur compilation: {e}")
    
    def launch_menu_bar_app(self):
        """Lance l'application barre de menu"""
        try:
            binary_path = '/Users/loicdeloison/Desktop/MacCleaner/MacCleanerMenuBarApp'
            
            # Lancer en arrière-plan
            subprocess.Popen([binary_path], 
                           cwd='/Users/loicdeloison/Desktop/MacCleaner')
            
            print("🚀 Application barre de menu lancée!")
            print("💡 Regardez dans la barre de menu en haut à droite pour l'icône 🛡️")
            
        except Exception as e:
            print(f"❌ Erreur lancement app: {e}")
    
    def get_system_metrics(self):
        """Récupère les métriques système"""
        try:
            metrics = {}
            
            # Disque via df
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        metrics['disk_percent'] = int(float(fields[4].replace('%', '')))
                        metrics['disk_free'] = fields[3]
            
            # Mémoire via vm_stat
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\n')
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
            print(f"❌ Erreur métriques: {e}")
            return {}
    
    def get_system_status_json(self):
        """Retourne le statut système en JSON pour l'app Swift"""
        metrics = self.get_system_metrics()
        
        if not metrics:
            return {}
        
        disk_percent = metrics.get('disk_percent', 0)
        memory_percent = metrics.get('memory_percent', 0)
        cpu_percent = metrics.get('cpu_percent', 0)
        
        # Déterminer le statut
        if disk_percent > 85 or memory_percent > 80:
            status = "critical"
            status_text = "Attention requise"
        elif disk_percent > 70 or memory_percent > 65:
            status = "warning"
            status_text = "Surveillance active"
        else:
            status = "optimal"
            status_text = "Système optimal"
        
        return {
            'status': status,
            'status_text': status_text,
            'disk_percent': disk_percent,
            'disk_free': metrics.get('disk_free', '--'),
            'memory_percent': memory_percent,
            'memory_free_mb': metrics.get('memory_free_mb', 0),
            'cpu_percent': cpu_percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def perform_cleanup(self):
        """Effectue un nettoyage rapide"""
        try:
            print("🧹 Démarrage nettoyage...")
            actions = []
            
            # Vider la corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists():
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=30, capture_output=True)
                actions.append("Corbeille")
            
            # Nettoyer caches
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
                        actions.append(f"Cache {cache_path.name}")
                    except:
                        pass
            
            self.config['last_cleanup'] = datetime.now().isoformat()
            self.save_config()
            
            self.send_notification("✅ Nettoyage terminé", f"{len(actions)} optimisations")
            print(f"✅ Nettoyage terminé: {actions}")
            
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
    
    def perform_optimization(self):
        """Effectue une optimisation système"""
        try:
            print("⚡ Démarrage optimisation...")
            
            # DNS flush
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], 
                         timeout=10, capture_output=True)
            
            # Purge mémoire
            subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
            
            self.send_notification("✅ Optimisation OK", "Système optimisé")
            print("⚡ Optimisation terminée")
            
        except Exception as e:
            print(f"❌ Erreur optimisation: {e}")
    
    def show_configuration(self):
        """Affiche la configuration"""
        config_text = f"""⚙️ CONFIGURATION ACTUELLE

🧹 Nettoyage automatique: {'OUI' if self.config['auto_cleanup_enabled'] else 'NON'}
🔔 Notifications: {'OUI' if self.config['notifications_enabled'] else 'NON'}
📊 Seuil disque: {self.config['auto_cleanup_threshold']}%
🧠 Seuil mémoire: {self.config['memory_threshold']}%
⏱️  Intervalle: {self.config['monitoring_interval']}s"""
        
        # Afficher via AppleScript
        script = f'''
        display dialog "{config_text}" buttons {{"🔙 Retour", "📊 Panneau Complet"}} default button "🔙 Retour" with title "⚙️ Configuration Guardian" with icon note
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "Panneau Complet" in result.stdout:
                # Ouvrir le panneau complet
                subprocess.Popen(['python3', 'maccleaner_guardian.py'])
        
        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
    
    def send_notification(self, title, message):
        """Envoie une notification macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" subtitle "MacCleaner Guardian"
            '''
            subprocess.run(['osascript', '-e', script], 
                         capture_output=True, timeout=5)
        except:
            pass

def main():
    """Point d'entrée principal"""
    import sys
    
    guardian = MacCleanerMenuBarIcon()
    
    # Gestion des arguments de ligne de commande pour l'app Swift
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--get-status':
            # Retourner le statut en JSON pour l'app Swift
            status_data = guardian.get_system_status_json()
            print(json.dumps(status_data))
        
        elif command == '--cleanup':
            guardian.perform_cleanup()
        
        elif command == '--optimize':
            guardian.perform_optimization()
        
        elif command == '--config':
            guardian.show_configuration()
        
        return
    
    # Mode normal - créer et lancer l'app barre de menu
    print("🛡️  Création de l'icône barre de menu...")
    print("⏳ Compilation en cours...")

if __name__ == "__main__":
    main()