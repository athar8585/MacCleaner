import threading, time, psutil, shutil
from datetime import datetime
from config.loader import load_settings, save_settings
from database.db import record_alert

class AutoScheduler:
    def __init__(self, trigger_fn, log_fn):
        self.trigger_clean = trigger_fn
        self.log = log_fn
        self.settings = load_settings()
        self.stop_flag = False
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        self.log("⏱️ Planificateur automatique démarré")

    def stop(self):
        self.stop_flag = True

    def _loop(self):
        last_run = 0
        interval = self.settings['scheduler'].get('interval_minutes', 30) * 60
        smart = self.settings['scheduler'].get('smart_scheduling', True)
        while not self.stop_flag:
            now = time.time()
            if now - last_run >= interval:
                if self._should_trigger(smart):
                    self.log("🤖 Déclenchement auto du nettoyage (conditions atteintes)")
                    record_alert('auto_clean', 'info', 'Auto clean triggered', datetime.utcnow().isoformat())
                    self.trigger_clean(auto=True)
                    last_run = now
            time.sleep(10)

    def _should_trigger(self, smart):
        if not smart:
            return True
        # Conditions seuils
        disk = shutil.disk_usage('/')
        free_percent = (disk.free / disk.total) * 100
        mem = psutil.virtual_memory()
        settings = self.settings
        thresholds = settings.get('thresholds', {})
        if free_percent < thresholds.get('disk_space_alert', 10):
            return True
        if mem.percent > thresholds.get('memory_alert', 85):
            return True
        return False
