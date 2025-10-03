#!/bin/bash

# 🚀 Script de lancement MacCleaner Pro Swift
echo "🍎 Lancement MacCleaner Pro Swift Native"
echo "======================================="

PROJECT_PATH="/Users/loicdeloison/Desktop/MacCleanerXcode"

if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Projet non trouvé dans $PROJECT_PATH"
    exit 1
fi

cd "$PROJECT_PATH"

echo "📁 Dossier projet: $(pwd)"
echo "📋 Contenu:"
ls -la

echo ""
echo "🔨 Compilation..."
swift build

if [ $? -eq 0 ]; then
    echo "✅ Compilation réussie !"
    echo ""
    echo "🚀 Lancement de l'application..."
    
    # Méthode 1: Lancement direct
    if [ -f ".build/debug/MacCleanerPro" ]; then
        echo "📱 Démarrage via binaire compilé..."
        ./.build/debug/MacCleanerPro
    else
        echo "📱 Démarrage via swift run..."
        swift run MacCleanerPro
    fi
else
    echo "❌ Erreur de compilation"
    echo ""
    echo "🔧 Alternatives:"
    echo "1. Ouvrir dans Xcode: open Package.swift"
    echo "2. Vérifier les erreurs: swift build --verbose"
fi