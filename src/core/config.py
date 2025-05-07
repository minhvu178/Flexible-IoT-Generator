# src/core/config.py
import json
import os
from src.datetime import datetime

class Config:
    """Configuration loader and manager."""
    
    def __init__(self, config_path=None):
        """
        Initialize configuration from src.file.
        
        Args:
            config_path: Path to configuration file (defaults to config/default.json)
        """
        if not config_path:
            config_path = os.path.join('config', 'default.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            
    def get(self, path, default=None):
        """
        Get a configuration value by path.
        
        Args:
            path: Dot-separated path to config value (e.g., 'general.log_level')
            default: Default value to return if path doesn't exist
            
        Returns:
            Configuration value or default
        """
        parts = path.split('.')
        value = self.config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
                
        return value
    
    def get_datetime(self, path, default=None):
        """
        Get a datetime configuration value.
        
        Args:
            path: Dot-separated path to config value
            default: Default value to return if path doesn't exist
            
        Returns:
            datetime object or default
        """
        value = self.get(path, default)
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value