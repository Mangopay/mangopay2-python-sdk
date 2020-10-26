import base64
import os
import random

from mangopay.resources import Client, ClientLogo, Address, BankWirePayOut, ClientWallet
from mangopay.utils import Money
from tests.test_base import BaseTestLive


class ClientsTestLive(BaseTestLive):

    def test_ClientGet(self):
        client = Client.get()

        self.assertIsNotNone(client)
        self.assertEqual('sdk-unit-tests', client.client_id)

    # def test_ClientUpdate(self):
    #     phone_number = str('+33123456789')
    #     client = Client.get()
    #     client.primary_button_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    #     client.primary_theme_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    #     client.headquarters_phone_number = phone_number
    #     new_client = client.update()
    #
    #     self.assertIsNotNone(new_client)
    #     self.assertEqual(client.primary_button_colour, new_client['primary_button_colour'])
    #     self.assertEqual(client.primary_theme_colour, new_client['primary_theme_colour'])
    #     self.assertEqual(client.headquarters_phone_number, phone_number, "Headquarter's phone number was not updated "
    #                                                                      "correctly")

    def test_LogoUpload(self):
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'TestKycPageFile.png')
        with open(file_path, 'rb') as f:
            data = f.read()
            encoded_file = base64.b64encode(data)

        client_logo = ClientLogo()
        client_logo.file = encoded_file
        client_logo.upload()

    def test_create_bank_account(self):
        account = BaseTestLive.get_client_bank_account()
        self.assertIsNotNone(account)
        self.assertIsNotNone(account.id)

    def test_create_payout(self):
        account = BaseTestLive.get_client_bank_account()
        payout = BankWirePayOut()
        wallets = ClientWallet.all()

        payout.debited_funds = Money()
        payout.debited_funds.currency = 'EUR'
        payout.debited_funds.amount = 12

        payout.bank_account = account
        payout.debited_wallet = wallets[0]
        payout.bank_wire_ref = 'invoice 7282'

        created_payout = BankWirePayOut(**payout.create_client_payout())

        self.assertIsNotNone(created_payout)
        self.assertIsNotNone(created_payout.id)