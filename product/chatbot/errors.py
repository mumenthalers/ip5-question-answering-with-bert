class APIException(Exception):
    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.message


class NoQuestionProvidedError(APIException):
    def __init__(self):
        message = 'Question must be provided.'
        super().__init__(412, message)
