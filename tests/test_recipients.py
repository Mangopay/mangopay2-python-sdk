import unittest

from mangopay.exceptions import APIError
from mangopay.resources import Recipient, RecipientSchema, PayoutMethod
from mangopay.utils import IndividualRecipient, Address
from tests.test_base import BaseTestLive


class RecipientsTest(BaseTestLive):
    _recipient = None

    def test_create_recipient(self):
        self.create_new_recipient()
        self.assertIsNotNone(RecipientsTest._recipient)
        self.assertIsNotNone(RecipientsTest._recipient.display_name)
        self.assertIsNotNone(RecipientsTest._recipient.payout_method_type)
        self.assertIsNotNone(RecipientsTest._recipient.recipient_type)
        self.assertIsNotNone(RecipientsTest._recipient.currency)
        self.assertIsNotNone(RecipientsTest._recipient.recipient_scope)
        self.assertIsNotNone(RecipientsTest._recipient.user_id)
        self.assertIsNotNone(RecipientsTest._recipient.individual_recipient)
        self.assertIsNotNone(RecipientsTest._recipient.local_bank_transfer)
        self.assertIsNone(RecipientsTest._recipient.international_bank_transfer)
        self.assertIsNone(RecipientsTest._recipient.business_recipient)

    def test_get_recipient(self):
        self.create_new_recipient()
        fetched = Recipient.get(RecipientsTest._recipient.id)

        self.assertIsNotNone(fetched)
        self.assertEqual(RecipientsTest._recipient.id, fetched.id)
        self.assertEqual(RecipientsTest._recipient.status, fetched.status)

    def test_get_user_recipients(self):
        self.create_new_recipient()
        john = BaseTestLive.get_john_sca_owner()
        fetched = Recipient.get_user_recipients(john.id)

        self.assertIsNotNone(fetched)
        self.assertIsInstance(fetched.data, list)
        self.assertTrue(len(fetched.data) > 0)

    def test_get_recipient_schema_local_bank_transfer_individual(self):
        schema = RecipientSchema.get('LocalBankTransfer', 'Individual', 'GBP')

        self.assertIsNotNone(schema)
        self.assertIsNotNone(schema.display_name)
        self.assertIsNotNone(schema.payout_method_type)
        self.assertIsNotNone(schema.recipient_type)
        self.assertIsNotNone(schema.currency)
        self.assertIsNotNone(schema.recipient_scope)
        self.assertIsNotNone(schema.tag)
        self.assertIsNotNone(schema.local_bank_transfer)
        self.assertIsNotNone(schema.individual_recipient)
        self.assertIsNone(schema.business_recipient)
        self.assertIsNone(schema.international_bank_transfer)

    def test_get_recipient_schema_international_bank_transfer_business(self):
        schema = RecipientSchema.get('InternationalBankTransfer', 'Business', 'GBP')

        self.assertIsNotNone(schema)
        self.assertIsNotNone(schema.display_name)
        self.assertIsNotNone(schema.payout_method_type)
        self.assertIsNotNone(schema.recipient_type)
        self.assertIsNotNone(schema.currency)
        self.assertIsNotNone(schema.recipient_scope)
        self.assertIsNotNone(schema.tag)
        self.assertIsNotNone(schema.business_recipient)
        self.assertIsNotNone(schema.international_bank_transfer)
        self.assertIsNone(schema.local_bank_transfer)
        self.assertIsNone(schema.individual_recipient)

    def test_get_payout_methods(self):
        payout_methods = PayoutMethod.get("DE", "EUR")

        self.assertIsNotNone(payout_methods)
        self.assertIsNotNone(payout_methods.available_payout_methods)

    def test_validate(self):
        john = BaseTestLive.get_john_sca_owner()
        recipient = RecipientsTest.get_new_recipient_obj()

        # should pass
        recipient.validate(john.id)

        # should fail
        recipient.individual_recipient = None
        try:
            recipient.validate(john.id)
        except APIError as e:
            self.assertTrue("One or several required parameters are missing or incorrect" in e.content['Message'])

    @unittest.skip("A recipient needs to be manually activated before running the test")
    def test_deactivate(self):
        self.create_new_recipient()
        deactivated = Recipient.deactivate(RecipientsTest._recipient.id)
        fetched = Recipient.get(RecipientsTest._recipient.id)

        self.assertEqual('PENDING', RecipientsTest._recipient.status)
        self.assertEqual('DEACTIVATED', deactivated.status)
        self.assertEqual('DEACTIVATED', fetched.status)

    @staticmethod
    def create_new_recipient():
        if RecipientsTest._recipient is None:
            john = BaseTestLive.get_john_sca_owner()
            recipient = RecipientsTest.get_new_recipient_obj()
            RecipientsTest._recipient = Recipient(**recipient.create(john.id))
        return RecipientsTest._recipient

    @staticmethod
    def get_new_recipient_obj():
        recipient = Recipient()
        recipient.display_name = 'Alex Smith GBP account'
        recipient.payout_method_type = 'LocalBankTransfer'
        recipient.recipient_type = 'Individual'
        recipient.currency = 'GBP'

        individual_recipient = IndividualRecipient()
        individual_recipient.first_name = 'Alex'
        individual_recipient.last_name = 'Smith'
        individual_recipient.address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                               city='City', region='Region',
                                               postal_code='11222', country='FR')
        recipient.individual_recipient = individual_recipient

        recipient.local_bank_transfer = {
            'GBP': {
                'SortCode': '200000',
                'AccountNumber': '55779911'
            }
        }

        return recipient
