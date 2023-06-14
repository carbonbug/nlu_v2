class NluException(Exception):
    def __init__(self, code, message="Salary is not in (5000, 15000) range"):
        self.code = code
        self.message = message
        super().__init__(self.message)
    @staticmethod
    def raise_nlu_exception(nlu_exception):
        raise NluException(message=nlu_exception["message"], code=nlu_exception["code"])

