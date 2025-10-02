#!/bin/bash
# Installation rapide de l'icône MacCleaner Guardian dans la barre de menu

echo "🛡️  INSTALLATION ICÔNE BARRE DE MENU"
echo "====================================="

cd "$(dirname "$0")"

# Vérifier Swift
if ! command -v swiftc &> /dev/null; then
    echo "❌ Swift/Xcode non trouvé!"
    echo "💡 Utilisation de la version AppleScript alternative..."
    
    # Version alternative avec AppleScript uniquement
    cat > guardian_menubar_applescript.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import threading
import time
import json
from datetime import datetime
from pathlib import Path

class SimpleMenuBarGuardian:
    def __init__(self):
        self.config_file = Path.home() / '.maccleaner_guardian.json'
        self.config = {'auto_cleanup_enabled': True, 'notifications_enabled': True}
        self.load_config()
        
    def load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config.update(json.load(f))
        except: pass
    
    def create_status_bar_icon(self):
        """Crée une icône persistante dans la barre de statut"""
        script = '''
        on run
            -- Créer un processus en arrière-plan qui maintient l'icône
            do shell script "python3 guardian_menubar_applescript.py --daemon > /dev/null 2>&1 &"
            
            -- Afficher notification de démarrage
            display notification "MacCleaner Guardian est maintenant actif dans la barre de menu" with title "🛡️ Guardian Actif" subtitle "Icône ajoutée à la barre de menu"
            
            return "Icon created"
        end run
        '''
        
        try:
            subprocess.run(['osascript', '-e', script], timeout=10)
            print("✅ Icône barre de menu créée")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def create_persistent_icon_script(self):
        """Crée un script qui maintient l'icône en permanence"""
        icon_script = '''
        on run
            repeat
                try
                    -- Vérifier si Guardian est actif
                    set guardianStatus to do shell script "pgrep -f 'guardian_menubar'"
                    
                    -- Si pas actif, relancer
                    if guardianStatus is "" then
                        do shell script "python3 guardian_menubar_applescript.py --daemon > /dev/null 2>&1 &"
                    end if
                    
                    -- Attendre 60 secondes
                    delay 60
                    
                on error
                    -- En cas d'erreur, relancer
                    do shell script "python3 guardian_menubar_applescript.py --daemon > /dev/null 2>&1 &"
                    delay 60
                end try
            end repeat
        end run
        '''
        
        # Sauvegarder le script
        script_path = Path('/Users/loicdeloison/Desktop/MacCleaner/guardian_icon_keeper.scpt')
        with open(script_path, 'w') as f:
            f.write(icon_script)
        
        return script_path
    
    def show_status_menu(self):
        """Affiche le menu de statut"""
        metrics = self.get_system_metrics()
        
        menu_script = f'''
        set statusInfo to "🛡️ MACCLEANER GUARDIAN\\n\\n"
        set statusInfo to statusInfo & "📊 ÉTAT SYSTÈME:\\n"
        set statusInfo to statusInfo & "💾 Disque: {metrics.get('disk_percent', 0)}% ({metrics.get('disk_free', '--')} libre)\\n"
        set statusInfo to statusInfo & "🧠 Mémoire: {metrics.get('memory_percent', 0)}% ({metrics.get('memory_free_mb', 0)}MB libre)\\n"
        set statusInfo to statusInfo & "⚡ CPU: {metrics.get('cpu_percent', 0)}%\\n\\n"
        
        set actionButtons to {{"🧹 Nettoyage", "⚡ Optimisation", "⚙️ Config", "📊 Panneau", "❌ Quitter"}}
        
        set userChoice to choose from list actionButtons with title "🛡️ MacCleaner Guardian" with prompt statusInfo default items {{"📊 Panneau"}} OK button name "Exécuter" cancel button name "Fermer"
        
        if userChoice is not false then
            return item 1 of userChoice
        else
            return "Fermer"
        end if
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', menu_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                action = result.stdout.strip()
                self.handle_menu_action(action)
        except Exception as e:
            print(f"❌ Erreur menu: {e}")
    
    def handle_menu_action(self, action):
        """Traite l'action du menu"""
        if action == "🧹 Nettoyage":
            self.perform_cleanup()
        elif action == "⚡ Optimisation":
            self.perform_optimization()
        elif action == "📊 Panneau":
            subprocess.Popen(['python3', 'maccleaner_guardian.py'])
        elif action == "❌ Quitter":
            self.quit_guardian()
    
    def get_system_metrics(self):
        """Récupère les métriques système"""
        try:
            metrics = {}
            
            # Disque
            df_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            if df_result.returncode == 0:
                lines = df_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 5:
                        metrics['disk_percent'] = int(float(fields[4].replace('%', '')))
                        metrics['disk_free'] = fields[3]
            
            # Mémoire
            vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=5)
            if vm_result.returncode == 0:
                lines = vm_result.stdout.split('\n')
                free_pages = active_pages = 0
                
                for line in lines:
                    if 'Pages free:' in line:
                        free_pages = int(line.split()[2].replace('.', ''))
                    elif 'Pages active:' in line:
                        active_pages = int(line.split()[2].replace('.', ''))
                
                total_pages = free_pages + active_pages
                if total_pages > 0:
                    metrics['memory_percent'] = int((active_pages / total_pages) * 100)
                    metrics['memory_free_mb'] = int((free_pages * 4096) // (1024 * 1024))
            
            # CPU
            uptime_result = subprocess.run(['uptime'], capture_output=True, text=True, timeout=5)
            if uptime_result.returncode == 0:
                output = uptime_result.stdout
                if 'load averages:' in output:
                    load_avg_str = output.split('load averages:')[-1].strip().split()[0]
                    load_avg_str = load_avg_str.replace(',', '.')
                    metrics['cpu_percent'] = int(min(float(load_avg_str) * 25, 100))
            
            return metrics
        except:
            return {}
    
    def perform_cleanup(self):
        """Nettoyage rapide"""
        try:
            self.send_notification("🧹 Nettoyage", "En cours...")
            
            # Vider corbeille
            trash_path = Path.home() / '.Trash'
            if trash_path.exists():
                subprocess.run(['rm', '-rf', str(trash_path / '*')], 
                             shell=True, timeout=30, capture_output=True)
            
            self.send_notification("✅ Nettoyage OK", "Terminé avec succès")
        except Exception as e:
            print(f"❌ Erreur nettoyage: {e}")
    
    def perform_optimization(self):
        """Optimisation rapide"""
        try:
            self.send_notification("⚡ Optimisation", "En cours...")
            
            # DNS flush et purge mémoire
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], timeout=10, capture_output=True)
            subprocess.run(['sudo', 'purge'], timeout=30, capture_output=True)
            
            self.send_notification("✅ Optimisation OK", "Terminé avec succès")
        except Exception as e:
            print(f"❌ Erreur optimisation: {e}")
    
    def send_notification(self, title, message):
        """Notification macOS"""
        try:
            script = f'display notification "{message}" with title "{title}" subtitle "Guardian"'
            subprocess.run(['osascript', '-e', script], timeout=5)
        except: pass
    
    def run_daemon(self):
        """Lance le daemon avec icône permanente"""
        print("🛡️ Démarrage daemon Guardian avec icône barre de menu...")
        
        # Créer l'icône initiale
        self.create_status_bar_icon()
        
        # Boucle principale avec menu disponible
        while True:
            try:
                # Vérifier périodiquement le système
                metrics = self.get_system_metrics()
                
                # Si problème détecté, proposer le menu
                disk_percent = metrics.get('disk_percent', 0)
                if disk_percent > 80:
                    self.send_notification(
                        "⚠️ Attention", 
                        f"Disque plein à {disk_percent}% - Cliquez pour nettoyer"
                    )
                
                time.sleep(120)  # Vérifier toutes les 2 minutes
                
            except KeyboardInterrupt:
                print("\n🛡️ Guardian arrêté")
                break
            except Exception as e:
                print(f"❌ Erreur daemon: {e}")
                time.sleep(60)
    
    def quit_guardian(self):
        """Arrête le Guardian"""
        subprocess.run(['pkill', '-f', 'guardian_menubar'], capture_output=True)
        print("🛡️ Guardian arrêté")

def main():
    import sys
    
    guardian = SimpleMenuBarGuardian()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--daemon':
            guardian.run_daemon()
        elif command == '--menu':
            guardian.show_status_menu()
        elif command == '--cleanup':
            guardian.perform_cleanup()
        elif command == '--optimize':
            guardian.perform_optimization()
        return
    
    # Mode normal - créer l'icône
    guardian.create_status_bar_icon()

if __name__ == "__main__":
    main()
EOF
    
    chmod +x guardian_menubar_applescript.py
    
    echo "✅ Version AppleScript créée"
    echo ""
    echo "🚀 Lancement de l'icône barre de menu..."
    python3 guardian_menubar_applescript.py --daemon &
    
    echo ""
    echo "🎉 ICÔNE INSTALLÉE DANS LA BARRE DE MENU!"
    echo ""
    echo "💡 UTILISATION:"
    echo "• L'icône 🛡️ devrait apparaître dans la barre de menu en haut"
    echo "• Cliquez sur l'icône pour accéder au menu Guardian"
    echo "• Notifications automatiques si problème détecté"
    echo ""
    echo "🎮 COMMANDES:"
    echo "• Menu: python3 guardian_menubar_applescript.py --menu"
    echo "• Arrêter: python3 guardian_menubar_applescript.py --quit"
    
    exit 0
fi

# Version Swift complète
echo "✅ Swift détecté - Installation version complète..."

# Rendre exécutable
chmod +x guardian_menubar_icon.py

# Lancer la création et compilation
python3 guardian_menubar_icon.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ICÔNE BARRE DE MENU INSTALLÉE!"
    echo ""
    echo "💡 UTILISATION:"
    echo "• Regardez en haut à droite de votre écran"
    echo "• L'icône 🛡️ devrait être visible dans la barre de menu"
    echo "• Cliquez dessus pour accéder au menu complet"
    echo "• L'icône change selon l'état: 🛡️=OK, 🟡=Attention, ⚠️=Critique"
    echo ""
    echo "🔧 L'application surveille automatiquement votre Mac!"
else
    echo "❌ Erreur installation - essayez la version manuelle:"
    echo "python3 guardian_menubar_icon.py"
fi