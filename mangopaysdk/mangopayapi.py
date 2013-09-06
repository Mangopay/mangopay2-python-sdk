from mangopaysdk.tools import apioauth, apiclients, apiusers, apiwallets, apitransfers, apipayins, apipayouts, apirefunds
from mangopaysdk.configuration import Configuration


class MangoPayApi:

    """MangoPay API main entry point.
    Provides managers to connect, send and read data from MangoPay API
    as well as holds configuration/authorization data.
    """

    def __init__(self):

        #########################################
        # Config/authorization related fields
        #########################################

        # OAuthToken; None by default: will auto-generate it on first API call.
        # Or you can set your own if you want to reuse it until it expires.
        self.OAuthToken = None

        # Configuration instance with default settings (to be reset if required).
        self.Config = Configuration()

        #########################################
        # API managers fields
        #########################################

        self.authenticationManager = apioauth.ApiOAuth(self)
        self.clients = apiclients.ApiClients(self)
        self.users = apiusers.ApiUsers(self)
        self.wallets = apiwallets.ApiWallets(self)
        self.transfers = apitransfers.ApiTransfers(self)
        self.payIns = apipayins.ApiPayIns(self)
        self.payOuts = apipayouts.ApiPayOuts(self)
        self.refunds = apirefunds.ApiRefunds(self)
