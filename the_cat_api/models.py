from typing import List, Dict


class Result:
    def __init__(self, success: bool, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param success: True if HTTP Request was successful, False if not
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.success = bool(success)
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []
