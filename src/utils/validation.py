from typing import Dict, Any, Optional
import json
import os

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate the main configuration."""
    required_keys = ['app', 'database', 'logging', 'scheduler', 'generator']
    return all(key in config for key in required_keys)

def validate_database_config(config: Dict[str, Any]) -> bool:
    """Validate database configuration."""
    required_keys = ['type', 'host', 'port', 'name']
    return all(key in config for key in required_keys)

def validate_logging_config(config: Dict[str, Any]) -> bool:
    """Validate logging configuration."""
    required_keys = ['level', 'file', 'console', 'format']
    return all(key in config for key in required_keys)

def validate_factory_config(config: Dict[str, Any]) -> bool:
    """Validate factory configuration."""
    required_keys = ['id', 'name', 'location']
    return all(key in config for key in required_keys)

def validate_plugin(plugin: Any) -> bool:
    """Validate a plugin."""
    return hasattr(plugin, 'generate') and callable(getattr(plugin, 'generate'))

def validate_app_config(config: Dict[str, Any]) -> bool:
    """Validate application configuration."""
    return validate_config(config) and validate_database_config(config.get('database', {}))
