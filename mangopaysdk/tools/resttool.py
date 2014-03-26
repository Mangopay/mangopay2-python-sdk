import requests, json, logging
from mangopaysdk.tools.authenticationHelper import AuthenticationHelper
from mangopaysdk.tools.urltool import UrlTool
from mangopaysdk.types.exceptions.responseexception import ResponseException
import sys


class BaseRestTool(object):
    """Class to prepare HTTP request, call the request and decode the response."""

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    # Request type for current request
    _requestType = ""

    # bool variable to flag that in request authentication data are required
    _authRequired = True

    # Array with HTTP header to send with request
    _requestHttpHeaders = {}

    # Array with data to pass in the request
    _requestData = []

    # Code get from response
    _responseCode = 0

    # bool variable to switch on/off log debugging
    _debugMode = False

    def __init__(self, root = None, authRequired = True):
        """Constructor.
        param bool authRequired Variable to flag that in request the authentication data are required
        param MangoPayApi Root/parent instance that holds the OAuthToken and Configuration instance
        """
        self._authRequired = authRequired
        self._root = root
        self._debugMode = self._root.Config.DebugMode

    def Request(self, urlMethod, requestType, requestData = None, pagination = None, additionalUrlParams = None):
        """Call request to MangoPay API.
        param string urlMethod Type of method in REST API
        param MangoPay requestType Type of request
        param array requestData Data to send in request
        param MangoPay pagination Pagination object
        return object Response data
        """
        self._requestType = requestType
        self._requestData = requestData

        response = self._runRequest(urlMethod, pagination, additionalUrlParams)

        return response

    def _runRequest(self, urlMethod, pagination, additionalUrlParams):
        """Execute request and check response.
        return object Respons data
        throws Exception If cURL has error
        """

        urlToolObj = UrlTool(self._root.Config)
        restUrl = urlToolObj.GetRestUrl(urlMethod, self._authRequired, pagination, additionalUrlParams)
        fullUrl = urlToolObj.GetFullUrl(restUrl)

        authObj = AuthenticationHelper(self._root).GetRequestAuthObject(self._authRequired)

        headers = {"Content-Type" : "application/x-www-form-urlencoded", 'Connection':'close'}
        headersJson = {"Content-Type" : "application/json", 'Connection':'close'}

        if (self._debugMode): logging.getLogger(__name__).debug('REQUEST: {0} {1}\n  DATA: {2}'.format(self._requestType, fullUrl, self._requestData))

        if self._requestType == "POST":
            response = requests.post(fullUrl, json.dumps(self._requestData), auth = authObj, verify=False, headers=headersJson)
        elif self._requestType == "GET":
            response = requests.get(fullUrl, auth = authObj, verify=False)
        elif self._requestType == "PUT":
            response = requests.put(fullUrl, json.dumps(self._requestData), auth = authObj, verify=False, headers=headersJson)  
        elif self._requestType == "DELETE":
            response = requests.delete(fullUrl, auth = authObj, verify=False, headers=headers)
        
        if (self._debugMode): logging.getLogger(__name__).debug('RESPONSE: {0}\n  {1}\n  {2}'.format(response.status_code, response.headers, response.text))

        decodedResp = json.loads(response.text) if (response.text != '' and 'application/json' in response.headers['content-type']) else None
        self._checkResponseCode(response, decodedResp)

        # load pagination info
        if not pagination == None:
            if ('x-number-of-pages' in response.headers.keys()):
                pagination.TotalPages = int(response.headers['x-number-of-pages'])
            if ('x-number-of-items' in response.headers.keys()):
                pagination.TotalItems = int(response.headers['x-number-of-items'])

        #try:
        #    if not pagination == None:
        #        pagination.TotalPages = int(response.headers['x-number-of-pages'])
        #except:
        #    pagination.TotalPages = 1
        #    if self._debugMode:
        #        logging.getLogger(__name__).debug(sys.exc_info()[0])
        #else:
        #    try:
        #        if not pagination == None:
        #            pagination.TotalItems = int(response.headers['x-number-of-items'])
        #    except:
        #        pagination.TotalItems = 0
        #        if self._debugMode:
        #            logging.getLogger(__name__).debug(sys.exc_info()[0])


        # this can hit create connection performance
        # response.connection.close()
        return decodedResp

    def _checkResponseCode(self, response, decodedResp):
        """Check response code.
        param object response Response from REST API
        @throws RequestException If response code not OK
        """
        
        if response.status_code != requests.codes.ok and response.status_code != requests.codes.no_content:
            message = str(response.status_code)
            if decodedResp != None and decodedResp.get('Message') != None:
                message = decodedResp.get('Message')
            elif decodedResp != None and decodedResp.get('error') != None:
                message = decodedResp.get('error')
            raise ResponseException(response.request.url, response.status_code, message)


def _getRestTool(root, *args, **kwargs):
        RestToolClass = root.Config.RestToolClass
        if RestToolClass is None:
            RestToolClass = BaseRestTool

        # in the case the user swap for his own class, check it's good enough
        if not issubclass(RestToolClass, BaseRestTool):
            raise ValueError("You've swapped the `Configuration.RestToolClass` "
                             "for you own but you need `%s` to subclass "
                             "the original class `%s`" % (RestToolClass,
                                                          BaseRestTool))

        return RestToolClass(root, *args, **kwargs)


class RestToolProxy(object):
    """
    Wrapper around the `BaseRestTool` class
    It decides which class should be used based on the `root.Config.RestToolClass`
    And then proxies the calls to the wrapped class instance
    """

    def __init__(self, root, *args, **kwargs):
        resttool = _getRestTool(root, *args, **kwargs)
        self._resttool = resttool

    def __getattribute__(self, attr):
        return getattr(object.__getattribute__(self, '_resttool'), attr)


# for easy backward compatibility we use the proxy as the main class
RestTool = RestToolProxy
