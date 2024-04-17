import yaml


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()

    
    def load_config(self):
        try:
            with open(self.config_file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f'Error loading config file: {str(e)}')
            return {}
        
    def get_config_value(self, key):
        try:
            return self.config[key]
        except Exception as e:
            print(f'Error getting config value: {str(e)}')
            return None