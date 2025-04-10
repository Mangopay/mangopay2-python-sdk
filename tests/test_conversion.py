from mangopay.resources import ConversionQuote, QuotedConversion, InstantConversion
from mangopay.utils import Money
from tests.resources import ConversionRate, Conversion, Wallet
from tests.test_base import BaseTestLive


class ConversionsTest(BaseTestLive):

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
        instant_conversion.debited_wallet = BaseTestLive.create_new_wallet_with_money(user)
        instant_conversion.credited_funds = credited_funds
        instant_conversion.debited_funds = debited_funds
        instant_conversion.fees = Money(amount=9, currency='EUR')
        instant_conversion.tag = "instant conversion test"

        instant_conversion_response = instant_conversion.save()

        self.assertIsNotNone(instant_conversion_response)
        self.assertIsNotNone(instant_conversion_response['debited_funds'].amount)
        self.assertIsNotNone(instant_conversion_response['credited_funds'].amount)
        self.assertIsNotNone(instant_conversion_response['fees'].amount)
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
        instant_conversion.debited_wallet = BaseTestLive.create_new_wallet_with_money(user)
        instant_conversion.credited_funds = credited_funds
        instant_conversion.debited_funds = debited_funds
        instant_conversion.tag = "instant conversion test"

        instant_conversion_response = instant_conversion.save()
        returned_conversion_response = Conversion.get_conversion(instant_conversion_response['id'])

        self.assertIsNotNone(returned_conversion_response)
        self.assertIsNotNone(returned_conversion_response.data[0])
        self.assertIsNotNone(returned_conversion_response.data[0].debited_funds.amount)
        self.assertIsNotNone(returned_conversion_response.data[0].credited_funds.amount)
        self.assertEqual(returned_conversion_response.data[0].status, 'SUCCEEDED')

    def test_create_conversion_quote(self):
        conversion_quote = ConversionQuote()
        conversion_quote.credited_funds = Money(currency='USD', amount=None)
        conversion_quote.debited_funds = Money(currency='GBP', amount=100)
        conversion_quote.duration = 300
        conversion_quote.tag = "Created using the Mangopay Python SDK"

        created_conversion_quote = conversion_quote.create_conversion_quote()

        self.assertIsNotNone(created_conversion_quote)
        self.assertIsNotNone(created_conversion_quote['debited_funds'])
        self.assertIsNotNone(created_conversion_quote['credited_funds'])
        self.assertIsNotNone(created_conversion_quote['conversion_rate'])
        self.assertEqual('ACTIVE', created_conversion_quote['status'])

    def test_get_conversion_quote(self):
        conversion_quote = ConversionQuote()
        conversion_quote.credited_funds = Money(currency='USD', amount=None)
        conversion_quote.debited_funds = Money(currency='GBP', amount=100)
        conversion_quote.duration = 300
        conversion_quote.tag = "Created using the Mangopay Python SDK"

        created_conversion_quote = conversion_quote.create_conversion_quote()
        returned_conversion_quote = ConversionQuote.get_conversion_quote(created_conversion_quote['id'])
        response = returned_conversion_quote.data[0]
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.debited_funds)
        self.assertIsNotNone(response.credited_funds)
        self.assertIsNotNone(response.conversion_rate)
        self.assertEqual('ACTIVE', response.status)

    def test_create_quoted_conversion(self):
        user = BaseTestLive.get_john()

        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'GBP'
        credited_wallet.description = 'WALLET IN GBP'
        credited_wallet = Wallet(**credited_wallet.save())
        debited_wallet = BaseTestLive.create_new_wallet_with_money(user)

        conversion_quote = ConversionQuote()
        conversion_quote.credited_funds = Money(currency='GBP', amount=None)
        conversion_quote.debited_funds = Money(currency='EUR', amount=50)
        conversion_quote.duration = 300
        conversion_quote.tag = "Created using the Mangopay Python SDK"
        created_conversion_quote = conversion_quote.create_conversion_quote()

        quoted_conversion = QuotedConversion()
        quoted_conversion.quote_id = created_conversion_quote['id']
        quoted_conversion.author_id = debited_wallet.owners_ids[0]
        quoted_conversion.credited_wallet = credited_wallet
        quoted_conversion.debited_wallet = debited_wallet

        response = quoted_conversion.save()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['debited_funds'].amount)
        self.assertIsNotNone(response['credited_funds'].amount)
        self.assertEqual(response['status'], 'SUCCEEDED')

    def test_get_quoted_conversion(self):
        user = BaseTestLive.get_john()

        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'GBP'
        credited_wallet.description = 'WALLET IN GBP'
        credited_wallet = Wallet(**credited_wallet.save())
        debited_wallet = BaseTestLive.create_new_wallet_with_money(user)

        conversion_quote = ConversionQuote()
        conversion_quote.credited_funds = Money(currency='GBP', amount=None)
        conversion_quote.debited_funds = Money(currency='EUR', amount=50)
        conversion_quote.duration = 300
        conversion_quote.tag = "Created using the Mangopay Python SDK"
        created_conversion_quote = conversion_quote.create_conversion_quote()

        quoted_conversion = QuotedConversion()
        quoted_conversion.quote_id = created_conversion_quote['id']
        quoted_conversion.author_id = debited_wallet.owners_ids[0]
        quoted_conversion.credited_wallet = credited_wallet
        quoted_conversion.debited_wallet = debited_wallet

        created_quoted_conversion = quoted_conversion.save()
        response = Conversion.get_conversion(created_quoted_conversion['id'])
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data[0])
        self.assertIsNotNone(response.data[0].debited_funds.amount)
        self.assertIsNotNone(response.data[0].credited_funds.amount)
        self.assertEqual(response.data[0].status, 'SUCCEEDED')
