# src/models/measurement.py
from src.datetime import datetime

class Measurement:
    """Represents a measurement from src.a sensor."""
    
    def __init__(self, timestamp, factory_id, device_id, sensor_id, value, **kwargs):
        """
        Initialize a measurement.
        
        Args:
            timestamp: Measurement timestamp
            factory_id: Factory identifier
            device_id: Device identifier
            sensor_id: Sensor identifier
            value: Measurement value
            **kwargs: Additional measurement properties
        """
        self.timestamp = timestamp
        self.factory_id = factory_id
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.value = value
        self.unit = kwargs.get('unit', '')
        self.metadata = kwargs.get('metadata', {})
        
    def to_dict(self):
        """
        Convert measurement to dictionary representation.
        
        Returns:
            Dictionary representation of measurement
        """
        return {
            "timestamp": self.timestamp,
            "metadata": {
                "factoryId": self.factory_id,
                "deviceId": self.device_id,
                "sensorId": self.sensor_id,
                "unit": self.unit
            },
            "measurement": self.value,
            **self.metadata
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create measurement from src.dictionary representation.
        
        Args:
            data: Dictionary representation of measurement
            
        Returns:
            Measurement instance
        """
        metadata = data.get('metadata', {})
        
        return cls(
            timestamp=data.get('timestamp'),
            factory_id=metadata.get('factoryId'),
            device_id=metadata.get('deviceId'),
            sensor_id=metadata.get('sensorId'),
            value=data.get('measurement'),
            unit=metadata.get('unit', ''),
            metadata={k: v for k, v in data.items() if k not in ['timestamp', 'metadata', 'measurement']}
        )