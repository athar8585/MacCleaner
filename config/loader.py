import json
import os
from pathlib import Path

_SETTINGS_CACHE = None
_DEFAULT_SETTINGS = {
    "version": "3.0.0",
    "ui": {"accent_color": "#007AFF", "theme": "auto", "ios26_style": True, "animations": True},
    "scheduler": {"enabled": True, "auto_clean_enabled": False, "smart_scheduling": True, "interval_minutes": 30},
    "thresholds": {"disk_space_alert": 10, "memory_alert": 85, "cache_size_alert": 5000},
    "malware_scanner": {"enabled": True, "auto_update_database": True, "database_path": "database/malware_signatures.json"},
    "database": {"enabled": True, "path": "database/mac_cleaner.db", "track_cleanings": True},
}

SETTINGS_PATHS = [
    Path(__file__).parent / 'settings.json',
    Path.cwd() / 'config' / 'settings.json'
]

def load_settings(force=False):
    global _SETTINGS_CACHE
    if _SETTINGS_CACHE is not None and not force:
        return _SETTINGS_CACHE
    for p in SETTINGS_PATHS:
        if p.exists():
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                _SETTINGS_CACHE = merge_dict(_DEFAULT_SETTINGS, data)
                return _SETTINGS_CACHE
            except Exception:
                continue
    _SETTINGS_CACHE = _DEFAULT_SETTINGS
    return _SETTINGS_CACHE

def merge_dict(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict):
            result[k] = merge_dict(result[k], v)
        else:
            result[k] = v
    return result

def save_settings(settings=None):
    settings = settings or _SETTINGS_CACHE or _DEFAULT_SETTINGS
    target = SETTINGS_PATHS[0]
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)
    return target
