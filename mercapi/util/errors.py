class MercapiError(Exception):
    pass


class ParseAPIResponseError(MercapiError):
    pass


class IncorrectRequestError(MercapiError):
    pass
