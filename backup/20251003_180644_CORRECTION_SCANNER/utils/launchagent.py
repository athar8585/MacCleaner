from pathlib import Path
import plistlib

PLIST_NAME = 'com.maccleaner.pro.autorun.plist'

TEMPLATE = {
    'Label': 'com.maccleaner.pro.autorun',
    'ProgramArguments': ['python3', str(Path.cwd() / 'mac_cleaner.py'), '--daemon'],
    'RunAtLoad': True,
    'KeepAlive': False,
    'StartInterval': 3600,
    'StandardOutPath': str(Path.cwd() / 'logs' / 'agent.out.log'),
    'StandardErrorPath': str(Path.cwd() / 'logs' / 'agent.err.log')
}

def launch_agent_path():
    return Path.home() / 'Library' / 'LaunchAgents' / PLIST_NAME

def is_launch_agent_installed():
    return launch_agent_path().exists()

def install_launch_agent():
    launch_dir = launch_agent_path().parent
    launch_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    plist_path = launch_agent_path()
    with open(plist_path, 'wb') as f:
        plistlib.dump(TEMPLATE, f)
    return plist_path

def uninstall_launch_agent():
    plist_path = launch_agent_path()
    if plist_path.exists():
        plist_path.unlink()
        return True
    return False
