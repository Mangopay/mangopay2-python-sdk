from mangopaysdk.tools import enums
import logging


class Configuration:
    """Configuration class for MangoPay API SDK.
    All fields are required.
    """

    # Setting for client: client Id and client password
    ClientID = ''
    ClientPassword = ''

    # Base URL to MangoPay API
    BaseUrl = 'https://api.sandbox.mangopay.com'

    # path to temp - required to cache auth tokens
    TempPath = "c:\Temp\\"

    # Constant to switch debug mode (0/1) - display all request and response data
    DebugMode = 0

    #AuthenticationType = enums.AuthenticationType.Strong

    # RestTool class
    # NB: you can swap this class for one of ours that implement some custom logic
    RestToolClass = None


# we use DEBUG level for internal debugging
if (Configuration.DebugMode):
    logging.basicConfig(level=logging.DEBUG)
