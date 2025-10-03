import os, datetime, json
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><title>Rapport MacCleaner</title><style>body{font-family:-apple-system,Helvetica,Arial;margin:24px;background:#f5f7fa;color:#222}h1{color:#007AFF}table{border-collapse:collapse;width:100%;margin:16px 0}th,td{border:1px solid #ddd;padding:6px;font-size:13px}th{background:#eef}code{background:#eee;padding:2px 4px;border-radius:4px}</style></head><body><h1>Rapport MacCleaner Pro</h1><p>Généré: {generated}</p><h2>Résumé</h2><ul><li>Espace libéré: {space_freed:.1f} MB</li><li>Mode: {mode}</li><li>Catégories: {categories}</li><li>Durée: {duration:.1f} sec</li></ul><h2>Fichiers Analysés (extrait)</h2><table><tr><th>Type</th><th>Taille</th><th>Chemin</th><th>Tags</th></tr>{rows}</table><p><em>MacCleaner Pro — Optimisation système intelligente.</em></p></body></html>"""

def generate_html_report(output_dir, analyzed_files, space_freed_mb, categories, duration_sec, mode, log_fn):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in sorted(analyzed_files, key=lambda x: x.get('size',0), reverse=True)[:200]:
        size = item.get('size',0)
        size_str = f"{size/1024/1024:.2f} MB" if size>1024*1024 else f"{size/1024:.1f} KB"
        tags = []
        if item.get('protected'): tags.append('iCloud')
        if item.get('important'): tags.append('Important')
        rows.append(f"<tr><td>{item.get('type')}</td><td>{size_str}</td><td><code>{item.get('path')}</code></td><td>{', '.join(tags)}</td></tr>")
    html = HTML_TEMPLATE.format(
        generated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        space_freed=space_freed_mb,
        categories=", ".join(categories),
        duration=duration_sec,
        mode=mode,
        rows=''.join(rows)
    )
    filename = output_dir / f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filename.write_text(html, encoding='utf-8')
    log_fn(f"📄 Rapport HTML généré: {filename}")
    return filename
