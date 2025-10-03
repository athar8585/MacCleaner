import subprocess, shlex, platform

#!/usr/bin/env python3
"""
Notifications macOS améliorées pour MacCleaner Pro
Support osascript + pync pour notifications robustes
"""

import subprocess
import os

# Tenter d'importer pync pour notifications améliorées
try:
    import pync
    PYNC_AVAILABLE = True
except ImportError:
    PYNC_AVAILABLE = False

def notify(title, message, subtitle=None, sound=True, urgency='normal'):
    """
    Envoyer une notification macOS
    
    Args:
        title: Titre de la notification
        message: Message principal
        subtitle: Sous-titre optionnel
        sound: Jouer un son (True/False)
        urgency: 'low', 'normal', 'critical'
    """
    
    # Essayer pync d'abord si disponible
    if PYNC_AVAILABLE:
        try:
            return _notify_pync(title, message, subtitle, sound, urgency)
        except Exception as e:
            print(f"❌ Erreur pync: {e}, fallback osascript")
    
    # Fallback vers osascript
    return _notify_osascript(title, message, subtitle, sound)

def _notify_pync(title, message, subtitle=None, sound=True, urgency='normal'):
    """Notification via pync (bibliothèque Python)"""
    options = {
        'title': title,
        'subtitle': subtitle or '',
        'message': message,
        'sound': 'default' if sound else None,
        'appIcon': None,  # Utiliser icône par défaut
    }
    
    # Mapper urgence vers pync
    if urgency == 'critical':
        options['sound'] = 'Basso'  # Son plus fort
    elif urgency == 'low':
        options['sound'] = None  # Pas de son
    
    return pync.notify(**{k: v for k, v in options.items() if v is not None})

def _notify_osascript(title, message, subtitle=None, sound=True):
    """Notification via osascript (fallback)"""
    try:
        # Construire la commande osascript
        script_parts = [
            'display notification',
            f'"{message}"',
            f'with title "{title}"'
        ]
        
        if subtitle:
            script_parts.append(f'subtitle "{subtitle}"')
        
        if sound:
            script_parts.append('sound name "default"')
        
        script = ' '.join(script_parts)
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Erreur osascript: {e}")
        return False

def notify_progress(title, message, progress_value=None, total=None):
    """
    Notification de progression
    
    Args:
        title: Titre
        message: Message
        progress_value: Valeur actuelle (optionnel)
        total: Valeur maximale (optionnel)
    """
    if progress_value is not None and total is not None:
        percentage = int((progress_value / total) * 100)
        progress_msg = f"{message} ({percentage}%)"
    else:
        progress_msg = message
    
    return notify(title, progress_msg, sound=False, urgency='low')

def notify_completion(title, message, stats=None, sound=True):
    """
    Notification de fin de tâche avec statistiques
    
    Args:
        title: Titre
        message: Message principal
        stats: Dictionnaire de statistiques optionnel
        sound: Jouer son de succès
    """
    if stats:
        # Formater les stats pour le message
        stats_text = []
        if 'freed_mb' in stats:
            stats_text.append(f"{stats['freed_mb']:.1f} MB libérés")
        if 'files_cleaned' in stats:
            stats_text.append(f"{stats['files_cleaned']} fichiers")
        if 'duration' in stats:
            stats_text.append(f"{stats['duration']:.1f}s")
        
        if stats_text:
            subtitle = " • ".join(stats_text)
        else:
            subtitle = None
    else:
        subtitle = None
    
    return notify(title, message, subtitle=subtitle, sound=sound, urgency='normal')

def notify_alert(title, message, alert_type='warning'):
    """
    Notification d'alerte ou d'erreur
    
    Args:
        title: Titre
        message: Message d'alerte
        alert_type: 'warning', 'error', 'critical'
    """
    sound_map = {
        'warning': True,
        'error': True,
        'critical': True
    }
    
    urgency_map = {
        'warning': 'normal',
        'error': 'normal', 
        'critical': 'critical'
    }
    
    # Préfixer le message selon le type
    prefixes = {
        'warning': '⚠️ ',
        'error': '❌ ',
        'critical': '🚨 '
    }
    
    prefixed_message = prefixes.get(alert_type, '') + message
    
    return notify(
        title, 
        prefixed_message, 
        sound=sound_map.get(alert_type, True),
        urgency=urgency_map.get(alert_type, 'normal')
    )

def test_notifications():
    """Tester les différents types de notifications"""
    print("🧪 Test des notifications...")
    
    # Test notification simple
    notify("MacCleaner Pro", "Test notification simple")
    
    # Test avec sous-titre
    notify("MacCleaner Pro", "Test avec sous-titre", subtitle="Sous-titre de test")
    
    # Test progression
    notify_progress("Nettoyage", "Fichiers temporaires", 45, 100)
    
    # Test complétion
    stats = {'freed_mb': 234.5, 'files_cleaned': 1234, 'duration': 15.2}
    notify_completion("Nettoyage terminé", "Nettoyage réussi", stats=stats)
    
    # Test alerte
    notify_alert("Attention", "Fichier suspect détecté", alert_type='warning')
    
    print("✅ Tests notifications terminés")

if __name__ == "__main__":
    test_notifications()
