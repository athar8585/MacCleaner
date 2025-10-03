import importlib, pkgutil, pathlib, sys, os
from importlib.util import spec_from_file_location, module_from_spec

PLUGIN_NAMESPACE = 'plugins'

class PluginManager:
    def __init__(self, plugin_dir=None, log_fn=None):
        self.log = log_fn or print
        self.plugins = {}
        self.plugin_dir = plugin_dir or pathlib.Path(__file__).parent
        self.discover()

    def discover(self):
        plugin_path = pathlib.Path(self.plugin_dir)
        if not plugin_path.exists():
            return
            
        for plugin_file in plugin_path.glob('*_cleanup.py'):
            name = plugin_file.stem.replace('_cleanup', '')
            try:
                spec = spec_from_file_location(name, plugin_file)
                if spec and spec.loader:
                    module = module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'run'):
                        self.plugins[name] = module.run  # Stocker la fonction, pas le module
                        self.log(f"🔌 Plugin chargé: {name}")
            except Exception as e:
                self.log(f"❌ Échec chargement plugin {name}: {e}")

    def run_all(self):
        total_freed = 0
        for name, plugin in self.plugins.items():
            try:
                freed = plugin.run(self.log)
                total_freed += freed or 0
            except Exception as e:
                self.log(f"❌ Plugin {name} erreur: {e}")
        self.log(f"🔁 Plugins terminé: {total_freed/1024/1024:.1f} MB libérés")
        return total_freed

    def get_available_plugins(self):
        """Retourner la liste des plugins disponibles"""
        return list(self.plugins.keys())
