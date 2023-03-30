class MercapiError(BaseException):
    pass


class ParseAPIResponseError(MercapiError):
    pass


class IncorrectRequestError(MercapiError):
    pass
