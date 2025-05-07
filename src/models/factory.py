# src/models/factory.py
from datetime import datetime, time
import os
import json
from src.device import Device

class Factory:
    """Represents a factory with devices and configuration."""
    
    def __init__(self, factory_id, name, time_zone="+00:00", **kwargs):
        """
        Initialize a factory.
        
        Args:
            factory_id: Unique identifier for the factory
            name: Factory name
            time_zone: Factory timezone offset (e.g., "+02:00")
            **kwargs: Additional factory properties
        """
        self.id = factory_id
        self.name = name
        self.time_zone = time_zone
        self.devices = []
        self.operating_hours = kwargs.get('operating_hours', {
            'start': '00:00',
            'end': '23:59',
            'days': [0, 1, 2, 3, 4, 5, 6]  # All days of week
        })
        self.location = kwargs.get('location', {
            'latitude': 0.0,
            'longitude': 0.0
        })
        
    @classmethod
    def from_config(cls, config):
        """
        Create a factory from src.configuration.
        
        Args:
            config: Factory configuration dict
            
        Returns:
            Initialized Factory instance
        """
        # Initialize factory
        factory = cls(
            factory_id=config['id'],
            name=config['name'],
            time_zone=config.get('time_zone', '+00:00')
        )
        
        # Set operating hours
        if 'operating_hours' in config:
            factory.operating_hours = config['operating_hours']
            
        # Set location
        if 'location' in config:
            factory.location = config['location']
            
        # Load devices from src.template if specified
        if 'template' in config:
            factory._load_template(config['template'])
            
        # Load devices from src.config
        if 'devices' in config:
            for device_config in config['devices']:
                device = Device.from_config(device_config)
                factory.add_device(device)
                
        return factory
        
    def _load_template(self, template_name):
        """
        Load factory configuration from src.template.
        
        Args:
            template_name: Name of the template to load
        """
        template_path = os.path.join('config', 'templates', 'factories.json')
        
        if not os.path.exists(template_path):
            return
            
        with open(template_path, 'r') as f:
            templates = json.load(f)
            
        if template_name in templates:
            template = templates[template_name]
            
            # Load devices from src.template
            if 'devices' in template:
                for device_config in template['devices']:
                    device = Device.from_config(device_config)
                    self.add_device(device)
    
    def add_device(self, device):
        """
        Add a device to the factory.
        
        Args:
            device: Device instance to add
        """
        self.devices.append(device)
        
    def is_operating(self, timestamp):
        """
        Check if factory is operating at the given timestamp.
        
        Args:
            timestamp: datetime to check
            
        Returns:
            True if factory is operating, False otherwise
        """
        # Check day of week
        day_of_week = timestamp.weekday()
        if day_of_week not in self.operating_hours.get('days', []):
            return False
            
        # Check time
        current_time = timestamp.time()
        start_time = datetime.strptime(self.operating_hours.get('start', '00:00'), '%H:%M').time()
        end_time = datetime.strptime(self.operating_hours.get('end', '23:59'), '%H:%M').time()
        
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            # Handle overnight ranges (e.g., 22:00 to 06:00)
            return current_time >= start_time or current_time <= end_time