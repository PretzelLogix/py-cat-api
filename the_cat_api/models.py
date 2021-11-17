from typing import List, Dict


class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Fact:
    def __init__(self, id: str, text: str, language_code: str, breed_id: str):
        self.id = id
        self.text = text
        self.language_code = language_code
        self.breed_id = breed_id
