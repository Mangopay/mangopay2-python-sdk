from mangopaysdk.types.exceptions.mangopayexception import MangoPayException


class ResponseException(MangoPayException):
    """ Exceptions that come as responses to from API calls."""

    def __init__(self, requestUrl, responseCode, errorMessage = None):
        self.RequestUrl = requestUrl
        self.Code = responseCode
        self.Message = errorMessage

    def __str__(self):
        return str(self.Message)
