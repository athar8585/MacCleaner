//
//  MacCleanerProApp.swift
//  MacCleanerPro
//
//  Point d'entrée principal de l'application
//

import SwiftUI

@main
struct MacCleanerProApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 1000, minHeight: 700)
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unified)
        
        Settings {
            SettingsView()
        }
    }
}