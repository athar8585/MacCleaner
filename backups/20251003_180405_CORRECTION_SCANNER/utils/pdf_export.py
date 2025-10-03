import subprocess, shutil, tempfile
from pathlib import Path

def html_to_pdf(html_path, output_path, log_fn):
    # Stratégie: essayer wkhtmltopdf sinon imprimer via 'textutil' (fallback simple)
    if shutil.which('wkhtmltopdf'):
        try:
            subprocess.run(['wkhtmltopdf', str(html_path), str(output_path)], check=True, timeout=30)
            log_fn(f"📄 PDF généré: {output_path}")
            return True
        except Exception as e:
            log_fn(f"❌ wkhtmltopdf échec: {e}")
    # Fallback minimal: convertir en RTF puis PDF (macOS)
    try:
        temp_rtf = Path(tempfile.gettempdir()) / (html_path.stem + '.rtf')
        subprocess.run(['textutil', '-convert', 'rtf', '-output', str(temp_rtf), str(html_path)], check=True)
        subprocess.run(['cupsfilter', str(temp_rtf), '-o', 'media=A4'] , stdout=open(output_path,'wb'), check=True)
        log_fn(f"📄 PDF (fallback) généré: {output_path}")
        return True
    except Exception as e:
        log_fn(f"❌ Conversion PDF fallback échouée: {e}")
    return False
