import logging
import os

class LoggingManager:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger("NewsExtractorLogger")
        self.logger.setLevel(logging.INFO)

        log_dir = os.path.dirname(log_file_path)
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        set.logger.addHandler(file_handler)
    
    def log_info(self, message):
        self.logger.info(message)
    
    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
        
