import hashlib, json, os, pathlib

DEFAULT_HASH_FILE = 'updates/hashes.json'
HASH_BLOCK_SIZE = 65536


def hash_file(path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while True:
                data = f.read(HASH_BLOCK_SIZE)
                if not data:
                    break
                h.update(data)
        return h.hexdigest()
    except FileNotFoundError:
        return ''


def load_hash_manifest(manifest_path: str = DEFAULT_HASH_FILE):
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def verify_paths(paths, base_dir='.', manifest_path=DEFAULT_HASH_FILE):
    manifest = load_hash_manifest(manifest_path)
    results = []
    for rel in paths:
        full = pathlib.Path(base_dir) / rel
        expected = manifest.get(rel)
        actual = hash_file(str(full))
        ok = expected is None or expected == actual
        results.append({
            'path': rel,
            'expected': expected,
            'actual': actual,
            'ok': ok
        })
    return results


def generate_manifest(paths, base_dir='.', out_file=DEFAULT_HASH_FILE):
    data = {}
    for rel in paths:
        full = pathlib.Path(base_dir) / rel
        if full.is_file():
            data[rel] = hash_file(str(full))
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return out_file
