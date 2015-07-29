from datetime import datetime


class UrlTool:

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    def __init__ (self, config):
       """Constructor.
       param MangoPayApi Root/parent instance that holds the OAuthToken and Configuration instance
       """
       self._config = config

    def GetRestUrl(self, urlKey, addClientId = True, pagination = None, additionalUrlParams = None):

        if not addClientId:
            url = '/v2.01' + urlKey
        else:
            url = '/v2.01/' + self._config.ClientID + urlKey

            if pagination != None:
                url += '?page=' + str(pagination.Page) + '&per_page=' + str(pagination.ItemsPerPage)

            if additionalUrlParams != None:
                url += "&" if (url.count("?") > 0) else "?"

                if 'sort' in additionalUrlParams:
                    url += "%s=%s&" %(additionalUrlParams['sort'][0], additionalUrlParams['sort'][1])

                if 'filter' in additionalUrlParams:
                    for key, val in additionalUrlParams['filter'].__dict__.items():
                        url += "%s=%s&" %(key,val)
                    #url += "filter=%s&" %(additionalUrlParams['filter'])

                # avoid urlparse because of 2.7 compatibility issues
                #for key, val in additionalUrlParams.__dict__.items():
                #    url += "%s=%s&" %(key,val)
                url = url[:-1]
                
        return url

    def GetFullUrl(self, restUrl):
        return self._getHost() + restUrl

    def _getHost(self):
        baseUrl = self._config.BaseUrl
        #remove '/' from end baseurl
        if baseUrl[-1] == '/':
            baseUrl = baseUrl[0: -1]

        return baseUrl
