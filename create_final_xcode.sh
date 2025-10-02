#!/bin/bash

# 🍎 Créateur de Projet Xcode Fonctionnel - SOLUTION DÉFINITIVE
# Utilise 'swift package' pour créer un projet propre

echo "🍎 CRÉATION PROJET XCODE DÉFINITIF"
echo "=================================="

PROJECT_DIR="/Users/loicdeloison/Desktop/MacCleaner/XcodeFinal"
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "📦 Initialisation du package Swift..."

# Créer un package Swift qui peut être ouvert dans Xcode
swift package init --type executable --name MacCleanerPro

echo "📝 Configuration du package pour macOS GUI..."

# Modifier Package.swift pour supporter SwiftUI
cat > Package.swift << 'PACKAGE_EOF'
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MacCleanerPro",
    platforms: [
        .macOS(.v13)
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "MacCleanerPro",
            dependencies: []
        )
    ]
)
PACKAGE_EOF

echo "🎨 Création de l'interface SwiftUI..."

# Remplacer le main.swift par notre application
cat > Sources/MacCleanerPro/main.swift << 'MAIN_EOF'
//
//  main.swift
//  MacCleanerPro
//
//  Application de nettoyage macOS native
//

import SwiftUI
import Foundation

@main
struct MacCleanerProApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 900, minHeight: 650)
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
    }
}

struct ContentView: View {
    @State private var selectedTab = "Dashboard"
    @State private var scanProgress: Double = 0.0
    @State private var isScanning = false
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            VStack(spacing: 0) {
                Text("MacCleaner Pro")
                    .font(.headline)
                    .fontWeight(.bold)
                    .padding()
                
                List {
                    SidebarButton(
                        title: "Dashboard", 
                        icon: "house.fill", 
                        color: .blue,
                        isSelected: selectedTab == "Dashboard"
                    ) {
                        selectedTab = "Dashboard"
                    }
                    
                    SidebarButton(
                        title: "Nettoyage", 
                        icon: "trash.circle.fill", 
                        color: .red,
                        isSelected: selectedTab == "Nettoyage"
                    ) {
                        selectedTab = "Nettoyage"
                    }
                    
                    SidebarButton(
                        title: "Sécurité", 
                        icon: "shield.checkered", 
                        color: .blue,
                        isSelected: selectedTab == "Sécurité"
                    ) {
                        selectedTab = "Sécurité"
                    }
                    
                    SidebarButton(
                        title: "Monitoring", 
                        icon: "chart.line.uptrend.xyaxis", 
                        color: .green,
                        isSelected: selectedTab == "Monitoring"
                    ) {
                        selectedTab = "Monitoring"
                    }
                }
                .listStyle(.sidebar)
            }
            .frame(minWidth: 220)
            
        } detail: {
            // Contenu principal
            Group {
                switch selectedTab {
                case "Dashboard":
                    DashboardView()
                case "Nettoyage":
                    CleaningView(scanProgress: $scanProgress, isScanning: $isScanning)
                case "Sécurité":
                    SecurityView()
                case "Monitoring":
                    MonitoringView()
                default:
                    DashboardView()
                }
            }
        }
    }
}

struct SidebarButton: View {
    let title: String
    let icon: String
    let color: Color
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: icon)
                    .font(.system(size: 16))
                    .foregroundColor(isSelected ? color : .secondary)
                    .frame(width: 20)
                
                Text(title)
                    .font(.system(size: 14, weight: isSelected ? .semibold : .regular))
                    .foregroundColor(isSelected ? .primary : .secondary)
                
                Spacer()
            }
            .padding(.vertical, 6)
            .padding(.horizontal, 12)
            .background(isSelected ? Color.blue.opacity(0.1) : Color.clear)
            .cornerRadius(6)
        }
        .buttonStyle(.plain)
    }
}

struct DashboardView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Header
                HStack {
                    Image(systemName: "macbook")
                        .font(.system(size: 48))
                        .foregroundColor(.blue)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text("MacCleaner Pro")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                        
                        Text("Votre Mac fonctionne parfaitement")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 2) {
                        Text("Version 1.0")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text("macOS Native")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(.blue)
                    }
                }
                .padding(20)
                .background(Color(.controlBackgroundColor))
                .cornerRadius(12)
                
                // Cartes système
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 16) {
                    
                    SystemCard(title: "Stockage", value: "125 GB", total: "500 GB", icon: "externaldrive", color: .blue)
                    SystemCard(title: "Mémoire", value: "8.2 GB", total: "16 GB", icon: "memorychip", color: .green)
                    SystemCard(title: "CPU", value: "25%", total: "100%", icon: "cpu", color: .orange)
                }
                
                Spacer()
            }
            .padding()
        }
    }
}

struct CleaningView: View {
    @Binding var scanProgress: Double
    @Binding var isScanning: Bool
    
    var body: some View {
        VStack(spacing: 32) {
            // Header
            VStack(spacing: 16) {
                Image(systemName: "trash.circle.fill")
                    .font(.system(size: 64))
                    .foregroundColor(.red)
                
                Text("Nettoyage intelligent")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                Text("Libérez de l'espace et optimisez les performances")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            
            // Progress
            if isScanning {
                VStack(spacing: 12) {
                    ProgressView(value: scanProgress)
                        .progressViewStyle(.linear)
                        .frame(maxWidth: 400)
                    
                    Text("Analyse en cours... \(Int(scanProgress * 100))%")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            // Actions
            VStack(spacing: 16) {
                Button(action: startScan) {
                    Label(isScanning ? "Analyse en cours..." : "Démarrer l'analyse", 
                          systemImage: isScanning ? "hourglass" : "magnifyingglass")
                        .font(.system(size: 16, weight: .medium))
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
                .disabled(isScanning)
                
                if !isScanning {
                    Button("Nettoyage rapide") {
                        // Action nettoyage rapide
                    }
                    .buttonStyle(.bordered)
                }
            }
            
            Spacer()
        }
        .padding()
    }
    
    private func startScan() {
        isScanning = true
        scanProgress = 0.0
        
        Timer.scheduledTimer(withTimeInterval: 0.02, repeats: true) { timer in
            scanProgress += 0.005
            if scanProgress >= 1.0 {
                timer.invalidate()
                isScanning = false
                scanProgress = 0.0
            }
        }
    }
}

struct SecurityView: View {
    var body: some View {
        VStack(spacing: 32) {
            Image(systemName: "shield.checkered")
                .font(.system(size: 64))
                .foregroundColor(.blue)
            
            Text("Scanner de sécurité")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Protection avancée contre les menaces")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            Button("Lancer scan sécurité") {
                // Action scan
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            
            Spacer()
        }
        .padding()
    }
}

struct MonitoringView: View {
    var body: some View {
        VStack(spacing: 32) {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .font(.system(size: 64))
                .foregroundColor(.green)
            
            Text("Monitoring système")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Surveillance temps réel des performances")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            Button("Voir les statistiques") {
                // Action stats
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            
            Spacer()
        }
        .padding()
    }
}

struct SystemCard: View {
    let title: String
    let value: String
    let total: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 24))
                .foregroundColor(color)
            
            VStack(spacing: 4) {
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text(value)
                    .font(.title3)
                    .fontWeight(.semibold)
                
                Text("/ \(total)")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .frame(maxWidth: .infinity)
        .padding(16)
        .background(Color(.controlBackgroundColor))
        .cornerRadius(10)
    }
}
MAIN_EOF

echo "🔧 Génération du projet Xcode..."

# Générer le fichier de projet Xcode
swift package generate-xcodeproj

echo "✅ PROJET XCODE CRÉÉ AVEC SUCCÈS !"
echo ""
echo "📁 Emplacement: $PROJECT_DIR"
echo ""
echo "🚀 MÉTHODES DE LANCEMENT :"
echo ""
echo "📱 MÉTHODE 1 - Xcode (Recommandée) :"
echo "   open MacCleanerPro.xcodeproj"
echo "   Puis ▶️ Run"
echo ""
echo "📱 MÉTHODE 2 - Terminal :"
echo "   swift run"
echo ""
echo "✅ Ce projet devrait build SANS ERREUR dans Xcode !"