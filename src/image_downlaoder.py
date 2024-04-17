import os
import requests

class ImageDownloader:
    def __init__(self, output_directory, logging_manager):
        self.output_directory = output_directory
        self.logging_manager = logging_manager

        os.makedirs(output_directory, exist_ok=True)

    def download_image(self, image_url, filename):
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            file_path = os.path.join(self.output_directory, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            self.logging_manager.log_info(f'Downloaded image: {filename}')
            return filename
        except Exception as e:
            self.logging_manager.log_error(f'Error downloading image: {str(e)}')
            return None