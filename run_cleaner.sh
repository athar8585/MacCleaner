#!/bin/bash

# MacCleaner Pro - Script de lancement
# Ce script configure l'environnement et lance l'application

echo "🧹 MacCleaner Pro - Initialisation..."

# Aller dans le répertoire du script
cd "$(dirname "$0")"

# Vérifier Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé. Installation requise."
    echo "Installer avec: brew install python3"
    exit 1
fi

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances si nécessaire
if ! python -c "import psutil" &> /dev/null; then
    echo "📦 Installation des dépendances..."
    pip install psutil
fi

# Créer le répertoire de sauvegarde
mkdir -p ~/Desktop/MacCleaner_Backup

# Lancer l'application
echo "🚀 Lancement de MacCleaner Pro..."
python mac_cleaner.py

echo "👋 MacCleaner Pro terminé."