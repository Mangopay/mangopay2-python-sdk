from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool


class ApiIdempotency(ApiBase):
    """MangoPay API methods for idempotency."""

    def Get(self, idempotencyKey = None):
        """Get idempotency response object
        param string Idempotency key
        return IdempotencyResponse from API
        """
        return self._getObject('idempotency_response_get', idempotencyKey)