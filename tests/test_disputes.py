import base64
import os
import time
import unittest

from mangopay.resources import Dispute, PayIn, DisputeDocument, SettlementTransfer, DisputeDocumentPage
from mangopay.utils import Money
from tests.test_base import BaseTestLive


# Comment following line to run DisputeTest
@unittest.skip('Skip dispute tests because there is a lack of data.')
class DisputeTest(BaseTestLive):
    def setUp(self):
        self._client_disputes = Dispute.all()
        self.assertTrue(self._client_disputes, "INITIALIZATION FAILURE - cannot test disputes")

    def test_GetDispute(self):
        dispute = Dispute.get(self._client_disputes[0].get_pk())

        self.assertIsNotNone(dispute)
        self.assertEqual(dispute.id, self._client_disputes[0].id)

    def test_GetTransactions(self):

        dispute = None
        for d in self._client_disputes:
            if d.dispute_type == 'NOT_CONTESTABLE':
                dispute = d
                break

        self.assertIsNotNone(
            dispute,
            "Cannot test getting dispute's transactions because there's no not contestable dispute in the disputes list."
        )

        transactions = dispute.transactions.all()

        self.assertIsNotNone(transactions)
        self.assertTrue(transactions)

    def test_GetDisputesForWallet(self):
        dispute = None

        for d in self._client_disputes :
            if d.initial_transaction_id is not None:
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting disputes for wallet because there\'s no dispute with transaction ID in the disputes list.')
        wallet = PayIn.get(dispute.initial_transaction_id).credited_wallet

        self.assertIsNotNone(wallet)

        result = wallet.disputes.all()

        self.assertIsNotNone(result)

    def test_GetDisputesForUser(self):
        dispute = None
        for d in self._client_disputes:
            if d.dispute_type == 'NOT_CONTESTABLE':
                dispute = d
                break

        self.assertIsNotNone(
            dispute,
            "Cannot test getting disputes for user because there's no not contestable dispute in the disputes list."
        )

        transactions = dispute.transactions.all()
        user = transactions[0].author
        disputes = user.disputes.all()

        self.assertIsNotNone(disputes)
        self.assertTrue(disputes)

    def test_GetDisputesPendingSettlement(self):
        disputes_pending = Dispute.get_pending_settlement()

        self.assertTrue(disputes_pending)


    def test_CreateDisputeDocument(self):
        dispute = None

        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION'):
                dispute = d
                break

        self.assertIsNotNone(dispute,
                             'Cannot test creating dispute document because there\'s no dispute with expected status in the disputes list.')

        document = DisputeDocument()
        document.type = 'DELIVERY_PROOF'
        document.dispute = dispute
        result = document.save()

        self.assertIsNotNone(result)
        self.assertEqual(result.type, document.type)

    def test_CreateDisputePage(self):
        dispute = None
        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION') and \
                            d.dispute_type in ('CONTESTABLE', 'RETRIEVAL'):
                dispute = d
                break

        self.assertIsNotNone(dispute,
                             'Cannot test creating dispute document page because there\'s no dispute with expected status in the disputes list.')

        dispute_document = DisputeDocument(type='DELIVERY_PROOF', dispute=dispute)
        result = dispute_document.save()
        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'TestKycPageFile.png')
        with open(file_path, 'rb') as f:
            data = f.read()
            encoded_file = base64.b64encode(data)

        resulted_dispute_document = DisputeDocument(result)
        dispute_document_page = DisputeDocumentPage(file=encoded_file, dispute=resulted_dispute_document, document=dispute)
        dispute_document_page.save()

        self.assertIsNotNone(result)
        self.assertEqual(dispute_document.type, resulted_dispute_document.type)

    def test_ContestDispute(self):
        dispute = None
        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION') and\
                            d.dispute_type in ('CONTESTABLE', 'RETRIEVAL'):
                dispute = d
                break

        self.assertIsNotNone(
            dispute,
            "Cannot test contesting dispute because there's no disputes that can be contested in the disputes list."
        )

        money = None
        if dispute.status == 'REOPENED_PENDING_CLIENT_ACTION':
            money = Money(100, 'EUR')

        result = dispute.contest(money)

        self.assertIsNotNone(result)

        self.assertEquals(dispute.id, result['id'])

    def test_SaveTag(self):
        dispute = self._client_disputes[0]
        new_tag = 'New tag ' + str(int(time.time()))
        dispute.tag = new_tag
        result = dispute.save()

        self.assertIsNotNone(result)
        self.assertEqual(dispute.tag, result['tag'])

    def test_CloseDispute(self):
        dispute = None
        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION'):
                dispute = d
                break

        self.assertIsNotNone(
            dispute,
            "Cannot test closing dispute because there's no available disputes with expected status in the disputes list."
        )

        result = dispute.close()

        self.assertIsNotNone(result)

    def test_GetDocument(self):
        dispute = None

        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION'):
                dispute = d
                break

        self.assertIsNotNone(dispute,
                             'Cannot test getting dispute\'s document because there\'s no dispute with expected status in the disputes list.')

        document = DisputeDocument()
        document.type = 'OTHER'
        document.dispute = dispute
        result = document.save()

        self.assertIsNotNone(result)
        self.assertEqual(result.creation_date, document.creation_date)
        self.assertEqual(result.id, document.id)
        self.assertEqual(result.refused_reason_message, document.refused_reason_message)
        self.assertEqual(result.refused_reason_type, document.refused_reason_type)
        self.assertEqual(result.status, document.status)
        self.assertEqual(result.tag, document.tag)
        self.assertEqual(result.type, document.type)
        self.assertEqual(result.dispute_id, document.dispute_id)

    def test_GetDocumentsForDispute(self):
        dispute = None

        for d in self._client_disputes:
            if d.status == 'SUBMITTED':
                dispute = d
                break

        if dispute is None:
            self.test_ContestDispute()
            self.setUp()

            for d in self._client_disputes:
                if d.status == 'SUBMITTED':
                    dispute = d
                    break

            self.assertIsNotNone(dispute,
                                 'Cannot test getting dispute\'s documents because there\'s no available disputes with SUBMITTED status in the disputes list.')

        result = dispute.documents.all()

        self.assertIsNotNone(result)

    def test_GetDocumentsForClient(self):
        result = DisputeDocument.all()
        self.assertIsNotNone(result)

    def test_SubmitDisputeDocument(self):
        dispute = None
        dispute_document = None
        for d in self._client_disputes:
            if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION'):
                dd = d.documents.all(page=1, per_page=1, status='CREATED')
                if dd is not None and len(dd) > 0:
                    dispute = d
                    dispute_document = dd(0)
                    break
        if dispute is None:
            for d in self._client_disputes:
                if d.status in ('PENDING_CLIENT_ACTION', 'REOPENED_PENDING_CLIENT_ACTION'):
                    dispute = d
                    dispute_document = DisputeDocument()
                    dispute_document.type = 'DELIVERY_PROOF'
                    dispute_document.dispute = dispute
                    dispute_document = dispute_document.save()
                    break

        self.assertIsNotNone(dispute,
                             'Cannot test submitting dispute\'s documents because there\'s no dispute with expected status in the disputes list.')
        self.assertIsNotNone(dispute_document,
                             'Cannot test submitting dispute\'s documents because there\'s no dispute document that can be updated.')

        result = None
        dispute_document_put = DisputeDocument()
        dispute_document_put.id = dispute_document.id
        dispute_document_put.dispute = dispute_document.dispute
        dispute_document_put.status = 'VALIDATION_ASKED'
        result = dispute_document_put.submit()

        self.assertIsNotNone(result)
        self.assertTrue(dispute_document_put.type == result['type'])
        self.assertTrue(result['status'] == dispute_document_put.status)

    def test_GetRepudiation(self):
        dispute = None
        for d in self._client_disputes:
            if d.dispute_type == 'NOT_CONTESTABLE' and d.initial_transaction_id is not None:
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting repudiation because there\'s no contestable dispute in the disputes list.')

        repudiation = dispute.transactions.all(page=1, per_page=1)[0]

        self.assertIsNotNone(repudiation)

    def test_CreateSettlementTransfer(self):
        dispute = None
        for d in self._client_disputes:
            if d.status == 'CLOSED' and d.dispute_type == 'NOT_CONTESTABLE':
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test creating settlement transfer because there\'s no closed and not contestable disputes in the disputes list.')

        repudiation = dispute.transactions.all()[0]

        self.assertIsNotNone(repudiation)

        debit_funds = Money()
        fees = Money()
        debit_funds.currency = 'EUR'
        debit_funds.amount = 1
        fees.currency = 'EUR'
        fees.amount = 0

        st = SettlementTransfer()
        st.author = repudiation.author
        st.debited_funds = debit_funds
        st.fees = fees
        st.repudiation_id = repudiation.id
        result = st.save()

        self.assertIsNotNone(result)
        self.assertEqual(result['author_id'], st.author.id)

    def test_GetFilteredDisputes(self):
        now = int(time.time())

        disputes_before = Dispute.all(BeforeDate=now)
        disputes_after = Dispute.all(AfterDate=now)
        self.assertTrue(disputes_before)
        self.assertFalse(disputes_after)

    def test_GetFilteredDisputeDocuments(self):
        now = int(time.time())

        dispute_documents_before = DisputeDocument.all(BeforeDate=now)
        dispute_documents_after = DisputeDocument.all(AfterDate=now+10000)

        self.assertTrue(dispute_documents_before)
        self.assertFalse(dispute_documents_after)

        document_type = dispute_documents_before[0].type
        result = DisputeDocument.all(Type=document_type)

        self.assertTrue(result)

        for dd in result:
            self.assertEqual(dd.type, document_type)

    def test_ResubmitDispute(self):
        dispute = None
        for d in self._client_disputes:
            if d.dispute_type == 'REOPENED_PENDING_CLIENT_ACTION':
                dispute = d
                break

        self.assertIsNotNone(
            dispute,
            "Cannot test resubmitting dispute because there's no re-opened disputes in the disputes list."
        )

        result = dispute.resubmit()

        self.assertTrue('status' in result)

        self.assertEquals(result['status'], 'SUBMITTED')