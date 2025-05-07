# src/models/sensor.py
import os
import json
from typing import Any, Dict, Optional

class Sensor:
    """Represents a sensor that generates data."""
    
    def __init__(self, sensor_id, sensor_type, unit, **kwargs):
        """
        Initialize a sensor.
        
        Args:
            sensor_id: Unique identifier for the sensor
            sensor_type: Type of sensor (e.g., temperature, pressure)
            unit: Unit of measurement (e.g., Celsius, PSI)
            **kwargs: Additional sensor properties
        """
        self.id = sensor_id
        self.type = sensor_type
        self.unit = unit
        self.min_range = kwargs.get('min_range', 0)
        self.max_range = kwargs.get('max_range', 100)
        self.mean = kwargs.get('mean', 50)
        self.sd = kwargs.get('sd', 10)
        self.deviation_weight = kwargs.get('deviation_weight', 5)
        self.last_value = None
        
    @classmethod
    def from_config(cls, config):
        """
        Create a sensor from src.configuration.
        
        Args:
            config: Sensor configuration dict
            
        Returns:
            Initialized Sensor instance
        """
        # Initialize sensor
        sensor = cls(
            sensor_id=config['sensorId'],
            sensor_type=config.get('sensorType', 'generic'),
            unit=config['unit'],
            min_range=config.get('min_range', 0),
            max_range=config.get('max_range', 100),
            mean=config.get('mean', 50),
            sd=config.get('sd', 10),
            deviation_weight=config.get('deviation_weight', 5)
        )
        
        # Load from src.template if specified
        if 'template' in config:
            sensor._load_template(config['template'])
                
        return sensor
        
    def _load_template(self, template_name):
        """
        Load sensor configuration from src.template.
        
        Args:
            template_name: Name of the template to load
        """
        template_path = os.path.join('config', 'templates', 'sensors.json')
        
        if not os.path.exists(template_path):
            return
            
        with open(template_path, 'r') as f:
            templates = json.load(f)
            
        if template_name in templates:
            template = templates[template_name]
            
            # Apply template properties
            for key, value in template.items():
                if key != 'template':
                    setattr(self, key, value)