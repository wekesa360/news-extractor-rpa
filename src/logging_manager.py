import logging
import os


class LoggingManager:
    def __init__(self, log_file_path):
        """
        Initializes a LoggingManager instance.

        Args:
            log_file_path (str): The path to the log file.
        """
        self.log_file_path = log_file_path
        self.logger = logging.getLogger("NewsExtractorLogger")
        self.logger.setLevel(logging.INFO)
        log_dir = os.path.dirname(log_file_path)
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        """
        Logs an informational message.

        Args:
            message (str): The message to be logged.
        """
        self.logger.info(message)

    def log_warning(self, message):
        """
        Logs a warning message.

        Args:
            message (str): The warning message to be logged.
        """
        self.logger.warning(message)

    def log_error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The error message to be logged.
        """
        self.logger.error(message)
