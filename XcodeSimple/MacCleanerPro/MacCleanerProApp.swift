//
//  MacCleanerProApp.swift
//  MacCleanerPro
//
//  Point d'entrée de l'application
//

import SwiftUI

@main
struct MacCleanerProApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 900, minHeight: 600)
        }
        .windowStyle(.titleBar)
    }
}
