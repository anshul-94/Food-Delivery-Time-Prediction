import sys

class CustomException(Exception):
    """
    Custom Exception class for the project.
    Provides detailed error information including
    file name and line number.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)

        _, _, exc_tb = error_detail.exc_info()

        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno

        self.error_message = (
            f"Error occurred in Python script:\n"
            f"File Name: {self.file_name}\n"
            f"Line Number: {self.line_number}\n"
            f"Error Message: {error_message}"
        )

    def __str__(self):
        return self.error_message
