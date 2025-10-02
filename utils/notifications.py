import subprocess, shlex, platform

def notify(title, message, sound=True):
    if platform.system() != 'Darwin':
        return
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(['osascript', '-e', script], check=False)
        if sound:
            subprocess.run(shlex.split('afplay /System/Library/Sounds/Glass.aiff'), check=False)
    except Exception:
        pass
