
        on run
            -- Configuration
            set guardianIcon to "🛡️"
            set guardianTitle to "MacCleaner Guardian"
            
            -- Créer un processus en arrière-plan permanent
            tell application "System Events"
                -- Lancer le processus Guardian en arrière-plan
                do shell script "cd /Users/loicdeloison/Desktop/MacCleaner && python3 quick_menubar_icon.py --daemon > /dev/null 2>&1 &"
            end tell
            
            -- Notification de démarrage
            display notification "Guardian est maintenant actif dans la barre de menu" with title guardianTitle subtitle "Icône 🛡️ ajoutée" sound name "Funk"
            
            -- Attendre un peu puis afficher le menu initial
            delay 2
            
            -- Menu de confirmation
            display dialog "🛡️ MacCleaner Guardian est maintenant actif !\n\nL'icône 🛡️ a été ajoutée à la barre de menu.\n\nFonctionnalités:\n• Surveillance automatique du système\n• Nettoyage intelligent\n• Notifications d'alerte\n• Menu accessible via l'icône\n\nLe Guardian fonctionne maintenant en arrière-plan." buttons {"📊 Ouvrir Panneau", "✅ OK"} default button "✅ OK" with title "Guardian Actif" with icon note
            
            set userChoice to button returned of result
            
            if userChoice is "📊 Ouvrir Panneau" then
                do shell script "cd /Users/loicdeloison/Desktop/MacCleaner && python3 maccleaner_guardian.py > /dev/null 2>&1 &"
            end if
            
            return "Guardian started successfully"
        end run
        