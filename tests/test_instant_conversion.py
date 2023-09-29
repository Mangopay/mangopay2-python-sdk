from mangopay.utils import Money
from tests.resources import ConversionRate, InstantConversion, Wallet
from tests.test_base import BaseTestLive


class InstantConversionTest(BaseTestLive):

    def test_get_conversion_rate(self):
        conversion_rate = ConversionRate()
        conversion_rate.debited_currency = 'EUR'
        conversion_rate.credited_currency = 'GBP'

        complete_conversion_rate = conversion_rate.get_conversion_rate()

        self.assertIsNotNone(complete_conversion_rate)
        self.assertIsNotNone(complete_conversion_rate.data[0].client_rate)
        self.assertIsNotNone(complete_conversion_rate.data[0].market_rate)

    def test_create_instant_conversion(self):
        user = BaseTestLive.get_john()

        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'GBP'
        credited_wallet.description = 'WALLET IN GBP'
        credited_wallet = Wallet(**credited_wallet.save())

        credited_funds = Money()
        credited_funds.currency = 'GBP'

        debited_funds = Money()
        debited_funds.currency = 'EUR'
        debited_funds.amount = 79

        instant_conversion = InstantConversion()
        instant_conversion.author = user
        instant_conversion.credited_wallet = credited_wallet
        instant_conversion.debited_wallet = BaseTestLive.create_new_wallet_with_money()
        instant_conversion.credited_funds = credited_funds
        instant_conversion.debited_funds = debited_funds
        instant_conversion.tag = "instant conversion test"

        instant_conversion_response = instant_conversion.create_instant_conversion()

        self.assertIsNotNone(instant_conversion_response)
        self.assertIsNotNone(instant_conversion_response['debited_funds'].amount)
        self.assertIsNotNone(instant_conversion_response['credited_funds'].amount)
        self.assertEqual(instant_conversion_response['status'], 'SUCCEEDED')

    def test_get_instant_conversion(self):
        user = BaseTestLive.get_john()

        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'GBP'
        credited_wallet.description = 'WALLET IN GBP'
        credited_wallet = Wallet(**credited_wallet.save())

        credited_funds = Money()
        credited_funds.currency = 'GBP'

        debited_funds = Money()
        debited_funds.currency = 'EUR'
        debited_funds.amount = 79

        instant_conversion = InstantConversion()
        instant_conversion.author = user
        instant_conversion.credited_wallet = credited_wallet
        instant_conversion.debited_wallet = BaseTestLive.create_new_wallet_with_money()
        instant_conversion.credited_funds = credited_funds
        instant_conversion.debited_funds = debited_funds
        instant_conversion.tag = "instant conversion test"

        instant_conversion_response = instant_conversion.create_instant_conversion()
        returned_conversion_response = InstantConversion.get_instant_conversion(instant_conversion_response['id'])

        self.assertIsNotNone(returned_conversion_response)
        self.assertIsNotNone(returned_conversion_response.data[0])
        self.assertIsNotNone(returned_conversion_response.data[0].debited_funds.amount)
        self.assertIsNotNone(returned_conversion_response.data[0].credited_funds.amount)
        self.assertEqual(returned_conversion_response.data[0].status, 'SUCCEEDED')
