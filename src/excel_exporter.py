import os
from openpyxl import Workbook


class ExcelExporter:
    def __init__(self, output_file_path, logging_manager):
        """
        Initializes an ExcelExporter instance.

        Args:
            output_file_path (str): The path to the output Excel file.
            logging_manager (LoggingManager): An instance of the LoggingManager class.
        """
        self.output_file_path = output_file_path
        self.logging_manager = logging_manager
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def write_headers(self, headers):
        """
        Writes the provided headers to the first row of the Excel sheet.

        Args:
            headers (list): A list of header strings to be written.
        """
        self.worksheet.append(headers)

    def write_row(self, row_data):
        """
        Writes a row of data to the Excel sheet.

        Args:
            row_data (list): A list of values to be written in a new row.
        """
        self.worksheet.append(row_data)

    def save_workbook(self):
        """
        Saves the workbook to the specified output file path.
        """
        try:
            self.workbook.save(self.output_file_path)
            self.logging_manager.log_info(f"Excel file saved: {self.output_file_path}")
        except Exception as e:
            self.logging_manager.log_error(f"Error saving Excel file: {str(e)}")
