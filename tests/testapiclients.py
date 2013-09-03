from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.tools.enums import *
from random import randint


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