import subprocess, os, pathlib, shutil

CANDIDATE_PATHS = [
    pathlib.Path('~/Library/Caches/Homebrew').expanduser(),
    pathlib.Path('/usr/local/Caches'),
    pathlib.Path('/opt/homebrew/Caches'),
]

def dir_size(p: pathlib.Path):
    total = 0
    if not p.exists():
        return 0
    for root, dirs, files in os.walk(p):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
    return total


def run(log):
    before = 0
    for p in CANDIDATE_PATHS:
        before += dir_size(p)
    # Lancer brew cleanup si brew installé
    if shutil.which('brew'):
        try:
            proc = subprocess.run(['brew', 'cleanup', '-s'], capture_output=True, text=True, timeout=300)
            if proc.returncode == 0:
                log('🍺 brew cleanup exécuté')
            else:
                log(f'⚠️ brew cleanup code={proc.returncode}')
        except Exception as e:
            log(f'❌ Erreur brew cleanup: {e}')
    else:
        log('ℹ️ Homebrew non installé - plugin ignoré')
        return 0
    after = 0
    for p in CANDIDATE_PATHS:
        after += dir_size(p)
    freed = max(0, before - after)
    log(f'✅ Homebrew cleanup: {(freed/1024/1024):.1f} MB libérés')
    return freed
