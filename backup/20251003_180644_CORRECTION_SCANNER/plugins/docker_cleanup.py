import subprocess, shutil, json, re

def _docker_disk_usage():
    try:
        proc = subprocess.run(['docker', 'system', 'df', '-v', '--format', 'json'], capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            return None
        # Format json pas toujours dispo sur anciennes versions; fallback parsing texte
        try:
            data = json.loads(proc.stdout)
            # Somme images + containers + volumes reclaimable
            reclaim = 0
            for section in data:
                reclaim += section.get('ReclaimableSize', 0)
            return reclaim
        except Exception:
            # Parsing texte
            text = proc.stdout
            match = re.search(r'Reclaimable:\s*([0-9\.]+)\s*([kMG]B)', text, re.IGNORECASE)
            if match:
                val = float(match.group(1))
                unit = match.group(2).upper()
                mult = {'KB':1024,'MB':1024**2,'GB':1024**3}.get(unit,1)
                return int(val*mult)
    except Exception:
        return None
    return None

def run(log):
    if not shutil.which('docker'):
        log('🐳 Docker non installé ou non dans PATH - plugin ignoré')
        return 0
    before = _docker_disk_usage() or 0
    try:
        prune = subprocess.run(['docker', 'system', 'prune', '-af', '--volumes'], capture_output=True, text=True, timeout=300)
        if prune.returncode == 0:
            log('🐳 docker system prune exécuté')
        else:
            log(f'⚠️ docker prune code={prune.returncode}')
    except Exception as e:
        log(f'❌ Erreur docker prune: {e}')
        return 0
    after = _docker_disk_usage() or 0
    freed = max(0, before - after)
    if freed:
        log(f'✅ Docker cleanup: {(freed/1024/1024):.1f} MB potentiellement récupérés')
    else:
        log('ℹ️ Docker cleanup terminé (aucun gain détecté)')
    return freed
