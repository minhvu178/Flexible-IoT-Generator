# src/generators/machine_status.py
from datetime import datetime, timedelta
from enum import Enum
import random
from .base import BaseGenerator

class MachineStatus(Enum):
    """Enum for machine status values."""
    RUNNING = "running"
    IDLE = "idle"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    SETUP = "setup"
    ERROR = "error"

class MachineStatusGenerator(BaseGenerator):
    """Generates machine status data."""
    
    def initialize(self):
        """Initialize the generator with transition probabilities."""
        self.current_status = MachineStatus.STOPPED
        self.status_since = None
        
        # Define transition probabilities for each state
        self.status_probabilities = {
            MachineStatus.RUNNING: {
                MachineStatus.RUNNING: 0.98,    # 98% chance to stay running
                MachineStatus.IDLE: 0.015,      # 1.5% chance to go idle
                MachineStatus.ERROR: 0.005      # 0.5% chance to error
            },
            MachineStatus.IDLE: {
                MachineStatus.IDLE: 0.7,        # 70% chance to stay idle
                MachineStatus.RUNNING: 0.25,    # 25% chance to start running
                MachineStatus.STOPPED: 0.05     # 5% chance to stop
            },
            MachineStatus.STOPPED: {
                MachineStatus.STOPPED: 0.7,     # 70% chance to stay stopped
                MachineStatus.SETUP: 0.3        # 30% chance to go to setup
            },
            MachineStatus.SETUP: {
                MachineStatus.SETUP: 0.6,       # 60% chance to stay in setup
                MachineStatus.RUNNING: 0.4      # 40% chance to start running
            },
            MachineStatus.MAINTENANCE: {
                MachineStatus.MAINTENANCE: 0.8, # 80% chance to stay in maintenance
                MachineStatus.STOPPED: 0.2      # 20% chance to stop
            },
            MachineStatus.ERROR: {
                MachineStatus.ERROR: 0.3,       # 30% chance to stay in error
                MachineStatus.STOPPED: 0.4,     # 40% chance to stop
                MachineStatus.MAINTENANCE: 0.3  # 30% chance to go to maintenance
            }
        }
    
    def generate(self, timestamp):
        """
        Generate machine status for the given timestamp.
        
        Args:
            timestamp: Timestamp to generate status for
            
        Returns:
            Generated status data or None if not operating
        """
        # Start with STOPPED status if no previous status
        if not self.status_since:
            self.current_status = MachineStatus.STOPPED
            self.status_since = timestamp - timedelta(minutes=30)
        
        # Check if factory is operating
        is_operating = self.is_within_operating_hours(timestamp)
        
        # If factory not operating, machine should be STOPPED
        if not is_operating and self.current_status != MachineStatus.STOPPED:
            self.current_status = MachineStatus.STOPPED
            self.status_since = timestamp
        
        # If factory is operating but machine is stopped, chance to start setup
        elif is_operating and self.current_status == MachineStatus.STOPPED:
            if random.random() < 0.3:  # 30% chance to start setup when factory is operating
                self.current_status = MachineStatus.SETUP
                self.status_since = timestamp
        
        # Otherwise, use transition probabilities
        else:
            self._update_status(timestamp)
        
        # Return current status data
        return {
            "timestamp": timestamp,
            "metadata": {
                "factoryId": self.factory.id,
                "deviceId": self.device.id,
                "type": "machine_status"
            },
            "status": self.current_status.value,
            "since": self.status_since.isoformat()
        }
    
    def _update_status(self, timestamp):
        """
        Update machine status based on transition probabilities.
        
        Args:
            timestamp: Current timestamp
        """
        # Get transition probabilities for current status
        transition_probs = self.status_probabilities.get(self.current_status, {})
        
        # If no transitions defined, no change
        if not transition_probs:
            return
        
        # Generate random number
        r = random.random()
        
        # Calculate cumulative probability and make transition
        cumulative_prob = 0
        for next_status, prob in transition_probs.items():
            cumulative_prob += prob
            if r < cumulative_prob:
                # If status changes, update status_since
                if next_status != self.current_status:
                    self.current_status = next_status
                    self.status_since = timestamp
                break