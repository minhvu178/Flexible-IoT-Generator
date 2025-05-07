# src/core/logger.py
import logging
import os
from datetime import datetime

def setup_logger(log_level='INFO', log_dir='logs'):
    """
    Set up and configure the logger.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('flexible_iot_generator')
    
    # Set log level
    log_level_value = getattr(logging, log_level.upper())
    logger.setLevel(log_level_value)
    
    # Create file handler with timestamp in filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f'generator_{timestamp}.log')
    file_handler = logging.FileHandler(log_file)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Configure handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger