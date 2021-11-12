from typing import List, Dict


class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result data model
        :param status_code: HTTP Status Code
        :param message: General message about the result
        :param data: a List of Dictionaries
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []
