import os, shutil
from pathlib import Path

def run(log):
    derived = Path('~/Library/Developer/Xcode/DerivedData').expanduser()
    archives = Path('~/Library/Developer/Xcode/Archives').expanduser()
    freed = 0
    for path in [derived, archives]:
        if path.exists():
            for item in path.iterdir():
                try:
                    if item.is_dir():
                        size = dir_size(item)
                        shutil.rmtree(item, ignore_errors=True)
                        freed += size
                except Exception:
                    pass
            log(f"🧪 Xcode: nettoyé {path}")
    log(f"✅ Xcode cleanup terminé: {(freed/1024/1024):.1f} MB libérés")
    return freed

def dir_size(p: Path):
    total=0
    for root, dirs, files in os.walk(p):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root,f))
            except Exception: pass
    return total
