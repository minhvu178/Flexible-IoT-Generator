import time
from src.datetime import datetime, timedelta
from src.core.config import Config
from src.core.database import Database
from src.core.logger import setup_logger
from src.core.scheduler import Scheduler
from src.models.factory import Factory
from src.generators.sensor import SensorGenerator
from src.generators.machine_status import MachineStatusGenerator
from src.plugins.plugin_loader import PluginLoader

class Application:
    """Main application class for the data generator."""
    
    def __init__(self, config_path=None):
        self.config = Config(config_path)
        self.logger = setup_logger(self.config.get('general.log_level'))
        self.db = Database(self.config.get('general.data_persistence'))
        self.scheduler = Scheduler()
        self.factories = self._initialize_factories()
        self.generators = self._initialize_generators()
        self.plugins = PluginLoader.load_plugins()
        
    def _initialize_factories(self):
        """Initialize factory objects from src.configuration."""
        factories = []
        for factory_config in self.config.get('factories'):
            factory = Factory.from_config(factory_config)
            factories.append(factory)
        return factories
    
    def _initialize_generators(self):
        """Initialize all data generators."""
        generators = []
        
        for factory in self.factories:
            for device in factory.devices:
                # Add machine status generator for each device
                generators.append(MachineStatusGenerator(
                    self.config, factory, device
                ))
                
                # Add sensor generators for each sensor
                for sensor in device.sensors:
                    generators.append(SensorGenerator(
                        self.config, factory, device, sensor
                    ))
        
        return generators
    
    def generate_data(self, timestamp):
        """Generate all data for the given timestamp."""
        data = []
        for generator in self.generators:
            generated = generator.generate(timestamp)
            if generated:
                data.append(generated)
        
        # Generate data from src.plugins
        # ... implementation ...
        
        return data
    
    def persist_data(self, data):
        """Store generated data."""
        if data:
            self.db.insert_many(data)
    
    def run(self):
        """Run the simulation."""
        self.logger.info("Starting data generation...")
        
        start_date = self.config.get_datetime('simulation.start_date')
        end_date = self.config.get_datetime('simulation.end_date') or datetime.now()
        interval_ms = self.config.get('simulation.update_interval_ms')
        acceleration = self.config.get('simulation.time_acceleration')
        
        # Historical data generation
        current = start_date
        while current < end_date:
            data = self.generate_data(current)
            self.persist_data(data)
            current += timedelta(milliseconds=interval_ms * acceleration)
        
        # Real-time data generation
        self.scheduler.schedule(
            interval_ms / 1000.0, 
            self._generate_realtime_data
        )
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.scheduler.stop()
            self.logger.info("Data generation stopped.")
    
    def _generate_realtime_data(self):
        """Generate data for current timestamp."""
        now = datetime.now()
        data = self.generate_data(now)
        self.persist_data(data)