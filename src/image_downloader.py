import os
import requests


class ImageDownloader:
    def __init__(self, output_directory, logging_manager):
        """
        Initializes an ImageDownloader instance.

        Args:
            output_directory (str): The path to the output directory for downloaded images.
            logging_manager (LoggingManager): An instance of the LoggingManager class.
        """
        self.output_directory = output_directory
        self.logging_manager = logging_manager
        os.makedirs(output_directory, exist_ok=True)

    def download_image(self, image_url, filename):
        """
        Downloads an image from the specified URL and saves it with the given filename.

        Args:
            image_url (str): The URL of the image to be downloaded.
            filename (str): The filename to use for saving the downloaded image.

        Returns:
            str: The filename of the downloaded image if successful, None otherwise.
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            file_path = os.path.join(self.output_directory, filename)
            with open(file_path, "wb") as file:
                file.write(response.content)
            self.logging_manager.log_info(f"Downloaded image: {filename}")
            return filename
        except Exception as e:
            self.logging_manager.log_error(f"Error downloading image: {str(e)}")
            return None
