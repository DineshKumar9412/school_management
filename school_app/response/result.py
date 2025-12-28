class Result:
    def __init__(self, code: int, message: str, extra: dict = None):
        self.code = code
        self.message = message
        self.extra = extra if extra is not None else {}

    def http_response(self):
        return {
            "code": self.code,
            "message": self.message,
            "result": self.extra
        }
