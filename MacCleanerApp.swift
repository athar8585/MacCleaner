import SwiftUI
import Foundation

@main
struct MacCleanerApp: App {
    @StateObject private var cleanerManager = MacCleanerManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(cleanerManager)
        }
        .windowStyle(DefaultWindowStyle())
        
        MenuBarExtra("MacCleaner Pro", systemImage: "sparkles") {
            MenuBarView()
                .environmentObject(cleanerManager)
        }
        .menuBarExtraStyle(.window)
    }
}

struct ContentView: View {
    @EnvironmentObject var cleanerManager: MacCleanerManager
    @State private var selectedTab = 0
    
    var body: some View {
        NavigationView {
            VStack {
                // En-tête avec statut
                HeaderView()
                
                // Onglets principaux
                TabView(selection: $selectedTab) {
                    // Onglet Nettoyage Rapide
                    QuickCleanView()
                        .tabItem {
                            Image(systemName: "bolt.fill")
                            Text("Nettoyage Rapide")
                        }
                        .tag(0)
                    
                    // Onglet Surveillance
                    MonitoringView()
                        .tabItem {
                            Image(systemName: "chart.line.uptrend.xyaxis")
                            Text("Surveillance")
                        }
                        .tag(1)
                    
                    // Onglet Protection
                    SecurityView()
                        .tabItem {
                            Image(systemName: "shield.fill")
                            Text("Protection")
                        }
                        .tag(2)
                    
                    // Onglet Paramètres
                    SettingsView()
                        .tabItem {
                            Image(systemName: "gear")
                            Text("Paramètres")
                        }
                        .tag(3)
                }
            }
            .frame(minWidth: 800, minHeight: 600)
        }
    }
}

struct HeaderView: View {
    @EnvironmentObject var cleanerManager: MacCleanerManager
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("MacCleaner Pro")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                Text("Système autonome de nettoyage et protection")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            // Indicateurs de statut
            HStack(spacing: 20) {
                StatusIndicator(
                    title: "Surveillance",
                    isActive: cleanerManager.isMonitoring,
                    color: .green
                )
                
                StatusIndicator(
                    title: "Protection",
                    isActive: cleanerManager.protectionEnabled,
                    color: .blue
                )
                
                StatusIndicator(
                    title: "Anti-Malware",
                    isActive: cleanerManager.malwareScanEnabled,
                    color: .orange
                )
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
    }
}

struct StatusIndicator: View {
    let title: String
    let isActive: Bool
    let color: Color
    
    var body: some View {
        VStack {
            Circle()
                .fill(isActive ? color : Color.gray)
                .frame(width: 12, height: 12)
            
            Text(title)
                .font(.caption)
                .foregroundColor(isActive ? .primary : .secondary)
        }
    }
}

struct QuickCleanView: View {
    @EnvironmentObject var cleanerManager: MacCleanerManager
    @State private var selectedOptions: Set<CleanupOption> = []
    @State private var showingResults = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Actions rapides
            HStack(spacing: 15) {
                QuickActionButton(
                    title: "Nettoyage Express",
                    subtitle: "Nettoyage sécurisé en 1 clic",
                    icon: "bolt.circle.fill",
                    color: .green
                ) {
                    cleanerManager.performQuickClean()
                }
                
                QuickActionButton(
                    title: "Scan Malware",
                    subtitle: "Vérification sécuritaire",
                    icon: "shield.checkerboard",
                    color: .orange
                ) {
                    cleanerManager.scanForMalware()
                }
                
                QuickActionButton(
                    title: "Optimisation",
                    subtitle: "Boost performances",
                    icon: "speedometer",
                    color: .blue
                ) {
                    cleanerManager.optimizeSystem()
                }
            }
            
            Divider()
            
            // Options de nettoyage détaillées
            Text("Options de Nettoyage Avancées")
                .font(.headline)
                .padding(.top)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                ForEach(CleanupOption.allCases, id: \.self) { option in
                    CleanupOptionCard(
                        option: option,
                        isSelected: selectedOptions.contains(option)
                    ) {
                        if selectedOptions.contains(option) {
                            selectedOptions.remove(option)
                        } else {
                            selectedOptions.insert(option)
                        }
                    }
                }
            }
            
            Spacer()
            
            // Boutons d'action
            HStack {
                Button("Analyser Seulement") {
                    cleanerManager.analyzeOnly(options: Array(selectedOptions))
                }
                .buttonStyle(.bordered)
                
                Spacer()
                
                Button("Nettoyer Maintenant") {
                    cleanerManager.performCleanup(options: Array(selectedOptions))
                    showingResults = true
                }
                .buttonStyle(.borderedProminent)
                .disabled(selectedOptions.isEmpty)
            }
        }
        .padding()
        .sheet(isPresented: $showingResults) {
            CleanupResultsView()
        }
    }
}

struct QuickActionButton: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 30))
                    .foregroundColor(color)
                
                Text(title)
                    .font(.headline)
                    .multilineTextAlignment(.center)
                
                Text(subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity, minHeight: 100)
            .padding()
            .background(Color(NSColor.controlBackgroundColor))
            .cornerRadius(12)
        }
        .buttonStyle(.plain)
    }
}

struct CleanupOptionCard: View {
    let option: CleanupOption
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Image(systemName: option.icon)
                            .foregroundColor(option.color)
                        
                        Text(option.title)
                            .font(.headline)
                            .foregroundColor(.primary)
                    }
                    
                    Text(option.description)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.leading)
                    
                    Text(option.estimatedSize)
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(option.color)
                }
                
                Spacer()
                
                Image(systemName: isSelected ? "checkmark.circle.fill" : "circle")
                    .foregroundColor(isSelected ? .accentColor : .secondary)
                    .font(.title2)
            }
            .padding()
            .background(isSelected ? Color.accentColor.opacity(0.1) : Color(NSColor.controlBackgroundColor))
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(isSelected ? Color.accentColor : Color.clear, lineWidth: 2)
            )
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
    }
}

enum CleanupOption: String, CaseIterable {
    case systemCaches = "system_caches"
    case userCaches = "user_caches"
    case logs = "logs"
    case downloads = "downloads"
    case trash = "trash"
    case browserData = "browser_data"
    
    var title: String {
        switch self {
        case .systemCaches: return "Caches Système"
        case .userCaches: return "Caches Utilisateur"
        case .logs: return "Logs & Diagnostics"
        case .downloads: return "Anciens Téléchargements"
        case .trash: return "Corbeille"
        case .browserData: return "Données Navigateur"
        }
    }
    
    var description: String {
        switch self {
        case .systemCaches: return "Caches macOS et applications"
        case .userCaches: return "Caches personnels"
        case .logs: return "Journaux et rapports de crash"
        case .downloads: return "Fichiers > 30 jours"
        case .trash: return "Vider la corbeille"
        case .browserData: return "Historique, cookies (optionnel)"
        }
    }
    
    var icon: String {
        switch self {
        case .systemCaches: return "cpu"
        case .userCaches: return "person.crop.circle"
        case .logs: return "doc.text"
        case .downloads: return "arrow.down.circle"
        case .trash: return "trash"
        case .browserData: return "safari"
        }
    }
    
    var color: Color {
        switch self {
        case .systemCaches: return .blue
        case .userCaches: return .green
        case .logs: return .orange
        case .downloads: return .purple
        case .trash: return .red
        case .browserData: return .cyan
        }
    }
    
    var estimatedSize: String {
        // Ces valeurs seraient calculées dynamiquement dans une vraie app
        switch self {
        case .systemCaches: return "~2.5 GB"
        case .userCaches: return "~800 MB"
        case .logs: return "~200 MB"
        case .downloads: return "~1.2 GB"
        case .trash: return "~500 MB"
        case .browserData: return "~150 MB"
        }
    }
}

struct MonitoringView: View {
    @EnvironmentObject var cleanerManager: MacCleanerManager
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Surveillance Système")
                .font(.title2)
                .fontWeight(.bold)
            
            // Métriques en temps réel
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                SystemMetricCard(
                    title: "Utilisation Disque",
                    value: cleanerManager.diskUsage,
                    unit: "%",
                    color: cleanerManager.diskUsage > 85 ? .red : .green,
                    icon: "internaldrive"
                )
                
                SystemMetricCard(
                    title: "Utilisation Mémoire",
                    value: cleanerManager.memoryUsage,
                    unit: "%",
                    color: cleanerManager.memoryUsage > 80 ? .orange : .green,
                    icon: "memorychip"
                )
                
                SystemMetricCard(
                    title: "Température CPU",
                    value: cleanerManager.cpuTemperature,
                    unit: "°C",
                    color: cleanerManager.cpuTemperature > 80 ? .red : .green,
                    icon: "thermometer"
                )
                
                SystemMetricCard(
                    title: "Espace Libéré",
                    value: cleanerManager.totalSpaceFreed,
                    unit: "GB",
                    color: .blue,
                    icon: "checkmark.circle"
                )
            }
            
            Divider()
            
            // Graphiques et historique
            Text("Historique (7 derniers jours)")
                .font(.headline)
            
            // Ici, vous ajouteriez des graphiques Charts
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(NSColor.controlBackgroundColor))
                .frame(height: 200)
                .overlay(
                    Text("Graphiques d'historique\n(À implémenter avec Charts)")
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                )
            
            Spacer()
        }
        .padding()
    }
}

struct SystemMetricCard: View {
    let title: String
    let value: Double
    let unit: String
    let color: Color
    let icon: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                
                Text(title)
                    .font(.headline)
                    .foregroundColor(.primary)
            }
            
            HStack(alignment: .lastTextBaseline) {
                Text(String(format: "%.1f", value))
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(color)
                
                Text(unit)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
    }
}

struct SecurityView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Protection et Sécurité")
                .font(.title2)
                .fontWeight(.bold)
            
            // Section iCloud
            ProtectionSection(
                title: "Protection iCloud",
                description: "Protège automatiquement vos fichiers synchronisés",
                icon: "icloud.fill",
                color: .blue,
                isEnabled: true
            )
            
            // Section Anti-Malware
            ProtectionSection(
                title: "Anti-Malware",
                description: "Scan en temps réel des menaces",
                icon: "shield.checkered",
                color: .orange,
                isEnabled: true
            )
            
            // Section Fichiers Importants
            ProtectionSection(
                title: "Fichiers Importants",
                description: "Protection automatique des documents récents",
                icon: "doc.fill",
                color: .green,
                isEnabled: true
            )
            
            Divider()
            
            // Quarantaine
            QuarantineView()
            
            Spacer()
        }
        .padding()
    }
}

struct ProtectionSection: View {
    let title: String
    let description: String
    let icon: String
    let color: Color
    let isEnabled: Bool
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
                .frame(width: 30)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                
                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Toggle("", isOn: .constant(isEnabled))
                .toggleStyle(SwitchToggleStyle())
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

struct QuarantineView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Fichiers en Quarantaine")
                .font(.headline)
            
            Text("Aucun fichier en quarantaine")
                .font(.caption)
                .foregroundColor(.secondary)
            
            Button("Gérer la Quarantaine") {
                // Action pour gérer la quarantaine
            }
            .buttonStyle(.bordered)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

struct SettingsView: View {
    var body: some View {
        Form {
            Section("Surveillance Automatique") {
                Toggle("Surveillance Active", isOn: .constant(true))
                
                HStack {
                    Text("Seuil Disque")
                    Spacer()
                    Text("85%")
                        .foregroundColor(.secondary)
                }
                
                HStack {
                    Text("Seuil Mémoire")
                    Spacer()
                    Text("80%")
                        .foregroundColor(.secondary)
                }
            }
            
            Section("Notifications") {
                Toggle("Alertes Système", isOn: .constant(true))
                Toggle("Sons d'Alerte", isOn: .constant(true))
                Toggle("Rapports de Nettoyage", isOn: .constant(true))
            }
            
            Section("Mises à Jour") {
                Toggle("Mise à Jour Automatique", isOn: .constant(true))
                
                HStack {
                    Text("Dernière Mise à Jour")
                    Spacer()
                    Text("Il y a 2 heures")
                        .foregroundColor(.secondary)
                }
                
                Button("Vérifier Maintenant") {
                    // Action de vérification
                }
            }
            
            Section("GitHub Integration") {
                Button("Sauvegarder sur GitHub") {
                    // Action de sauvegarde GitHub
                }
                .buttonStyle(.borderedProminent)
                
                Button("Restaurer depuis GitHub") {
                    // Action de restauration GitHub
                }
                .buttonStyle(.bordered)
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

struct MenuBarView: View {
    @EnvironmentObject var cleanerManager: MacCleanerManager
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("MacCleaner Pro")
                .font(.headline)
            
            Divider()
            
            Button("Nettoyage Express") {
                cleanerManager.performQuickClean()
            }
            
            Button("Scan Malware") {
                cleanerManager.scanForMalware()
            }
            
            Button("Ouvrir Interface") {
                NSApplication.shared.activate(ignoringOtherApps: true)
            }
            
            Divider()
            
            HStack {
                Text("Statut:")
                    .foregroundColor(.secondary)
                
                Circle()
                    .fill(cleanerManager.isMonitoring ? .green : .red)
                    .frame(width: 8, height: 8)
                
                Text(cleanerManager.isMonitoring ? "Actif" : "Inactif")
                    .font(.caption)
            }
            
            Button("Quitter") {
                NSApplication.shared.terminate(nil)
            }
        }
        .padding()
    }
}

struct CleanupResultsView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 60))
                .foregroundColor(.green)
            
            Text("Nettoyage Terminé!")
                .font(.title)
                .fontWeight(.bold)
            
            VStack(alignment: .leading, spacing: 8) {
                ResultRow(label: "Espace libéré:", value: "2.8 GB")
                ResultRow(label: "Fichiers nettoyés:", value: "1,247")
                ResultRow(label: "Durée:", value: "2 min 34 sec")
                ResultRow(label: "Fichiers protégés:", value: "156")
            }
            .padding()
            .background(Color(NSColor.controlBackgroundColor))
            .cornerRadius(12)
            
            Button("Fermer") {
                // Fermer la sheet
            }
            .buttonStyle(.borderedProminent)
        }
        .padding(40)
        .frame(width: 400, height: 350)
    }
}

struct ResultRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            
            Spacer()
            
            Text(value)
                .fontWeight(.semibold)
        }
    }
}

// Manager pour gérer l'état de l'application
class MacCleanerManager: ObservableObject {
    @Published var isMonitoring = false
    @Published var protectionEnabled = true
    @Published var malwareScanEnabled = true
    
    @Published var diskUsage: Double = 0
    @Published var memoryUsage: Double = 0
    @Published var cpuTemperature: Double = 0
    @Published var totalSpaceFreed: Double = 0
    
    init() {
        startMonitoring()
    }
    
    func startMonitoring() {
        isMonitoring = true
        // Simuler des données en temps réel
        Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { _ in
            self.updateMetrics()
        }
    }
    
    private func updateMetrics() {
        // Dans une vraie app, ces valeurs viendraient du système autonome Python
        diskUsage = Double.random(in: 70...90)
        memoryUsage = Double.random(in: 40...85)
        cpuTemperature = Double.random(in: 45...75)
    }
    
    func performQuickClean() {
        // Lancer le nettoyage rapide
        print("Lancement du nettoyage express...")
    }
    
    func scanForMalware() {
        // Lancer le scan malware
        print("Lancement du scan anti-malware...")
    }
    
    func optimizeSystem() {
        // Lancer l'optimisation système
        print("Lancement de l'optimisation...")
    }
    
    func analyzeOnly(options: [CleanupOption]) {
        // Analyser sans nettoyer
        print("Analyse des options: \(options)")
    }
    
    func performCleanup(options: [CleanupOption]) {
        // Effectuer le nettoyage
        print("Nettoyage des options: \(options)")
        totalSpaceFreed += Double.random(in: 0.5...5.0)
    }
}