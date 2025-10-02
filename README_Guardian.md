# MacCleaner Guardian - Version Stable

## 🛡️ Description
Guardian Stable est une version contrôlée et fiable de MacCleaner Guardian qui évite les notifications intempestives et les processus multiples incontrôlés.

## 📋 Fonctionnalités
- ✅ Surveillance discrète du système (disque et mémoire)
- ✅ Notifications contrôlées (maximum une toutes les 5 minutes)
- ✅ Nettoyage automatique des fichiers temporaires
- ✅ Protection contre les doublons de processus
- ✅ Arrêt propre avec gestion des signaux
- ✅ Interface menu conviviale

## 🚀 Utilisation

### Lancement rapide et sécurisé
```bash
./launch_guardian.sh
```
Ce script vous propose 3 options :
1. **Mode daemon** : Lance Guardian en arrière-plan
2. **Mode interactif** : Ouvre le menu de contrôle
3. **Vérification statut** : Affiche l'état actuel

### Commandes directes
```bash
# Démarrer en arrière-plan
python3 guardian_stable.py --daemon

# Vérifier le statut
python3 guardian_stable.py --status

# Arrêter Guardian
python3 guardian_stable.py --stop

# Ouvrir le menu
python3 guardian_stable.py --menu
# ou plus simplement :
./menu.sh
```

### En cas de problème (processus bloqués)
```bash
./emergency_cleanup.sh
```

## 🔧 Paramètres de surveillance
- **Disque** : Alerte si utilisation > 90%
- **Mémoire** : Alerte si utilisation > 85%
- **Notifications** : Maximum une toutes les 5 minutes
- **Vérification** : Toutes les minutes

## 📊 Menu interactif
1. **Démarrer la surveillance** - Lance Guardian si pas déjà actif
2. **Arrêter la surveillance** - Arrête Guardian proprement
3. **Statut du système** - Affiche métriques actuelles
4. **Nettoyage manuel** - Lance un nettoyage immédiat
5. **Quitter** - Ferme le menu

## 🛑 Sécurités intégrées
- **Fichier PID** : Empêche les lancements multiples
- **Cooldown notifications** : Évite le spam de notifications
- **Gestion signaux** : Arrêt propre avec Ctrl+C
- **Nettoyage automatique** : Supprime les fichiers PID obsolètes

## 🔍 Surveillance
Guardian surveille en permanence :
- **Espace disque** : Alerte et nettoyage automatique si nécessaire
- **Utilisation mémoire** : Alerte si seuil dépassé
- **Fichiers temporaires** : Suppression automatique (fichiers > 7 jours)

## 💡 Conseils d'utilisation
- Utilisez `./launch_guardian.sh` pour un démarrage sûr
- Le menu (`./menu.sh`) permet un contrôle facile
- En cas de problème, utilisez `./emergency_cleanup.sh`
- Guardian ne génère qu'une notification par situation critique

## 🆘 Dépannage
Si vous voyez encore des notifications intempestives :
1. Lancez `./emergency_cleanup.sh`
2. Attendez quelques secondes
3. Relancez avec `./launch_guardian.sh`

Guardian Stable est conçu pour être discret et efficace, sans perturbation de votre travail !