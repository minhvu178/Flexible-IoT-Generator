# src/generators/base.py
from src.abc import ABC, abstractmethod
from datetime import datetime

class BaseGenerator(ABC):
    """Base class for all data generators."""
    
    def __init__(self, config, factory, device=None, sensor=None):
        """
        Initialize generator with factory, device, and sensor context.
        
        Args:
            config: Application configuration
            factory: Factory instance
            device: Device instance (optional)
            sensor: Sensor instance (optional)
        """
        self.config = config
        self.factory = factory
        self.device = device
        self.sensor = sensor
        self.initialize()
    
    def initialize(self):
        """Initialize generator with specific setup."""
        pass
    
    @abstractmethod
    def generate(self, timestamp):
        """
        Generate data for the given timestamp.
        
        Args:
            timestamp: Timestamp to generate data for
            
        Returns:
            Generated data or None if not applicable
        """
        pass
    
    def is_within_operating_hours(self, timestamp):
        """
        Check if timestamp is within factory operating hours.
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            True if within operating hours, False otherwise
        """
        return self.factory.is_operating(timestamp)