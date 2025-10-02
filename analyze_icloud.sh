#!/bin/bash

# MacCleaner Pro - Analyseur iCloud
# Analyse et détection des fichiers synchronisés avec iCloud

# Couleurs
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}☁️ MacCleaner Pro - Analyseur iCloud${NC}"
echo "============================================"
echo ""

# Fonction d'analyse iCloud
analyze_icloud_directory() {
    local dir="$1"
    local dir_name="$2"
    
    if [[ ! -d "$dir" ]]; then
        echo -e "${YELLOW}⚠️  Répertoire $dir_name non trouvé${NC}"
        return
    fi
    
    echo -e "${BLUE}📁 Analyse: $dir_name${NC}"
    
    local total_files=0
    local icloud_files=0
    local total_size=0
    local icloud_size=0
    
    # Analyser les fichiers
    local count=0
    while IFS= read -r -d '' file; do
        total_files=$((total_files + 1))
        count=$((count + 1))
        
        # Calculer la taille
        if [[ -f "$file" ]]; then
            local size=$(stat -f%z "$file" 2>/dev/null || echo "0")
            total_size=$((total_size + size))
            
            # Détecter les fichiers iCloud
            if [[ "$file" == *".icloud"* ]] || [[ "$file" == *"Mobile Documents"* ]] || [[ "$file" == *"com~apple~CloudDocs"* ]]; then
                icloud_files=$((icloud_files + 1))
                icloud_size=$((icloud_size + size))
                echo -e "${GREEN}  ☁️  $(basename "$file")${NC}"
            elif xattr "$file" 2>/dev/null | grep -q "com.apple.clouddocs"; then
                icloud_files=$((icloud_files + 1))
                icloud_size=$((icloud_size + size))
                echo -e "${GREEN}  ☁️  $(basename "$file") (attribut iCloud)${NC}"
            fi
        fi
        
        # Limiter l'affichage pour éviter le spam
        if [[ $count -gt 50 ]]; then
            echo -e "${YELLOW}  ... (affichage limité à 50 fichiers)${NC}"
            break
        fi
        
    done < <(find "$dir" -type f -print0 2>/dev/null)
    
    # Afficher les statistiques
    local total_mb=$((total_size / 1024 / 1024))
    local icloud_mb=$((icloud_size / 1024 / 1024))
    
    echo -e "${YELLOW}  📊 Fichiers total: $total_files${NC}"
    echo -e "${YELLOW}  📊 Fichiers iCloud: $icloud_files${NC}"
    echo -e "${YELLOW}  📊 Taille totale: ${total_mb}MB${NC}"
    echo -e "${YELLOW}  📊 Taille iCloud: ${icloud_mb}MB${NC}"
    echo ""
}

# Analyser les répertoires principaux
echo -e "${BLUE}🔍 Recherche des fichiers iCloud...${NC}"
echo ""

analyze_icloud_directory "$HOME/Documents" "Documents"
analyze_icloud_directory "$HOME/Desktop" "Bureau"
analyze_icloud_directory "$HOME/Library/Mobile Documents" "iCloud Drive"
analyze_icloud_directory "$HOME/iCloud Drive" "iCloud Drive (alias)"

# Vérifier les paramètres iCloud
echo -e "${BLUE}⚙️  Paramètres iCloud système...${NC}"

# Vérifier si iCloud Drive est activé
if [[ -d "$HOME/Library/Mobile Documents" ]]; then
    echo -e "${GREEN}✅ iCloud Drive activé${NC}"
    
    # Compter les dossiers d'applications
    app_folders=$(find "$HOME/Library/Mobile Documents" -maxdepth 1 -type d -name "com~apple~*" 2>/dev/null | wc -l)
    echo -e "${YELLOW}📱 Applications synchronisées: $app_folders${NC}"
else
    echo -e "${RED}❌ iCloud Drive non détecté${NC}"
fi

# Vérifier l'espace iCloud
echo ""
echo -e "${BLUE}💾 Espace de stockage...${NC}"

# Utiliser la commande système pour obtenir l'info iCloud si disponible
if command -v brctl &> /dev/null; then
    echo -e "${YELLOW}📊 Utilisation iCloud:${NC}"
    brctl diagnosis 2>/dev/null | grep -E "(iCloud|Storage)" || echo "  Information non disponible"
fi

echo ""
echo -e "${BLUE}💡 Recommandations:${NC}"
echo "• Les fichiers iCloud détectés seront automatiquement protégés lors du nettoyage"
echo "• Utilisez l'option '🔒 Protéger les fichiers iCloud' dans MacCleaner Pro"
echo "• Les fichiers .icloud sont des liens vers le cloud - ne pas supprimer"
echo "• Vérifiez régulièrement votre espace de stockage iCloud"

echo ""
echo -e "${GREEN}✅ Analyse iCloud terminée${NC}"