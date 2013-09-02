from datetime import datetime
import urllib


class UrlTool:

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    def __init__ (self, root):
       """Constructor.
       param MangoPayApi Root/parent instance that holds the OAuthToken and Configuration instance
       """
       self._root = root

    def GetRestUrl(self, urlKey, addClientId = True, pagination = None, additionalUrlParams = None):

        if not addClientId:
            url = '/v2' + urlKey
        else:
            url = '/v2/' + self._root.Config.ClientID + urlKey

            if pagination != None:
                url += '?page=' + str(pagination.Page) + '&per_page=' + str(pagination.ItemsPerPage)

            if additionalUrlParams != None:
                url += "&" if (url.count("?") > 0) else "?"
                url += urllib.parse.urlencode(additionalUrlParams.__dict__)
 
        return url

    def GetFullUrl(self, restUrl):
        return self._getHost() + restUrl

    def _getHost(self):
        baseUrl = self._root.Config.BaseUrl
        #remove '/' from end baseurl
        if baseUrl[-1] == '/':
            baseUrl = baseUrl[0: -1]

        return baseUrl
