import json, urllib.request, os
from pathlib import Path
from config.loader import load_settings, save_settings

MANIFEST_LOCAL = Path('updates/latest.json')

def fetch_manifest(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def load_local_manifest():
    if MANIFEST_LOCAL.exists():
        try:
            return json.loads(MANIFEST_LOCAL.read_text('utf-8'))
        except Exception:
            return None
    return None

def save_manifest(data):
    MANIFEST_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_LOCAL.write_text(json.dumps(data, indent=2), encoding='utf-8')

def check_for_update(log_fn):
    settings = load_settings()
    url = settings.get('update_url') or settings.get('updates', {}).get('manifest_url')
    if not url:
        log_fn("ℹ️ Pas d'URL de mise à jour configurée")
        return None
    try:
        remote = fetch_manifest(url)
        save_manifest(remote)
        current_version = settings.get('version', '0.0.0')
        remote_version = remote.get('version')
        if _version_gt(remote_version, current_version):
            log_fn(f"⬆️ Nouvelle version disponible: {remote_version} (actuelle {current_version})")
            return remote
        else:
            log_fn("✅ Application à jour")
    except Exception as e:
        log_fn(f"❌ Erreur vérification mise à jour: {e}")
    return None

def apply_signature_update(manifest, log_fn):
    sig_url = manifest.get('signatures_url')
    if not sig_url:
        return False
    try:
        with urllib.request.urlopen(sig_url, timeout=5) as resp:
            raw = resp.read().decode('utf-8')
        Path('malware_scanner/signatures_min.json').write_text(raw, encoding='utf-8')
        log_fn("✅ Signatures mises à jour")
        return True
    except Exception as e:
        log_fn(f"❌ Erreur mise à jour signatures: {e}")
        return False

def _version_gt(a, b):
    def parse(v):
        return [int(x) for x in v.split('.') if x.isdigit()]
    return parse(a) > parse(b)
