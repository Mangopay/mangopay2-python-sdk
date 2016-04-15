from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.entities.client import Client
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.tools.enums import *
from random import randint
import os


class Test_ApiClients(TestBase):

    def test_Clients_CreateClient(self):        
        id = str(randint(1000000000000, 9999999999999))
        client = self.sdk.clients.Create(id, 'test', 'test@o2.pl')
        self.assertTrue(client.Name == 'test')
        self.assertTrue(client.Email == 'test@o2.pl')

    def test_Clients_TryCreateInvalidClient(self):
        with self.assertRaises(ResponseException) as cm:
            # invalid id
            client = self.sdk.clients.Create('0', 'test', 'test@o2.pl')

    def test_Clients_Get(self):
        client = self.sdk.clients.Get()

        self.assertIsNotNone(client)
        self.assertTrue(client.ClientId == 'sdk-unit-tests')

    def test_Clients_Update(self):
        client = self.sdk.clients.Get()

        color1 = str(randint(100000, 999999))
        color2 = str(randint(100000, 999999))

        client.PrimaryButtonColour = '#' + color1
        client.PrimaryThemeColour = '#' + color2

        clientNew = self.sdk.clients.Update(client)

        self.assertIsNotNone(clientNew)
        self.assertTrue(clientNew.PrimaryButtonColour == '#' + color1)
        self.assertTrue(clientNew.PrimaryThemeColour == '#' + color2)

    def test_Clients_Logo(self):
        self.sdk.clients.UploadLogo(os.path.join(os.path.dirname(__file__), "TestKycPageFile.png"))

    def test_Clients_GetWallets(self):
        feesWallets = self.sdk.clients.GetWallets(FundsType.FEES, Pagination(1, 1))
        creditWallets = self.sdk.clients.GetWallets(FundsType.CREDIT, Pagination(1, 1))

        self.assertIsNotNone(feesWallets)
        self.assertIsNotNone(creditWallets)

    def test_Clients_GetWallet(self):
        feesWallets = self.sdk.clients.GetWallets(FundsType.FEES, Pagination(1, 1))
        creditWallets = self.sdk.clients.GetWallets(FundsType.CREDIT, Pagination(1, 1))
        defaultWallets = self.sdk.clients.GetWallets(FundsType.DEFAULT, Pagination(1, 1))

        if (feesWallets == None or len(feesWallets) == 0 or creditWallets == None or len(creditWallets) == 0 or defaultWallets == None or len(defaultWallets) == 0):
            self.assertIsTrue(False, "Cannot test getting client's wallet because there is no any wallet for client.")

        wallet = None
        result = None
        if (feesWallets != None and len(feesWallets) > 0):
            wallet = feesWallets[0]
        else:
            if (creditWallets != None and len(creditWallets) > 0):
                wallet = creditWallets[0]
            else:
                wallet = defaultWallets[0]

        result = self.sdk.clients.GetWallet(wallet.FundsType, wallet.Currency)

        self.assertIsNotNone(result)
        self.assertTrue(result.FundsType == wallet.FundsType)
        self.assertTrue(result.Currency == wallet.Currency)

    def test_Clients_GetWalletTransactions(self):
        feesWallets = self.sdk.clients.GetWallets(FundsType.FEES, Pagination(1, 1))
        creditWallets = self.sdk.clients.GetWallets(FundsType.CREDIT, Pagination(1, 1))
        defaultWallets = self.sdk.clients.GetWallets(FundsType.DEFAULT, Pagination(1, 1))

        if (feesWallets == None or len(feesWallets) == 0 or creditWallets == None or len(creditWallets) == 0 or defaultWallets == None or len(defaultWallets) == 0):
            self.assertTrue(False, "Cannot test getting client's wallet because there is no any wallet for client.")

        wallet = None
        result = None
        if (feesWallets != None and len(feesWallets) > 0):
            wallet = feesWallets[0]
        else:
            if (creditWallets != None and len(creditWallets) > 0):
                wallet = creditWallets[0]
            else:
                wallet = defaultWallets[0]

        result = self.sdk.clients.GetWalletTransactions(wallet.FundsType, wallet.Currency)

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)