# src/generators/machine_status.py
from enum import Enum
from .base import BaseGenerator
import random

class MachineStatus(Enum):
    RUNNING = "running"
    IDLE = "idle"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    SETUP = "setup"
    ERROR = "error"

class MachineStatusGenerator(BaseGenerator):
    """Generates machine status data."""
    
    def initialize(self):
        self.current_status = MachineStatus.STOPPED
        self.status_since = None
        self.status_probabilities = {
            MachineStatus.RUNNING: {
                MachineStatus.RUNNING: 0.98,
                MachineStatus.IDLE: 0.015,
                MachineStatus.ERROR: 0.005
            },
            MachineStatus.IDLE: {
                MachineStatus.IDLE: 0.7,
                MachineStatus.RUNNING: 0.25,
                MachineStatus.STOPPED: 0.05
            },
            # ... other transition probabilities
        }
    
    def generate(self, timestamp):
        if not self.is_within_operating_hours(timestamp):
            return {"status": MachineStatus.STOPPED.value, "timestamp": timestamp}
            
        # Status transition logic based on probabilities
        # ... implementation ...
        
        return {
            "timestamp": timestamp,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "type": "machine_status"
            },
            "status": self.current_status.value,
            "since": self.status_since
        }