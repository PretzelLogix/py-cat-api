from typing import List, Dict


class Result:
    def __init__(self, success: bool, status_code: int, message: str = '', data: List[Dict] = None):
        self.success = bool(success)
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []
