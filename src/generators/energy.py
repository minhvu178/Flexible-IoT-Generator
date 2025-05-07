# src/generators/energy.py
import random
from datetime import timedelta
from src.base import BaseGenerator
from src.machine_status import MachineStatus

class EnergyGenerator(BaseGenerator):
    """Generates energy consumption data."""
    
    def initialize(self):
        """Initialize the generator."""
        # Energy consumption rates (kW) based on device type
        self.energy_rates = {
            "plastic_extruder": {
                MachineStatus.RUNNING: (10, 15),
                MachineStatus.IDLE: (2, 3),
                MachineStatus.STOPPED: (0.5, 1),
                "default": (0.5, 1)
            },
            "injection_molder": {
                MachineStatus.RUNNING: (20, 30),
                MachineStatus.IDLE: (3, 5),
                MachineStatus.STOPPED: (1, 2),
                "default": (1, 2)
            },
            "cnc_machine": {
                MachineStatus.RUNNING: (5, 10),
                MachineStatus.IDLE: (1, 2),
                MachineStatus.STOPPED: (0.2, 0.5),
                "default": (0.2, 0.5)
            },
            "default": {
                MachineStatus.RUNNING: (8, 12),
                MachineStatus.IDLE: (2, 3),
                MachineStatus.STOPPED: (0.5, 1),
                "default": (0.5, 1)
            }
        }
        
        # Get device type
        self.device_type = getattr(self.device, 'type', 'default').lower()
        
        # Total energy consumption
        self.total_consumption = 0
        self.last_update = None
        self.report_interval = timedelta(minutes=5)  # Report every 5 minutes
    
    def generate(self, timestamp):
        """
        Generate energy consumption data.
        
        Args:
            timestamp: Timestamp to generate data for
            
        Returns:
            Generated energy data or None if not time for a report
        """
        # Check if it's time for a report
        if not self.last_update:
            self.last_update = timestamp - self.report_interval
            
        elapsed = timestamp - self.last_update
        if elapsed < self.report_interval:
            return None
            
        # Update last update time
        self.last_update = timestamp
        
        # Get current machine status from src.machine status generator
        machine_status = None
        for generator in self.factory.generators:
            if (generator.__class__.__name__ == 'MachineStatusGenerator' and 
                generator.device.id == self.device.id):
                machine_status = generator.current_status
                break
        
        # Calculate energy consumption since last update
        elapsed_hours = elapsed.total_seconds() / 3600  # Convert to hours
        
        # Get energy rate for current status
        status_key = machine_status if machine_status else "default"
        device_rates = self.energy_rates.get(self.device_type, self.energy_rates['default'])
        min_rate, max_rate = device_rates.get(status_key, device_rates['default'])
        
        # Calculate base rate with some randomness
        base_rate = random.uniform(min_rate, max_rate)
        
        # Add some fluctuation
        fluctuation = random.uniform(0.9, 1.1)
        rate = base_rate * fluctuation
        
        # Calculate period consumption
        period_consumption = rate * elapsed_hours
        
        # Update total consumption
        self.total_consumption += period_consumption
        
        # Return energy data
        return {
            "timestamp": timestamp,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "type": "energy"
            },
            "current_kw": round(rate, 2),
            "kwh_used": round(period_consumption, 3),
            "total_kwh": round(self.total_consumption, 3)
        }