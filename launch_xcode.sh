#!/bin/bash

# 🍎 MacCleaner Pro - Lanceur Xcode
# Ouvre directement le projet dans Xcode

echo "🍎 LANCEMENT MACCLEANR PRO - XCODE"
echo "=================================="

PROJECT_PATH="/Users/loicdeloison/Desktop/MacCleaner/XcodeProject/MacCleanerPro.xcodeproj"

# Vérifier si Xcode est installé
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ ERREUR: Xcode n'est pas installé"
    echo "📱 Installer Xcode depuis l'App Store"
    exit 1
fi

# Vérifier si le projet existe
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ ERREUR: Projet Xcode non trouvé"
    echo "📁 Chemin: $PROJECT_PATH"
    exit 1
fi

echo "✅ Xcode détecté"
echo "📁 Ouverture du projet..."

# Ouvrir Xcode avec le projet
open "$PROJECT_PATH"

echo "🚀 PROJET OUVERT DANS XCODE !"
echo ""
echo "🔧 ÉTAPES SUIVANTES DANS XCODE :"
echo "1. Sélectionner 'MacCleanerPro' dans le navigateur"
echo "2. Cliquer sur ▶️ (Run) ou Cmd+R"
echo "3. L'app s'ouvrira comme une vraie app native !"
echo ""
echo "📱 RÉSULTAT : Application .app authentique macOS"