import argparse
import os
from src.app import Application

def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description='Flexible IoT Data Generator')
    parser.add_argument('--config', help='Path to configuration file')
    args = parser.parse_args()
    
    # Get configuration path
    config_path = args.config
    if config_path and not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        return
    
    # Create and run application
    app = Application(config_path)
    app.run()

if __name__ == '__main__':
    main()