# src/generators/quality.py
import random
from datetime import timedelta
from .base import BaseGenerator

class QualityGenerator(BaseGenerator):
    """Generates product quality data."""
    
    def initialize(self):
        """Initialize the generator."""
        self.defect_rate = random.uniform(0.001, 0.03)  # 0.1% to 3% defect rate
        self.last_check_time = None
        self.check_interval = timedelta(minutes=15)  # Quality check every 15 minutes
        
        # Define potential defect types based on the device type
        self.defect_types = {
            "plastic_extruder": ["bubble", "discoloration", "thickness", "contamination"],
            "injection_molder": ["flash", "short_shot", "warping", "sink_mark", "burn_mark"],
            "cnc_machine": ["dimension", "finish", "tool_mark", "chatter"],
            "packaging_machine": ["seal", "alignment", "label", "count"],
            "assembly_robot": ["connection", "alignment", "missing_part", "damage"],
            "default": ["visual", "dimension", "functional", "material"]
        }
    
    def generate(self, timestamp):
        """
        Generate quality check data.
        
        Args:
            timestamp: Timestamp to generate data for
            
        Returns:
            Generated quality data or None if not time for a check
        """
        # Check if factory is operating
        if not self.is_within_operating_hours(timestamp):
            return None
        
        # Initialize last check time if not set
        if not self.last_check_time:
            self.last_check_time = timestamp - self.check_interval
            
        # Check if it's time for a quality check
        if timestamp - self.last_check_time < self.check_interval:
            return None
            
        # Update last check time
        self.last_check_time = timestamp
        
        # Get device type (or default)
        device_type = getattr(self.device, 'type', 'default').lower()
        
        # Get defect types for this device
        defect_list = self.defect_types.get(device_type, self.defect_types['default'])
        
        # Generate sample size (between 10 and 100)
        sample_size = random.randint(10, 100)
        
        # Calculate number of defects based on defect rate
        num_defects = round(sample_size * self.defect_rate)
        
        # Generate defects data if any
        defects = []
        if num_defects > 0:
            for _ in range(num_defects):
                defect_type = random.choice(defect_list)
                severity = random.uniform(0.1, 1.0)
                defects.append({
                    "type": defect_type,
                    "severity": round(severity, 2)
                })
        
        # Build quality check data
        return {
            "timestamp": timestamp,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "type": "quality_check"
            },
            "sample_size": sample_size,
            "passed": sample_size - num_defects,
            "defects": num_defects,
            "defect_rate": round(num_defects / sample_size, 4),
            "defect_details": defects
        }