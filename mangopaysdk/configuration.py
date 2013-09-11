from mangopaysdk.tools import enums


class Configuration:
    """Configuration class for MangoPay API SDK.
    All fields are required.
    """

    # Setting for client: client Id and client password
    ClientID = ''
    ClientPassword = ''

    # Base URL to MangoPay API
    BaseUrl = 'https://mangopay-api-inte.leetchi.com'

    # path to temp - required to cache auth tokens
    TempPath = "c:\Temp\\"

    # Constant to switch debug mode (0/1) - display all request and response data
    DebugMode = 0

    #AuthenticationType = enums.AuthenticationType.Strong

# we use DEBUG level for internal debugging
if (Configuration.DebugMode):
    import logging
    logging.basicConfig(level=logging.DEBUG)
