//
//  ContentView.swift
//  MacCleanerPro
//
//  Interface principale
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 0
    @State private var scanProgress: Double = 0.0
    @State private var isScanning = false
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            List {
                NavigationLink(destination: DashboardView()) {
                    Label("Dashboard", systemImage: "house.fill")
                }
                
                NavigationLink(destination: CleaningView(scanProgress: $scanProgress, isScanning: $isScanning)) {
                    Label("Nettoyage", systemImage: "trash.circle.fill")
                }
                
                NavigationLink(destination: SecurityView()) {
                    Label("Sécurité", systemImage: "shield.checkered")
                }
                
                NavigationLink(destination: MonitoringView()) {
                    Label("Monitoring", systemImage: "chart.line.uptrend.xyaxis")
                }
            }
            .navigationTitle("MacCleaner Pro")
            
        } detail: {
            DashboardView()
        }
    }
}

struct DashboardView: View {
    var body: some View {
        VStack(spacing: 24) {
            // Header
            HStack {
                Image(systemName: "macbook")
                    .font(.system(size: 48))
                    .foregroundColor(.blue)
                
                VStack(alignment: .leading) {
                    Text("MacCleaner Pro")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text("Votre Mac fonctionne parfaitement")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
            }
            .padding()
            
            // Cartes d'informations
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 16) {
                
                InfoCard(title: "Stockage", value: "125 GB", total: "500 GB", icon: "externaldrive", color: .blue)
                InfoCard(title: "Mémoire", value: "8.2 GB", total: "16 GB", icon: "memorychip", color: .green)
                InfoCard(title: "CPU", value: "25%", total: "100%", icon: "cpu", color: .orange)
            }
            .padding()
            
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(NSColor.controlBackgroundColor))
    }
}

struct CleaningView: View {
    @Binding var scanProgress: Double
    @Binding var isScanning: Bool
    
    var body: some View {
        VStack(spacing: 24) {
            Text("🧹 Nettoyage intelligent")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            if isScanning {
                ProgressView(value: scanProgress)
                    .progressViewStyle(.linear)
                    .padding()
                
                Text("Analyse en cours... \(Int(scanProgress * 100))%")
                    .foregroundColor(.secondary)
            }
            
            Button(action: startScan) {
                Label("Démarrer l'analyse", systemImage: "magnifyingglass")
            }
            .buttonStyle(.borderedProminent)
            .disabled(isScanning)
            
            Spacer()
        }
        .padding()
    }
    
    private func startScan() {
        isScanning = true
        scanProgress = 0.0
        
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            scanProgress += 0.02
            if scanProgress >= 1.0 {
                timer.invalidate()
                isScanning = false
            }
        }
    }
}

struct SecurityView: View {
    var body: some View {
        VStack {
            Image(systemName: "shield.checkered")
                .font(.system(size: 64))
                .foregroundColor(.blue)
            
            Text("Scanner de sécurité")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Protection temps réel")
                .foregroundColor(.secondary)
        }
    }
}

struct MonitoringView: View {
    var body: some View {
        VStack {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .font(.system(size: 64))
                .foregroundColor(.green)
            
            Text("Monitoring système")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Surveillance en temps réel")
                .foregroundColor(.secondary)
        }
    }
}

struct InfoCard: View {
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
        .background(Color(NSColor.windowBackgroundColor))
        .cornerRadius(8)
    }
}

#Preview {
    ContentView()
}
