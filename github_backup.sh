#!/bin/bash

# Script de sauvegarde GitHub automatique pour MacCleaner Pro
# Usage: ./github_backup.sh [repo_name] [description]

set -euo pipefail

REPO_NAME="${1:-MacCleaner}"
DESCRIPTION="${2:-Nettoyeur Mac Ultra-Complet et Professionnel avec surveillance temps réel}"
GITHUB_USERNAME="$(git config user.name 2>/dev/null || echo "votre-username")"

echo "🚀 Sauvegarde GitHub MacCleaner Pro"
echo "=================================="
echo "Repo: $REPO_NAME"
echo "Description: $DESCRIPTION"
echo "Username: $GITHUB_USERNAME"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [[ ! -f "mac_cleaner.py" ]]; then
    echo "❌ Erreur: Exécutez ce script depuis le répertoire MacCleaner"
    exit 1
fi

# Vérifier l'état Git
echo "📋 Vérification de l'état Git..."
if [[ -n "$(git status --porcelain)" ]]; then
    echo "⚠️ Il y a des changements non commités:"
    git status --short
    read -p "Voulez-vous continuer? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "🚫 Opération annulée"
        exit 1
    fi
fi

# Préparer les fichiers pour GitHub
echo "📝 Préparation des fichiers GitHub..."

# Copier README pour GitHub si différent
if [[ -f "README_GITHUB.md" ]]; then
    cp README_GITHUB.md README.md.github
    echo "✅ README GitHub préparé"
fi

# Commit des fichiers GitHub si nécessaires
if [[ -n "$(git status --porcelain)" ]]; then
    git add .gitignore LICENSE README_GITHUB.md github_backup.sh
    git commit -m "docs: ajout fichiers GitHub (LICENSE, .gitignore, README)" || true
fi

# Afficher les informations du repo
echo ""
echo "📊 Statistiques du repo:"
echo "- Commits: $(git rev-list --count HEAD)"
echo "- Branches: $(git branch | wc -l | tr -d ' ')"
echo "- Fichiers: $(find . -type f -not -path './.git/*' -not -path './.venv/*' | wc -l | tr -d ' ')"
echo "- Taille: $(du -sh . | cut -f1)"

# Instructions pour créer le repo GitHub
echo ""
echo "🔧 INSTRUCTIONS POUR CRÉER LE REPO GITHUB:"
echo ""
echo "1️⃣ Créer le repo sur GitHub:"
echo "   - Aller sur: https://github.com/new"
echo "   - Nom: $REPO_NAME"
echo "   - Description: $DESCRIPTION"
echo "   - ✅ Public (ou Private selon préférence)"
echo "   - ❌ NE PAS initialiser avec README/LICENSE/gitignore"
echo "   - Cliquer 'Create repository'"
echo ""

echo "2️⃣ Configurer la remote et pousser:"
echo "   git remote add origin git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo "3️⃣ Ou via HTTPS (si pas de clé SSH):"
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git branch -M main" 
echo "   git push -u origin main"
echo ""

# Proposer d'automatiser si GitHub CLI installé
if command -v gh >/dev/null 2>&1; then
    echo "🤖 GitHub CLI détecté! Voulez-vous créer automatiquement?"
    read -p "Créer le repo automatiquement? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Création automatique du repo..."
        
        # Créer le repo
        gh repo create "$REPO_NAME" --description "$DESCRIPTION" --public
        
        # Ajouter remote et pousser
        git remote add origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
        git branch -M main
        git push -u origin main
        
        echo "✅ Repo créé et sauvegardé!"
        echo "🌐 Disponible sur: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        
        # Proposer d'ouvrir dans le navigateur
        read -p "Ouvrir dans le navigateur? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            open "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        fi
        
        exit 0
    fi
fi

echo "📋 COMMANDES À COPIER-COLLER:"
echo ""
echo "# Après avoir créé le repo sur GitHub:"
echo "git remote add origin git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "✨ Votre projet sera alors sauvegardé sur GitHub!"

# Afficher le contenu du README pour vérification
echo ""
echo "📄 Aperçu du README qui sera affiché sur GitHub:"
echo "================================================"
if [[ -f "README_GITHUB.md" ]]; then
    head -20 README_GITHUB.md
    echo "... (fichier complet: README_GITHUB.md)"
else
    head -20 README.md
fi