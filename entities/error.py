class ErrorMessage:
    def __init__(self, message : str, code : int):
        self.message = message
        self.code = code

    def get_message(self):
        if self.message is "":
           return ""
        return "The following error occurred : " + self.message

    def get_code(self) -> int:
        return self.code
    
    def set_code(self, code : int):
        self.code = code

    def set_message(self, message : str):
        self.message = message