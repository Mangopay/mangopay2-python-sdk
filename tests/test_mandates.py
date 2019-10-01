from mangopay.resources import Mandate
from tests.test_base import BaseTestLive


class MandatesTestLive(BaseTestLive):

    def test_Mandate_Create(self):
        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account().id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'FR'
        mandate = Mandate(**mandate.save())

        self.assertIsNotNone(mandate)
        self.assertTrue(mandate.id)

    def test_Mandate_Get(self):
        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account().id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'FR'
        mandate_created = Mandate(**mandate.save())
        mandate = Mandate.get(mandate_created.id)

        self.assertIsNotNone(mandate)
        self.assertTrue(mandate.id)
        self.assertEqual(mandate_created.id, mandate.id)

    # def test_Mandate_Cancel(self):
    #     mandate = Mandate()
    #     mandate.bank_account_id = BaseTestLive.get_johns_account().id
    #     mandate.return_url = 'http://test.test'
    #     mandate.culture = 'FR'
    #     mandate = Mandate(**mandate.save())
    #
    #     #    ! IMPORTANT NOTE !
    #     #
    #     #    In order to make this test pass, at this place you have to set a breakpoint,
    #     #    navigate to URL the mandate.RedirectURL property points to and click "CONFIRM" button.
    #
    #     mandate = Mandate.get(mandate.id)
    #
    #     self.assertTrue(mandate.status == 'SUBMITTED',
    #                     "In order to make this test pass, after creating mandate and before cancelling it you have to navigate to URL the mandate.\
    #                     RedirectURL property points to and click CONFIRM button.")
    #
    #     mandate = mandate.cancel()
    #
    #     self.assertIsNotNone(mandate)
    #     self.assertTrue(mandate['status'] == 'FAILED')

    def test_Mandates_GetAll(self):
        mandates = Mandate.all()

        self.assertTrue(mandates)

    def test_Mandates_GetForUser(self):
        user = BaseTestLive.get_john(recreate=True)
        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account(recreate=True).id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'EN'
        mandate_created = Mandate(**mandate.save())

        mandates = user.mandates.all()

        self.assertTrue(mandates)
        self.assertTrue(len(mandates[0].id) > 0)
        self.assertEqual(mandate_created.id, mandates[0].id)

    def test_Mandates_GetForBankAccount(self):
        BaseTestLive.get_john(recreate=True)
        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account(recreate=True).id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'EN'
        mandate_created = Mandate(**mandate.save())

        mandates_page = BaseTestLive.get_johns_account().get_mandates()
        mandates = mandates_page.data

        self.assertTrue(mandates)
        self.assertIsNotNone(mandates[0])
        self.assertTrue(mandates[0].id)
        self.assertEqual(mandates[0].id, mandate_created.id)

    def test_Mandate_GetTransactions(self):
        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account().id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'FR'
        mandate = Mandate(**mandate.save())

        transactions_page = mandate.get_transactions()

        self.assertIsNotNone(transactions_page.data)
        self.assertIsInstance(transactions_page.data, list)
