//
//  ContentView.swift
//  MacCleanerPro
//
//  Interface principale avec navigation sidebar native macOS
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab: SidebarItem = .dashboard
    @State private var scanProgress: Double = 0.0
    @State private var isScanning = false
    @State private var systemInfo = SystemInfo()
    
    var body: some View {
        NavigationSplitView {
            // SIDEBAR NAVIGATION - Style macOS natif
            List(SidebarItem.allCases, selection: $selectedTab) { item in
                NavigationLink(value: item) {
                    Label(item.title, systemImage: item.icon)
                        .font(.system(size: 14, weight: .medium))
                }
            }
            .navigationSplitViewColumnWidth(min: 200, ideal: 220)
            .listStyle(.sidebar)
            
        } detail: {
            // CONTENU PRINCIPAL
            Group {
                switch selectedTab {
                case .dashboard:
                    DashboardView(systemInfo: $systemInfo)
                case .cleaning:
                    CleaningView(scanProgress: $scanProgress, isScanning: $isScanning)
                case .security:
                    SecurityView()
                case .monitoring:
                    MonitoringView(systemInfo: $systemInfo)
                case .settings:
                    SettingsView()
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(Color(NSColor.controlBackgroundColor))
        }
        .onAppear {
            updateSystemInfo()
        }
    }
    
    private func updateSystemInfo() {
        systemInfo.refreshData()
    }
}

// MARK: - Dashboard View
struct DashboardView: View {
    @Binding var systemInfo: SystemInfo
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Image(systemName: "macbook")
                            .font(.system(size: 32))
                            .foregroundColor(.blue)
                        
                        VStack(alignment: .leading) {
                            Text("MacCleaner Pro")
                                .font(.title)
                                .fontWeight(.bold)
                            
                            Text("Votre Mac fonctionne parfaitement")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        
                        Spacer()
                        
                        VStack(alignment: .trailing) {
                            Text("Dernière analyse")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            Text("Il y a 2 heures")
                                .font(.caption)
                                .fontWeight(.medium)
                        }
                    }
                    .padding()
                    .background(Color(NSColor.controlBackgroundColor))
                    .cornerRadius(12)
                }
                
                // Cartes d'information système
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 16) {
                    
                    SystemInfoCard(
                        title: "Stockage",
                        value: systemInfo.storageUsed,
                        total: systemInfo.storageTotal,
                        icon: "externaldrive",
                        color: .blue
                    )
                    
                    SystemInfoCard(
                        title: "Mémoire",
                        value: systemInfo.memoryUsed,
                        total: systemInfo.memoryTotal,
                        icon: "memorychip",
                        color: .green
                    )
                    
                    SystemInfoCard(
                        title: "CPU",
                        value: "\(Int(systemInfo.cpuUsage))%",
                        total: "100%",
                        icon: "cpu",
                        color: .orange
                    )
                }
                
                // Actions rapides
                VStack(alignment: .leading, spacing: 12) {
                    Text("Actions rapides")
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    HStack(spacing: 12) {
                        QuickActionButton(
                            title: "Nettoyage rapide",
                            icon: "trash.circle.fill",
                            color: .red
                        ) {
                            // Action nettoyage
                        }
                        
                        QuickActionButton(
                            title: "Scan sécurité",
                            icon: "shield.checkered",
                            color: .blue
                        ) {
                            // Action sécurité
                        }
                        
                        QuickActionButton(
                            title: "Optimisation",
                            icon: "speedometer",
                            color: .green
                        ) {
                            // Action optimisation
                        }
                    }
                }
                .padding()
                .background(Color(NSColor.controlBackgroundColor))
                .cornerRadius(12)
                
                Spacer()
            }
            .padding()
        }
    }
}

// MARK: - Cleaning View
struct CleaningView: View {
    @Binding var scanProgress: Double
    @Binding var isScanning: Bool
    @State private var cleaningItems: [CleaningItem] = []
    
    var body: some View {
        VStack(spacing: 24) {
            // Header de nettoyage
            VStack(spacing: 16) {
                HStack {
                    Image(systemName: "trash.circle.fill")
                        .font(.system(size: 48))
                        .foregroundColor(.red)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Nettoyage intelligent")
                            .font(.title)
                            .fontWeight(.bold)
                        
                        Text("Libérez de l'espace et optimisez les performances")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                }
                
                // Barre de progression
                if isScanning {
                    VStack(spacing: 8) {
                        ProgressView(value: scanProgress)
                            .progressViewStyle(.linear)
                        
                        Text("Analyse en cours... \(Int(scanProgress * 100))%")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .padding()
            .background(Color(NSColor.controlBackgroundColor))
            .cornerRadius(12)
            
            // Liste des éléments à nettoyer
            List {
                ForEach(cleaningItems) { item in
                    CleaningItemRow(item: item)
                }
            }
            .listStyle(.inset)
            
            // Boutons d'action
            HStack(spacing: 16) {
                Button(action: startScan) {
                    Label("Démarrer l'analyse", systemImage: "magnifyingglass")
                }
                .buttonStyle(.borderedProminent)
                .disabled(isScanning)
                
                if !cleaningItems.isEmpty {
                    Button(action: startCleaning) {
                        Label("Nettoyer sélectionnés", systemImage: "trash")
                    }
                    .buttonStyle(.bordered)
                }
            }
            .padding()
        }
        .padding()
        .onAppear {
            loadCleaningItems()
        }
    }
    
    private func startScan() {
        isScanning = true
        scanProgress = 0.0
        
        // Simulation de scan
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            scanProgress += 0.02
            if scanProgress >= 1.0 {
                timer.invalidate()
                isScanning = false
                loadCleaningItems()
            }
        }
    }
    
    private func startCleaning() {
        // Logique de nettoyage
        let selectedItems = cleaningItems.filter { $0.isSelected }
        // Traitement...
    }
    
    private func loadCleaningItems() {
        cleaningItems = [
            CleaningItem(name: "Cache navigateurs", size: "2.3 GB", category: .cache),
            CleaningItem(name: "Fichiers temporaires", size: "1.8 GB", category: .temp),
            CleaningItem(name: "Corbeille pleine", size: "945 MB", category: .trash),
            CleaningItem(name: "Logs système", size: "567 MB", category: .logs)
        ]
    }
}

// MARK: - Components

struct SystemInfoCard: View {
    let title: String
    let value: String
    let total: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 24))
                .foregroundColor(color)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            
            Text(value)
                .font(.title2)
                .fontWeight(.semibold)
            
            Text("sur \(total)")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

struct QuickActionButton: View {
    let title: String
    let icon: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 24))
                    .foregroundColor(color)
                
                Text(title)
                    .font(.caption)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color(NSColor.controlBackgroundColor))
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
    }
}

struct CleaningItemRow: View {
    @State var item: CleaningItem
    
    var body: some View {
        HStack {
            Toggle("", isOn: $item.isSelected)
                .toggleStyle(.checkbox)
            
            Image(systemName: item.category.icon)
                .foregroundColor(item.category.color)
            
            VStack(alignment: .leading) {
                Text(item.name)
                    .font(.headline)
                
                Text(item.category.rawValue)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text(item.size)
                .font(.system(.body, design: .monospaced))
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Security View
struct SecurityView: View {
    var body: some View {
        VStack {
            Image(systemName: "shield.checkered")
                .font(.system(size: 64))
                .foregroundColor(.blue)
            
            Text("Scanner de sécurité")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Bientôt disponible")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Monitoring View
struct MonitoringView: View {
    @Binding var systemInfo: SystemInfo
    
    var body: some View {
        VStack {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .font(.system(size: 64))
                .foregroundColor(.green)
            
            Text("Monitoring système")
                .font(.title)
                .fontWeight(.bold)
            
            Text("CPU: \(Int(systemInfo.cpuUsage))%")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Settings View
struct SettingsView: View {
    var body: some View {
        VStack {
            Image(systemName: "gear")
                .font(.system(size: 64))
                .foregroundColor(.gray)
            
            Text("Préférences")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Configuration de l'application")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Models

enum SidebarItem: String, CaseIterable, Identifiable {
    case dashboard = "Dashboard"
    case cleaning = "Nettoyage"
    case security = "Sécurité"
    case monitoring = "Monitoring"
    case settings = "Réglages"
    
    var id: String { rawValue }
    
    var title: String { rawValue }
    
    var icon: String {
        switch self {
        case .dashboard: return "house.fill"
        case .cleaning: return "trash.circle.fill"
        case .security: return "shield.checkered"
        case .monitoring: return "chart.line.uptrend.xyaxis"
        case .settings: return "gear"
        }
    }
}

struct CleaningItem: Identifiable {
    let id = UUID()
    let name: String
    let size: String
    let category: CleaningCategory
    var isSelected = true
}

enum CleaningCategory: String, CaseIterable {
    case cache = "Cache"
    case temp = "Temporaires"
    case trash = "Corbeille"
    case logs = "Logs"
    
    var icon: String {
        switch self {
        case .cache: return "externaldrive.badge.timemachine"
        case .temp: return "clock.badge.exclamationmark"
        case .trash: return "trash.fill"
        case .logs: return "doc.text"
        }
    }
    
    var color: Color {
        switch self {
        case .cache: return .blue
        case .temp: return .orange
        case .trash: return .red
        case .logs: return .purple
        }
    }
}

class SystemInfo: ObservableObject {
    @Published var storageUsed = "125 GB"
    @Published var storageTotal = "500 GB"
    @Published var memoryUsed = "8.2 GB"
    @Published var memoryTotal = "16 GB"
    @Published var cpuUsage: Double = 25.0
    
    func refreshData() {
        // Simulation de données système réelles
        cpuUsage = Double.random(in: 10...60)
    }
}

#Preview {
    ContentView()
}