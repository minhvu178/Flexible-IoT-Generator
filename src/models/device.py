# src/models/device.py
import os
import json
from typing import List, Optional

from .sensor import Sensor

class Device:
    """Represents a device with sensors."""
    
    def __init__(self, device_id, device_type, **kwargs):
        """
        Initialize a device.
        
        Args:
            device_id: Unique identifier for the device
            device_type: Type of device
            **kwargs: Additional device properties
        """
        self.id = device_id
        self.type = device_type
        self.sensors = []
        self.stability_factor = kwargs.get('stability_factor', 95)
        self.sfd_start_time = kwargs.get('sfd_start_time', '14:00')
        self.sfd_end_time = kwargs.get('sfd_end_time', '16:00')
        
    @classmethod
    def from_config(cls, config):
        """
        Create a device from src.configuration.
        
        Args:
            config: Device configuration dict
            
        Returns:
            Initialized Device instance
        """
        # Initialize device
        device = cls(
            device_id=config['deviceId'],
            device_type=config['deviceType'],
            stability_factor=config.get('stabilityFactor', 95),
            sfd_start_time=config.get('sfd_start_time', '14:00'),
            sfd_end_time=config.get('sfd_end_time', '16:00')
        )
        
        # Load from src.template if specified
        if 'template' in config:
            device._load_template(config['template'])
            
        # Load sensors from src.config
        if 'sensors' in config:
            for sensor_config in config['sensors']:
                sensor = Sensor.from_config(sensor_config)
                device.add_sensor(sensor)
                
        return device
        
    def _load_template(self, template_name):
        """
        Load device configuration from src.template.
        
        Args:
            template_name: Name of the template to load
        """
        template_path = os.path.join('/home/minhvu/Flexible-IoT-Generator', 'config', 'templates', 'devices.json')
        
        if not os.path.exists(template_path):
            return
            
        with open(template_path, 'r') as f:
            templates = json.load(f)
            
        if template_name in templates:
            template = templates[template_name]
            
            # Load sensors from src.template
            if 'sensors' in template:
                for sensor_config in template['sensors']:
                    sensor = Sensor.from_config(sensor_config)
                    self.add_sensor(sensor)
    
    def add_sensor(self, sensor):
        """
        Add a sensor to the device.
        
        Args:
            sensor: Sensor instance to add
        """
        self.sensors.append(sensor)