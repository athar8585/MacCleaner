#!/usr/bin/env swift

import Foundation
import Cocoa
import SwiftUI

// MARK: - Application principale
@main
struct MacCleanerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
    }
}

// MARK: - Vue principale
struct ContentView: View {
    @State private var selectedSection: String = "Dashboard"
    @State private var scanProgress: Double = 0.0
    @State private var isScanning = false
    @State private var systemInfo = SystemInfo()
    
    var body: some View {
        NavigationSplitView {
            // Sidebar navigation
            List {
                Button(action: { selectedSection = "Dashboard" }) {
                    Label("Dashboard", systemImage: "house.fill")
                        .foregroundColor(selectedSection == "Dashboard" ? .blue : .primary)
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedSection = "Nettoyage" }) {
                    Label("Nettoyage", systemImage: "trash.circle.fill")
                        .foregroundColor(selectedSection == "Nettoyage" ? .red : .primary)
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedSection = "Sécurité" }) {
                    Label("Sécurité", systemImage: "shield.checkered")
                        .foregroundColor(selectedSection == "Sécurité" ? .blue : .primary)
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedSection = "Monitoring" }) {
                    Label("Monitoring", systemImage: "chart.line.uptrend.xyaxis")
                        .foregroundColor(selectedSection == "Monitoring" ? .green : .primary)
                }
                .buttonStyle(.plain)
            }
            .navigationTitle("MacCleaner Pro")
            .frame(minWidth: 200)
            
        } detail: {
            // Contenu principal
            Group {
                switch selectedSection {
                case "Dashboard":
                    DashboardView(systemInfo: systemInfo)
                case "Nettoyage":
                    CleaningView(scanProgress: $scanProgress, isScanning: $isScanning)
                case "Sécurité":
                    SecurityView()
                case "Monitoring":
                    MonitoringView()
                default:
                    DashboardView(systemInfo: systemInfo)
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .onAppear {
            systemInfo.updateInfo()
        }
    }
}

// MARK: - Dashboard
struct DashboardView: View {
    let systemInfo: SystemInfo
    
    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Header principal
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
                    
                    VStack(alignment: .trailing, spacing: 4) {
                        Text("Version 1.0.0")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text("macOS Native")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(.blue)
                    }
                }
                .padding()
                .background(Color(NSColor.controlBackgroundColor))
                .cornerRadius(12)
                
                // Informations système
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 16) {
                    
                    SystemCard(
                        title: "Stockage",
                        value: systemInfo.storageUsed,
                        total: systemInfo.storageTotal,
                        icon: "externaldrive",
                        color: .blue
                    )
                    
                    SystemCard(
                        title: "Mémoire",
                        value: systemInfo.memoryUsed,
                        total: systemInfo.memoryTotal,
                        icon: "memorychip",
                        color: .green
                    )
                    
                    SystemCard(
                        title: "CPU",
                        value: "\(systemInfo.cpuUsage)%",
                        total: "100%",
                        icon: "cpu",
                        color: .orange
                    )
                }
                
                // Actions rapides
                HStack(spacing: 16) {
                    ActionButton(
                        title: "Nettoyage rapide",
                        icon: "trash.circle.fill",
                        color: .red
                    )
                    
                    ActionButton(
                        title: "Scan sécurité",
                        icon: "shield.checkered",
                        color: .blue
                    )
                    
                    ActionButton(
                        title: "Optimisation",
                        icon: "speedometer",
                        color: .green
                    )
                }
                .padding()
                
                Spacer()
            }
            .padding()
        }
    }
}

// MARK: - Nettoyage
struct CleaningView: View {
    @Binding var scanProgress: Double
    @Binding var isScanning: Bool
    
    var body: some View {
        VStack(spacing: 24) {
            // Header nettoyage
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
            
            // Barre de progression
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
            
            // Bouton d'action
            Button(action: startScan) {
                Label(isScanning ? "Analyse en cours..." : "Démarrer l'analyse", 
                      systemImage: isScanning ? "hourglass" : "magnifyingglass")
            }
            .buttonStyle(.borderedProminent)
            .disabled(isScanning)
            .controlSize(.large)
            
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
    
    private func startScan() {
        isScanning = true
        scanProgress = 0.0
        
        Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { timer in
            scanProgress += 0.01
            if scanProgress >= 1.0 {
                timer.invalidate()
                isScanning = false
                scanProgress = 0.0
            }
        }
    }
}

// MARK: - Sécurité
struct SecurityView: View {
    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "shield.checkered")
                .font(.system(size: 64))
                .foregroundColor(.blue)
            
            Text("Scanner de sécurité")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Protection avancée contre les menaces")
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Button("Lancer scan sécurité") {
                // Action sécurité
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Monitoring
struct MonitoringView: View {
    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .font(.system(size: 64))
                .foregroundColor(.green)
            
            Text("Monitoring système")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Surveillance en temps réel des performances")
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Button("Voir les statistiques") {
                // Action monitoring
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Composants

struct SystemCard: View {
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
            
            Text("/ \(total)")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

struct ActionButton: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        Button(action: {}) {
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

// MARK: - Modèles

class SystemInfo {
    var storageUsed = "125 GB"
    var storageTotal = "500 GB"
    var memoryUsed = "8.2 GB"
    var memoryTotal = "16 GB"
    var cpuUsage = 25
    
    func updateInfo() {
        // Simulation de données
        cpuUsage = Int.random(in: 15...45)
    }
}
