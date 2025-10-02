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

def full_update_check(log_fn):
    """Vérification complète avec téléchargement binaire (concept)"""
    settings = load_settings()
    url = settings.get('update_url') or settings.get('updates', {}).get('manifest_url')
    if not url:
        log_fn("ℹ️ Pas d'URL de mise à jour configurée")
        return False, "Pas d'URL configurée"
    
    try:
        remote = fetch_manifest(url)
        current_version = settings.get('version', '0.0.0')
        remote_version = remote.get('version', '0.0.0')
        
        if not _version_gt(remote_version, current_version):
            return False, f"Version actuelle ({current_version}) est à jour"
        
        # TODO: Implémenter téléchargement complet
        # - Télécharger archive .zip/.tar.gz
        # - Vérifier signature/hash
        # - Backup version actuelle
        # - Extraction et remplacement
        # - Redémarrage automatique
        
        log_fn(f"⬆️ Mise à jour {remote_version} disponible (téléchargement manuel requis)")
        return True, f"Mise à jour {remote_version} disponible"
        
    except Exception as e:
        error_msg = f"Erreur vérification complète: {e}"
        log_fn(f"❌ {error_msg}")
        return False, error_msg

def download_and_verify_update(manifest, log_fn):
    """Télécharger et vérifier une mise à jour complète"""
    download_url = manifest.get('download_url')
    if not download_url:
        return False, "Pas d'URL de téléchargement"
    
    try:
        import tempfile
        import hashlib
        
        # Télécharger dans un fichier temporaire
        log_fn("📥 Téléchargement de la mise à jour...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with urllib.request.urlopen(download_url, timeout=30) as response:
                chunk_size = 8192
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    tmp_file.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        if downloaded % (chunk_size * 10) == 0:  # Log tous les 10 chunks
                            log_fn(f"📥 Progression: {progress:.1f}%")
            
            tmp_path = tmp_file.name
        
        # Vérifier hash si fourni
        expected_hash = manifest.get('sha256')
        if expected_hash:
            log_fn("🔍 Vérification intégrité...")
            with open(tmp_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash != expected_hash:
                os.unlink(tmp_path)
                return False, "Hash de vérification invalide"
        
        log_fn("✅ Téléchargement vérifié")
        return True, tmp_path
        
    except Exception as e:
        return False, f"Erreur téléchargement: {e}"
