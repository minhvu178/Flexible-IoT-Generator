# src/generators/production.py
import random
from datetime import timedelta
from src.base import BaseGenerator
from src.machine_status import MachineStatus

class ProductionGenerator(BaseGenerator):
    """Generates production count data."""
    
    def initialize(self):
        """Initialize the generator."""
        # Production rate range (units per hour) based on device type
        self.production_rates = {
            "plastic_extruder": (50, 120),
            "injection_molder": (80, 200),
            "cnc_machine": (10, 40),
            "packaging_machine": (300, 600),
            "assembly_robot": (40, 100),
            "default": (20, 80)
        }
        
        # Get production range for this device
        device_type = getattr(self.device, 'type', 'default').lower()
        self.min_rate, self.max_rate = self.production_rates.get(
            device_type, self.production_rates['default']
        )
        
        # Set production target (average rate)
        self.target_rate = (self.min_rate + self.max_rate) / 2
        
        # Initialize counters
        self.total_count = 0
        self.hourly_count = 0
        self.last_update = None
        self.report_interval = timedelta(minutes=15)  # Report every 15 minutes
    
    def generate(self, timestamp):
        """
        Generate production count data.
        
        Args:
            timestamp: Timestamp to generate data for
            
        Returns:
            Generated production data or None if not time for a report
        """
        # Check if factory is operating
        if not self.is_within_operating_hours(timestamp):
            return None
            
        # Initialize last update time if not set
        if not self.last_update:
            self.last_update = timestamp - self.report_interval
        
        # Check if it's time for a report
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
        
        # Calculate production since last update
        elapsed_hours = elapsed.total_seconds() / 3600  # Convert to hours
        
        # Base production rate - varies by ±10%
        base_rate = random.uniform(self.min_rate, self.max_rate)
        
        # Adjust based on machine status
        if machine_status:
            if machine_status == MachineStatus.RUNNING:
                rate = base_rate
            elif machine_status == MachineStatus.IDLE:
                rate = base_rate * 0.1  # 10% of normal production
            else:
                rate = 0  # No production in other states
        else:
            # If no machine status available, assume running at normal rate
            rate = base_rate
        
        # Calculate period production
        period_production = int(rate * elapsed_hours)
        
        # Update total count
        self.total_count += period_production
        
        # Update hourly count (reset if more than an hour has passed)
        hours_since_last = elapsed.total_seconds() / 3600
        if hours_since_last >= 1:
            self.hourly_count = period_production
        else:
            self.hourly_count += period_production
        
        # Return production data
        return {
            "timestamp": timestamp,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "type": "production"
            },
            "interval_count": period_production,
            "hourly_rate": round(self.hourly_count / min(hours_since_last, 1), 2),
            "total_count": self.total_count,
            "target_rate": self.target_rate,
            "efficiency": round((self.hourly_count / (self.target_rate * min(hours_since_last, 1))) * 100, 2)
        }