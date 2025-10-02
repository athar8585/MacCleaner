#!/bin/bash
# Script d'installation pour MacCleaner Pro
# Installe l'application et ses dépendances

# Configuration
APP_NAME="MacCleaner Pro"
INSTALL_DIR="$HOME/Applications/MacCleanerPro"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installation de $APP_NAME"
echo "=================================="

# Vérifier Python 3
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis mais non installé"
    echo "📦 Installez Python 3 depuis python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION détecté"

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 requis mais non installé"
    exit 1
fi

# Créer le répertoire d'installation
echo "📁 Création du répertoire d'installation..."
mkdir -p "$INSTALL_DIR"

# Copier les fichiers
echo "📋 Copie des fichiers de l'application..."
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Installation des dépendances Python
echo "📦 Installation des dépendances..."
cd "$INSTALL_DIR"

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le script de lancement
echo "🔗 Création du lanceur..."
cat > "$INSTALL_DIR/run.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 launch.py
EOF

chmod +x "$INSTALL_DIR/run.sh"

# Créer l'alias dans le terminal
echo "⚙️ Configuration du terminal..."
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]]; then
    if ! grep -q "alias maccleaner" "$SHELL_RC" 2>/dev/null; then
        echo "alias maccleaner='$INSTALL_DIR/run.sh'" >> "$SHELL_RC"
        echo "✅ Alias 'maccleaner' ajouté à $SHELL_RC"
    fi
fi

# Créer le raccourci Applications (optionnel)
echo "🖥️ Création du raccourci Applications..."
cat > "$INSTALL_DIR/MacCleanerPro.command" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source venv/bin/activate
python3 launch.py
EOF

chmod +x "$INSTALL_DIR/MacCleanerPro.command"

# Instructions finales
echo ""
echo "🎉 Installation terminée avec succès!"
echo "=================================="
echo "📍 Emplacement: $INSTALL_DIR"
echo ""
echo "🚀 Pour lancer l'application:"
echo "   • Terminal: maccleaner"
echo "   • Ou double-clic sur: $INSTALL_DIR/MacCleanerPro.command"
echo ""
echo "📝 Pour désinstaller:"
echo "   rm -rf '$INSTALL_DIR'"
echo ""
echo "🔄 Redémarrez votre terminal pour utiliser 'maccleaner'" 