from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.entities.client import Client
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
