from mangopaysdk.tools import enums
import logging
import tempfile


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
    TempPath = tempfile.gettempdir()

    # Constant to switch debug mode (0/1) - display all request and response data
    DebugMode = 0

    # SSL verification (False (no verification) or path to the cacert.pem file)
    SSLVerification = False

    # RestTool class
    # NB: you can swap this class for one of ours that implement some custom logic
    RestToolClass = None

    # Session object from the `requests` library
    Session = None


# we use DEBUG level for internal debugging
if (Configuration.DebugMode):
    logging.basicConfig(level=logging.DEBUG)
