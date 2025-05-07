# src/generators/sensor.py
from datetime import datetime, timezone, timedelta
import random
from src.base import BaseGenerator

class SensorGenerator(BaseGenerator):
    """Generates sensor measurement data."""
    
    def initialize(self):
        """Initialize the generator."""
        # Set the last value to None - will be updated during generation
        self.sensor.last_value = None
    
    def generate(self, timestamp):
        """
        Generate sensor data for the given timestamp.
        
        Args:
            timestamp: Timestamp to generate data for
            
        Returns:
            Generated sensor data dict or None if not operating
        """
        # Check if factory is operating
        if not self.is_within_operating_hours(timestamp):
            return None
            
        # Generate measurement value
        value = self._generate_value(timestamp)
        
        # Update last value
        self.sensor.last_value = value
        
        # Create payload
        if self.config.get('general.data_persistence.type') == 'file':
            # For file output, use string timestamp
            ts = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")
        else:
            # For MongoDB, use datetime with timezone
            ts = self._adjust_timestamp_timezone(timestamp)
        
        return {
            "timestamp": ts,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "sensorId": self.sensor.id,
                "unit": self.sensor.unit,
                "type": self.sensor.type
            },
            "measurement": value
        }
    
    def _generate_value(self, timestamp):
        """
        Generate a measurement value.
        
        Args:
            timestamp: Timestamp to generate value for
            
        Returns:
            Generated sensor value
        """
        # Check if current time is within stability factor time range
        current_time = timestamp.time()
        sfd_start_time = datetime.strptime(self.device.sfd_start_time, "%H:%M").time()
        sfd_end_time = datetime.strptime(self.device.sfd_end_time, "%H:%M").time()
        
        sensor = self.sensor
        stability_factor = self.device.stability_factor
        
        # Proceed only if the current time is within the specified range
        if self._is_time_in_range(current_time, sfd_start_time, sfd_end_time):
            # Calculate the sensor value based on deviation_weight and stabilityFactor
            mean = sensor.mean
            sd = sensor.sd
            min_value = sensor.min_range
            max_value = sensor.max_range
            deviation_weight = sensor.deviation_weight
            
            # Adjust mean based on deviation_weight
            if deviation_weight == 5:
                new_mean = mean
            elif deviation_weight > 5:  # scale upwards
                weight_factor = (deviation_weight - 5) / 5.0
                new_mean = mean + weight_factor * (max_value - mean)
            else:  # scale downwards
                weight_factor = (5 - deviation_weight) / 5.0
                new_mean = mean - weight_factor * (mean - min_value)
            
            # Adjust for stabilityFactor < 50
            if stability_factor < 50:
                if deviation_weight > 7:
                    new_mean = min(new_mean, max_value + (deviation_weight - 7) * sd)
                elif deviation_weight < 3:
                    new_mean = max(new_mean, min_value - (3 - deviation_weight) * sd)
            
            # Generate value based on the new mean and sd
            value = random.gauss(new_mean, sd)
            
            # Clamp the value to be within the min and max range
            value = max(min_value, min(value, max_value))
            
            return value
        else:
            # Return the default mean if outside the time range
            return sensor.mean
    
    def _is_time_in_range(self, current_time, start_time, end_time):
        """
        Check if current_time is within the specified time range.
        
        Args:
            current_time: Time to check
            start_time: Start of time range
            end_time: End of time range
            
        Returns:
            True if current_time is within range, False otherwise
        """
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            # Handle overnight ranges (e.g., 22:00 to 06:00)
            return current_time >= start_time or current_time <= end_time
    
    def _adjust_timestamp_timezone(self, timestamp):
        """
        Adjust timestamp to include the factory's timezone.
        
        Args:
            timestamp: Timestamp to adjust
            
        Returns:
            Timestamp with factory timezone
        """
        # Parse the timezone offset
        offset_str = self.factory.time_zone
        
        # Default to UTC if no timezone specified
        if not offset_str:
            return timestamp.replace(tzinfo=timezone.utc)
            
        # Parse the timezone offset
        hours, minutes = map(int, offset_str.replace(':', ''))
        
        # Create timezone offset
        tz_offset = timezone(timedelta(hours=hours, minutes=minutes))
        
        # Apply timezone offset
        local_time = timestamp.replace(tzinfo=tz_offset)
        
        # Convert to UTC for MongoDB storage
        return local_time.astimezone(timezone.utc)
        
    def is_within_operating_hours(self, timestamp):
        """
        Check if timestamp is within factory operating hours.
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            True if within operating hours, False otherwise
        """
        return self.factory.is_operating(timestamp)