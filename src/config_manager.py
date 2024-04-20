import yaml


class ConfigManager:
    def __init__(self, config_file_path, logging_manager):
        """
        Initializes a ConfigManager instance.

        Args:
            config_file_path (str): The path to 
            the configuration file.
        """
        self.config_file_path = config_file_path
        self.logging_manager = logging_manager
        self.logging_manager.log_info(f"Loading configs from {self.config_file_path}")
        self.config = self.load_config()

    def load_config(self):
        """
        Loads the configuration from the specified file.

        Returns:
            dict: The loaded configuration data, or 
            an empty dictionary if an error occurred.
        """
        try:
            with open(self.config_file_path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logging_manager.log_error(f"Error loading config file: {str(e)}")
            return {}

    def get_config_value(self, key):
        """
        Retrieves the value for the specified key from the configuration.

        Args:
            key (str): The key for which to retrieve the value.

        Returns:
            Any: The value associated with the key, or 
            None if the key is not found or an error occurred.
        """
        try:
            return self.config[key]
        except Exception as e:
            self.logging_manager.log_error(f"Error getting config value: {str(e)}")
            return None
