import subprocess

def run(log):
    freed = 0
    cmds = [
        ['docker','system','prune','-f'],
        ['docker','volume','prune','-f'],
        ['docker','image','prune','-af']
    ]
    for c in cmds:
        try:
            proc = subprocess.run(c, capture_output=True, text=True, timeout=60)
            if proc.returncode==0:
                log(f"🐳 {' '.join(c)} OK")
            else:
                log(f"⚠️ Docker commande échec: {' '.join(c)}")
        except FileNotFoundError:
            log("ℹ️ Docker non installé - plugin ignoré")
            return 0
        except Exception as e:
            log(f"❌ Erreur Docker: {e}")
    log("✅ Docker cleanup terminé")
    return freed
