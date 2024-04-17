import os
from openpyxl import Workbook

class ExcelExporter:
    def __init__(self, output_file_path, logging_manager):
        self.output_file_path = output_file_path
        self.logging_manager = logging_manager
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    
    def write_headers(self, headers):
        self.worksheet.append(headers)

    def write_row(self, row_data):
        self.worksheet.append(row_data)
    
    def save_workbook(self):
        try:
            self.workbook.save(self.output_file_path)
            self.logging_manager.log_info(f'Excel file saved: {self.output_file_path}')
        except Exception as e:
            self.logging_manager.log_error(f'Error saving Excel file: {str(e)}')