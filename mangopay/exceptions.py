class APIError(Exception):
    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code', None)
        self.url = kwargs.pop('url', None)
        self.content = kwargs.pop('content', None)
        self.headers = kwargs.pop('headers', None)

        super(APIError, self).__init__(*args, **kwargs)


class DecodeError(APIError):
    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('body', None)
        self.headers = kwargs.pop('headers', None)
        self.url = kwargs.pop('url', None)
        self.content = kwargs.pop('content', None)

        super(DecodeError, self).__init__(*args, **kwargs)


class AuthenticationError(APIError):
    pass


class CurrencyMismatch(Exception):
    pass
