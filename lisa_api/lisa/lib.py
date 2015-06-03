from stevedore import extension
import logging


class PluginManager(object):
    __instance = None

    def __new__(cls):
        if PluginManager.__instance is None:
            PluginManager.__instance = object.__new__(cls)
        return PluginManager.__instance

    def __init__(self):
        self.mgr = None
        self.plugins = []
        self.django_plugins = []
        self.load_plugins()

    def load_plugins(self):
        mgr = extension.ExtensionManager(
            namespace='lisa.api.plugins',
            invoke_on_load=False,
            verify_requirements=True
        )
        self.plugins = mgr.names()
        for plugin in self.plugins:
            self.django_plugins.append('lisa_plugins_%s' % plugin)
        logging.critical("Loaded plugins : %s" % self.plugins)
