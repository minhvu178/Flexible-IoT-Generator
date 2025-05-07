# src/plugins/plugin_loader.py
import importlib
import os
import pkgutil
import inspect
from ..generators.base import BaseGenerator


class PluginLoader:
    """Loads generator plugins from src.the plugins directory."""
    
    @staticmethod
    def load_plugins():
        """Discover and load all generator plugins."""
        plugins = {}
        plugin_path = os.path.join(os.path.dirname(__file__), 'custom')
        
        for _, name, ispkg in pkgutil.iter_modules([plugin_path]):
            if not ispkg:
                module = importlib.import_module(f'plugins.custom.{name}')
                for item_name, item in inspect.getmembers(module, inspect.isclass):
                    if issubclass(item, BaseGenerator) and item != BaseGenerator:
                        plugins[item_name] = item
        
        return plugins