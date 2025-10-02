import importlib, pkgutil, pathlib

PLUGIN_NAMESPACE = 'plugins'

class PluginManager:
    def __init__(self, log_fn):
        self.log = log_fn
        self.plugins = []
        self.discover()

    def discover(self):
        pkg_path = pathlib.Path(__file__).parent
        for modinfo in pkgutil.iter_modules([str(pkg_path)]):
            name = modinfo.name
            if name.endswith('_cleanup'):
                try:
                    module = importlib.import_module(f'{PLUGIN_NAMESPACE}.{name}')
                    if hasattr(module, 'run'):
                        self.plugins.append(module)
                        self.log(f"🔌 Plugin chargé: {name}")
                except Exception as e:
                    self.log(f"❌ Échec chargement plugin {name}: {e}")

    def run_all(self):
        total_freed = 0
        for plugin in self.plugins:
            try:
                freed = plugin.run(self.log)
                total_freed += freed or 0
            except Exception as e:
                self.log(f"❌ Plugin {plugin.__name__} erreur: {e}")
        self.log(f"🔁 Plugins terminé: {total_freed/1024/1024:.1f} MB libérés")
        return total_freed
