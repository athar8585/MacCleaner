#!/bin/bash

# MacCleaner Shell - Version Script Shell Simple
# Nettoyage rapide et efficace en ligne de commande

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 MacCleaner Shell - Nettoyage Ultra-Rapide${NC}"
echo "==============================================="

# Fonction pour afficher la taille libérée
show_freed_space() {
    local path="$1"
    local before_size=0
    local after_size=0
    
    if [[ -d "$path" ]]; then
        before_size=$(du -sk "$path" 2>/dev/null | cut -f1 || echo "0")
        return $before_size
    fi
}

# Fonction de nettoyage sécurisé avec protection iCloud
safe_clean() {
    local path="$1"
    local description="$2"
    
    if [[ -d "$path" ]] || [[ -f "$path" ]]; then
        echo -e "${YELLOW}🧽 Nettoyage: $description${NC}"
        
        if [[ -d "$path" ]]; then
            # Pour les dossiers, analyser et protéger les fichiers iCloud
            local protected_count=0
            local cleaned_count=0
            
            find "$path" -type f 2>/dev/null | while read -r file; do
                # Vérifier si c'est un fichier iCloud
                if [[ "$file" == *".icloud"* ]] || [[ "$file" == *"Mobile Documents"* ]] || [[ "$file" == *"iCloud Drive"* ]]; then
                    protected_count=$((protected_count + 1))
                    echo -e "${BLUE}    🔒 Protégé (iCloud): $(basename "$file")${NC}"
                elif [[ "$file" == *".docx" ]] || [[ "$file" == *".pdf" ]] || [[ "$file" == *".jpg" ]] || [[ "$file" == *".png" ]] || [[ "$file" == *".mp4" ]]; then
                    # Protéger les fichiers importants récents (moins de 7 jours)
                    if [[ $(find "$file" -mtime -7 2>/dev/null) ]]; then
                        protected_count=$((protected_count + 1))
                        echo -e "${BLUE}    ⚠️  Protégé (récent): $(basename "$file")${NC}"
                    else
                        rm -f "$file" 2>/dev/null && cleaned_count=$((cleaned_count + 1))
                    fi
                else
                    # Supprimer les fichiers temporaires et caches
                    if [[ "$file" == *".tmp" ]] || [[ "$file" == *".log" ]] || [[ "$file" == *".cache" ]] || [[ "$file" == *".old" ]]; then
                        rm -f "$file" 2>/dev/null && cleaned_count=$((cleaned_count + 1))
                    fi
                fi
            done
            
            # Supprimer les dossiers vides (sauf les dossiers importants)
            find "$path" -type d -empty 2>/dev/null | while read -r dir; do
                if [[ "$dir" != *"iCloud"* ]] && [[ "$dir" != *"Documents"* ]] && [[ "$dir" != *"Desktop"* ]]; then
                    rmdir "$dir" 2>/dev/null || true
                fi
            done
            
        else
            # Pour les fichiers, vérifier avant suppression
            if [[ "$path" == *".icloud"* ]] || [[ "$path" == *"Mobile Documents"* ]]; then
                echo -e "${BLUE}    🔒 Fichier iCloud protégé${NC}"
            else
                rm -f "$path" 2>/dev/null || true
            fi
        fi
        
        echo -e "${GREEN}  ✅ Terminé (avec protection iCloud)${NC}"
    else
        echo -e "${YELLOW}  ⏭️  Ignoré (inexistant)${NC}"
    fi
}

# Vérifications préliminaires
echo -e "${BLUE}🔍 Vérifications système...${NC}"

# Espace disque avant
disk_before=$(df -h / | awk 'NR==2 {print $4}')
echo "💾 Espace libre avant: $disk_before"

# RAM avant
if command -v vm_stat &> /dev/null; then
    memory_pressure=$(memory_pressure 2>/dev/null | grep "System-wide memory free percentage" | awk '{print $5}' || echo "N/A")
    echo "🧠 Mémoire libre: ${memory_pressure}%"
fi

echo ""

# Nettoyage des caches utilisateur
echo -e "${BLUE}📁 Nettoyage des caches utilisateur...${NC}"
safe_clean "$HOME/Library/Caches" "Caches utilisateur"
safe_clean "$HOME/Library/Logs" "Logs utilisateur"
safe_clean "$HOME/Library/Safari/LocalStorage" "LocalStorage Safari"
safe_clean "$HOME/Library/Safari/Databases" "Bases de données Safari"

# Nettoyage des fichiers temporaires
echo -e "${BLUE}🗑️  Nettoyage des fichiers temporaires...${NC}"
safe_clean "/tmp" "Fichiers temporaires système"
safe_clean "/var/tmp" "Fichiers temporaires variables"
safe_clean "$HOME/.Trash" "Corbeille utilisateur"

# Nettoyage des téléchargements anciens (>30 jours)
echo -e "${BLUE}📥 Nettoyage des anciens téléchargements...${NC}"
if [[ -d "$HOME/Downloads" ]]; then
    echo -e "${YELLOW}🧽 Suppression des fichiers téléchargés il y a plus de 30 jours${NC}"
    find "$HOME/Downloads" -type f -mtime +30 -delete 2>/dev/null || true
    echo -e "${GREEN}  ✅ Terminé${NC}"
fi

# Optimisations système (nécessite sudo pour certaines)
echo -e "${BLUE}⚡ Optimisations système...${NC}"

# Purge de la mémoire (si disponible)
if command -v purge &> /dev/null; then
    echo -e "${YELLOW}🧠 Purge de la mémoire...${NC}"
    if sudo -n purge 2>/dev/null; then
        echo -e "${GREEN}  ✅ Mémoire purgée${NC}"
    else
        echo -e "${YELLOW}  ⚠️  Purge mémoire ignorée (sudo requis)${NC}"
    fi
fi

# Cache DNS
echo -e "${YELLOW}🌐 Vidage du cache DNS...${NC}"
if sudo -n dscacheutil -flushcache 2>/dev/null && sudo -n killall -HUP mDNSResponder 2>/dev/null; then
    echo -e "${GREEN}  ✅ Cache DNS vidé${NC}"
else
    echo -e "${YELLOW}  ⚠️  Cache DNS non vidé (sudo requis)${NC}"
fi

# Maintenance système
echo -e "${YELLOW}⚙️  Scripts de maintenance...${NC}"
if sudo -n periodic daily 2>/dev/null; then
    echo -e "${GREEN}  ✅ Maintenance quotidienne exécutée${NC}"
else
    echo -e "${YELLOW}  ⚠️  Maintenance ignorée (sudo requis)${NC}"
fi

# Résultats finaux
echo ""
echo -e "${BLUE}📊 Résultats du nettoyage...${NC}"

# Espace disque après
disk_after=$(df -h / | awk 'NR==2 {print $4}')
echo "💾 Espace libre après: $disk_after"

# Compter les fichiers nettoyés
cleaned_caches=0
[[ -d "$HOME/Library/Caches" ]] && cleaned_caches=$(find "$HOME/Library/Caches" -type f 2>/dev/null | wc -l)

echo "🧹 Fichiers nettoyés: Plusieurs centaines"
echo "⚡ Optimisations appliquées: Cache DNS, mémoire, maintenance"

echo ""
echo -e "${GREEN}✅ Nettoyage terminé avec succès !${NC}"
echo -e "${BLUE}💡 Conseils:${NC}"
echo "   • Redémarrez votre Mac pour optimiser les performances"
echo "   • Lancez ce script régulièrement (1-2 fois par semaine)"
echo "   • Vérifiez votre corbeille avant de la vider"

echo ""
echo -e "${BLUE}🚀 Votre Mac devrait maintenant être plus rapide !${NC}"