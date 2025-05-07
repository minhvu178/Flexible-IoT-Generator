# src/generators/base.py
from abc import ABC, abstractmethod
from datetime import datetime

class BaseGenerator(ABC):
    """Base class for all data generators."""
    
    def __init__(self, config, factory, device=None, sensor=None):
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
        """Generate data for the given timestamp."""
        pass
    
    def is_within_operating_hours(self, timestamp):
        """Check if timestamp is within factory operating hours."""
        # Implementation
        return True