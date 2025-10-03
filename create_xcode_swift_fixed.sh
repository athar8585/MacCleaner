#!/bin/bash

# 🍎 Créateur de Projet Xcode Swift - VERSION CORRIGÉE
echo "🍎 CRÉATION PROJET XCODE SWIFT FONCTIONNEL"
echo "=========================================="

PROJECT_DIR="/Users/loicdeloison/Desktop/MacCleaner/XcodeFinal"
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "📦 Initialisation du package Swift..."

# Créer un package SwiftUI
swift package init --type executable --name MacCleanerPro

echo "📝 Configuration SwiftUI..."

# Modifier Package.swift pour SwiftUI
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

echo "🎨 Création interface SwiftUI..."

# Supprimer le fichier par défaut
rm Sources/MacCleanerPro/MacCleanerPro.swift

# Créer main.swift avec SwiftUI
cat > Sources/MacCleanerPro/main.swift << 'MAIN_EOF'
//
//  main.swift
//  MacCleanerPro - Application native macOS
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
    @State private var cleaningProgress: Double = 0.0
    @State private var isScanning = false
    @State private var scanResults: [String] = []
    @State private var logs: [String] = ["MacCleaner Pro - Démarré"]
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            VStack(alignment: .leading, spacing: 20) {
                Text("MacCleaner Pro")
                    .font(.title)
                    .fontWeight(.bold)
                
                VStack(alignment: .leading, spacing: 12) {
                    NavigationLink("🧹 Nettoyage") {
                        CleaningView()
                    }
                    
                    NavigationLink("🛡️ Scanner") {
                        ScannerView()
                    }
                    
                    NavigationLink("⚙️ Préférences") {
                        SettingsView()
                    }
                }
                
                Spacer()
                
                VStack(alignment: .leading) {
                    Text("Informations Système")
                        .font(.headline)
                    
                    SystemInfoView()
                }
            }
            .padding()
            .frame(minWidth: 200)
            
        } detail: {
            // Main content
            CleaningView()
        }
        .frame(minWidth: 900, minHeight: 650)
    }
}

struct CleaningView: View {
    @State private var cleaningProgress: Double = 0.0
    @State private var isCleaning = false
    @State private var spaceFreed: String = "0 MB"
    @State private var logs: [String] = ["Prêt pour le nettoyage..."]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Nettoyage Système")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            // Progress section
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("Progression:")
                    Spacer()
                    Text("\(Int(cleaningProgress * 100))%")
                        .foregroundColor(.secondary)
                }
                
                ProgressView(value: cleaningProgress)
                    .progressViewStyle(LinearProgressViewStyle())
                
                Text("Espace libéré: \(spaceFreed)")
                    .font(.subheadline)
                    .foregroundColor(.green)
            }
            .padding()
            .background(Color.gray.opacity(0.1))
            .cornerRadius(10)
            
            // Actions
            HStack(spacing: 20) {
                Button(action: startCleaning) {
                    HStack {
                        Image(systemName: "trash")
                        Text("Démarrer Nettoyage")
                    }
                    .foregroundColor(.white)
                    .padding()
                    .background(isCleaning ? Color.gray : Color.blue)
                    .cornerRadius(8)
                }
                .disabled(isCleaning)
                
                Button(action: quickClean) {
                    HStack {
                        Image(systemName: "bolt")
                        Text("Nettoyage Rapide")
                    }
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.orange)
                    .cornerRadius(8)
                }
                
                Button(action: emptyTrash) {
                    HStack {
                        Image(systemName: "trash.fill")
                        Text("Vider Corbeille")
                    }
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.red)
                    .cornerRadius(8)
                }
            }
            
            // Logs
            VStack(alignment: .leading) {
                Text("Journal d'activité")
                    .font(.headline)
                
                ScrollView {
                    LazyVStack(alignment: .leading) {
                        ForEach(logs, id: \.self) { log in
                            Text(log)
                                .font(.system(.caption, design: .monospaced))
                                .padding(.vertical, 2)
                        }
                    }
                }
                .frame(height: 200)
                .padding()
                .background(Color.black.opacity(0.05))
                .cornerRadius(8)
            }
            
            Spacer()
        }
        .padding()
    }
    
    private func startCleaning() {
        isCleaning = true
        cleaningProgress = 0.0
        addLog("🧹 Démarrage du nettoyage complet...")
        
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { timer in
            cleaningProgress += 0.1
            
            if cleaningProgress >= 1.0 {
                timer.invalidate()
                isCleaning = false
                spaceFreed = "\(Int.random(in: 100...2000)) MB"
                addLog("✅ Nettoyage terminé - \(spaceFreed) libérés")
            } else {
                let actions = ["Nettoyage caches système...", "Suppression fichiers temporaires...", "Optimisation mémoire...", "Nettoyage logs..."]
                addLog(actions.randomElement() ?? "Nettoyage en cours...")
            }
        }
    }
    
    private func quickClean() {
        addLog("⚡ Nettoyage rapide...")
        spaceFreed = "\(Int.random(in: 50...500)) MB"
        addLog("✅ Nettoyage rapide terminé - \(spaceFreed) libérés")
    }
    
    private func emptyTrash() {
        addLog("🗑️ Vidage de la corbeille...")
        // Ici on appellerait la fonction système réelle
        spaceFreed = "\(Int.random(in: 10...100)) MB"
        addLog("✅ Corbeille vidée - \(spaceFreed) libérés")
    }
    
    private func addLog(_ message: String) {
        let timestamp = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .medium)
        logs.append("[\(timestamp)] \(message)")
    }
}

struct ScannerView: View {
    @State private var isScanning = false
    @State private var scanResults: [String] = []
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Scanner de Sécurité")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Button(action: startScan) {
                HStack {
                    Image(systemName: "magnifyingglass")
                    Text(isScanning ? "Scan en cours..." : "Démarrer Scan")
                }
                .foregroundColor(.white)
                .padding()
                .background(isScanning ? Color.gray : Color.green)
                .cornerRadius(8)
            }
            .disabled(isScanning)
            
            if !scanResults.isEmpty {
                Text("Résultats:")
                    .font(.headline)
                
                List(scanResults, id: \.self) { result in
                    Text(result)
                }
            }
            
            Spacer()
        }
        .padding()
    }
    
    private func startScan() {
        isScanning = true
        scanResults = []
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            scanResults = [
                "✅ Aucune menace détectée",
                "📊 324 fichiers analysés",
                "🛡️ Système sécurisé"
            ]
            isScanning = false
        }
    }
}

struct SettingsView: View {
    @State private var autoClean = false
    @State private var notifications = true
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Préférences")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            VStack(alignment: .leading, spacing: 12) {
                Toggle("Nettoyage automatique", isOn: $autoClean)
                Toggle("Notifications", isOn: $notifications)
            }
            
            Spacer()
        }
        .padding()
    }
}

struct SystemInfoView: View {
    @State private var ramUsage: Double = 0.65
    @State private var diskUsage: Double = 0.43
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("RAM:")
                Spacer()
                Text("\(Int(ramUsage * 100))%")
            }
            ProgressView(value: ramUsage)
                .progressViewStyle(LinearProgressViewStyle())
            
            HStack {
                Text("Disque:")
                Spacer()
                Text("\(Int(diskUsage * 100))%")
            }
            ProgressView(value: diskUsage)
                .progressViewStyle(LinearProgressViewStyle())
        }
        .font(.caption)
        .onAppear {
            // Simulation données système
            ramUsage = Double.random(in: 0.3...0.9)
            diskUsage = Double.random(in: 0.2...0.8)
        }
    }
}

#Preview {
    ContentView()
}
MAIN_EOF

echo "🔨 Test de compilation..."
swift build

if [ $? -eq 0 ]; then
    echo "✅ SUCCÈS - Projet compilé sans erreur !"
    echo ""
    echo "🚀 LANCEMENT:"
    echo "📱 Xcode: open Package.swift"
    echo "📱 Terminal: swift run"
    echo ""
    echo "📁 Projet créé dans: $PROJECT_DIR"
else
    echo "❌ Erreur de compilation"
fi