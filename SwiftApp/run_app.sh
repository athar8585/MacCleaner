#!/bin/bash
echo "🚀 Lancement MacCleaner Pro (Swift)"
echo "==================================="

if ! command -v swift &> /dev/null; then
    echo "❌ Swift n'est pas installé"
    echo "📱 Installer Xcode Command Line Tools:"
    echo "   xcode-select --install"
    exit 1
fi

echo "✅ Swift détecté"
echo "🚀 Compilation et lancement..."

swift MacCleanerApp.swift
