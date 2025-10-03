import psutil

def can_clean(settings, log_fn):
    batt = getattr(psutil, 'sensors_battery', lambda: None)()
    if batt is None:
        return True
    conf = settings.get('battery', {})
    if conf.get('skip_on_battery', True) and not batt.power_plugged:
        log_fn("🔋 Sur batterie: nettoyage différé")
        return False
    if batt.percent < conf.get('min_percent_clean', 25):
        log_fn(f"🔋 Batterie trop basse ({batt.percent}%) : nettoyage annulé")
        return False
    return True
