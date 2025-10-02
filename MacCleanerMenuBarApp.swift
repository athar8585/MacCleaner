
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
                print("Erreur mise à jour données: \(error)")
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
                statusItem.title = "📊 \(statusText) (\(timestamp))"
            }
            
            // Métriques
            if let diskItem = menu.item(withTag: 101) {
                let diskPercent = systemData["disk_percent"] as? Int ?? 0
                let diskFree = systemData["disk_free"] as? String ?? "--"
                diskItem.title = "💾 Disque: \(diskPercent)% (\(diskFree) libre)"
            }
            
            if let memoryItem = menu.item(withTag: 102) {
                let memoryPercent = systemData["memory_percent"] as? Int ?? 0
                let memoryFree = systemData["memory_free_mb"] as? Int ?? 0
                memoryItem.title = "🧠 Mémoire: \(memoryPercent)% (\(memoryFree)MB libre)"
            }
            
            if let cpuItem = menu.item(withTag: 103) {
                let cpuPercent = systemData["cpu_percent"] as? Int ?? 0
                cpuItem.title = "⚡ CPU: \(cpuPercent)%"
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
                print("Erreur exécution commande: \(error)")
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
