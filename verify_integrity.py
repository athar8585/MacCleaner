#!/usr/bin/env python3
"""
Script de vérification d'intégrité pour MacCleaner Pro
Usage: python3 verify_integrity.py
"""

from utils.integrity import verify_paths

def main():
    print("🔍 Vérification d'intégrité MacCleaner Pro")
    print("=" * 50)
    
    critical_files = [
        'mac_cleaner.py',
        'config/settings.json',
        'malware_scanner/signatures_min.json',
        'plugins/plugin_loader.py',
        'plugins/docker_cleanup.py',
        'plugins/homebrew_cleanup.py',
        'plugins/xcode_cleanup.py',
        'plugins/node_modules_cleanup.py',
        'utils/updater.py',
        'utils/notifications.py',
        'utils/launchagent.py',
        'utils/battery.py',
        'utils/reports.py',
        'utils/pdf_export.py',
        'utils/integrity.py',
        'scheduler/auto_runner.py',
        'database/db.py',
        'ui/theme.py',
        'config/loader.py'
    ]
    
    results = verify_paths(critical_files)
    
    print(f"Vérification de {len(critical_files)} fichiers critiques:")
    print()
    
    ok_count = 0
    altered_count = 0
    
    for r in results:
        status = '✅ OK' if r['ok'] else '⚠️ ALTÉRÉ'
        print(f"{status} {r['path']}")
        if r['ok']:
            ok_count += 1
        else:
            altered_count += 1
    
    print()
    print(f"Résumé: {ok_count} OK, {altered_count} altérés")
    
    if altered_count == 0:
        print('✅ Intégrité globale: OK')
        return 0
    else:
        print('⚠️ Des fichiers semblent modifiés (comparez avec le dépôt source).')
        return 1

if __name__ == "__main__":
    exit(main())