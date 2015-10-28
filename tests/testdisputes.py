import os
from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.types.money import Money
from mangopaysdk.tools.sorting import Sorting
from mangopaysdk.tools.enums import *
from random import randint
from mangopaysdk.entities.dispute import Dispute
from mangopaysdk.entities.disputedocument import DisputeDocument
from mangopaysdk.entities.disputepage import DisputePage
from mangopaysdk.entities.repudiation import Repudiation
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.tools.filtertransactions import FilterTransactions
import time


class Test_Disputes(TestBase):


    # IMPORTANT NOTE!
    # 
    # Due to the fact the disputes CANNOT be created on user's side,
    # a special approach in testing is needed. 
    # In order to get the tests below pass, a bunch of disputes has
    # to be prepared on the API's side - if it is not, you can
    # just skip these tests, as they won't pass.


    def refreshClientDisputes(self):
        sorting = Sorting()
        sorting.AddField("CreationDate", SortDirection.DESC)
        pagination = Pagination(1, 100)
        self._clientDisputes = self.sdk.disputes.GetAll(pagination, None, sorting)

        self.assertIsNotNone(self._clientDisputes, 'INITIALIZATION FAILURE - cannot test disputes')
        self.assertTrue(len(self._clientDisputes) > 0, 'INITIALIZATION FAILURE - cannot test disputes')
        return

    def test_Disputes_GetDispute(self):
        self.refreshClientDisputes()

        dispute = self.sdk.disputes.Get(self._clientDisputes[0].Id)

        self.assertIsNotNone(dispute)
        self.assertEqual(dispute.Id, self._clientDisputes[0].Id)

    def test_Disputes_GetTransactions(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.DisputeType != DisputeType.RETRIEVAL):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting dispute\'s transactions because there\'s no dispute of non-RETRIEVAL type in the disputes list.')

        pagination = Pagination(1, 10)
        transactions = self.sdk.disputes.GetTransactions(dispute.Id, pagination)

        self.assertIsNotNone(transactions)
        self.assertTrue(len(transactions) > 0)

    def test_Disputes_GetDisputesForWallet(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.InitialTransactionId != None):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting disputes for wallet because there\'s no dispute with transaction ID in the disputes list.')

        walletId = self.sdk.payIns.Get(dispute.InitialTransactionId).CreditedWalletId
        pagination = Pagination(1, 10)
        disputes = self.sdk.disputes.GetDisputesForWallet(walletId, pagination)

        self.assertIsNotNone(disputes)
        self.assertTrue(len(disputes) > 0)

    def test_Disputes_GetDisputesForUser(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.DisputeType != DisputeType.RETRIEVAL):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting disputes for user because there\'s no dispute of non-RETRIEVAL type in the disputes list.')

        pagination = Pagination(1, 10)
        transactions = self.sdk.disputes.GetTransactions(dispute.Id, pagination)
        userId = transactions[0].AuthorId;
        disputes = self.sdk.disputes.GetDisputesForUser(userId, pagination)

        self.assertIsNotNone(disputes)
        self.assertTrue(len(disputes) > 0)

    def test_Disputes_CreateDocument(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test creating dispute document because there\'s no dispute with expected status in the disputes list.')

        result = None

        document = DisputeDocument()
        document.Type = DisputeDocumentType.DELIVERY_PROOF

        result = self.sdk.disputes.CreateDocument(document, dispute.Id)

        self.assertIsNotNone(result)
        self.assertEqual(result.Type, DisputeDocumentType.DELIVERY_PROOF)

    def test_Disputes_CreatePage(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test creating dispute document page because there\'s no dispute with expected status in the disputes list.')

        document = DisputeDocument()
        document.Type = DisputeDocumentType.DELIVERY_PROOF

        result = self.sdk.disputes.CreateDocument(document, dispute.Id)

        disputePage = DisputePage().LoadDocumentFromFile(os.path.join(os.path.dirname(__file__), "TestKycPageFile.png"))
        self.sdk.disputes.CreatePage(disputePage, dispute.Id, result.Id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.Type, DisputeDocumentType.DELIVERY_PROOF)

    def test_Disputes_ContestDispute(self):
        self.refreshClientDisputes()

        notContestedDispute = None

        for d in self._clientDisputes:
            if ((d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION)
                and (d.DisputeType == DisputeType.CONTESTABLE or d.DisputeType == DisputeType.RETRIEVAL)):
                notContestedDispute = d
                break

        self.assertIsNotNone(notContestedDispute, 'Cannot test contesting dispute because there\'s no dispute that can be contested in the disputes list.')

        result = None

        contestedFunds = None
        if (notContestedDispute.Status == DisputeStatus.PENDING_CLIENT_ACTION):
            contestedFunds = Money()
            contestedFunds.Amount = 100
            contestedFunds.Currency = 'EUR'

        result = self.sdk.disputes.ContestDispute(contestedFunds, notContestedDispute.Id)

        self.assertIsNotNone(result)
        self.assertEqual(result.Id, notContestedDispute.Id)

    def test_Disputes_SaveTag(self):
        self.refreshClientDisputes()
        newTag = 'New tag: ' + str(randint(1000000000000, 9999999999999))

        result = self.sdk.disputes.UpdateTag(newTag, self._clientDisputes[0].Id)

        self.assertIsNotNone(result)
        self.assertEqual(result.Tag, newTag)

    def test_Disputes_CloseDispute(self):
        self.refreshClientDisputes()
        
        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test closing dispute because there\'s no dispute that can be closed in the disputes list.')

        result = self.sdk.disputes.CloseDispute(dispute.Id)

        self.assertIsNotNone(result)

    def test_Disputes_GetDocument(self):
        self.refreshClientDisputes()
        
        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting dispute\'s document because there\'s no dispute with expected status in the disputes list.')

        document = None
        result = None

        documentPost = DisputeDocument()
        documentPost.Type = DisputeDocumentType.OTHER
        document = self.sdk.disputes.CreateDocument(documentPost, dispute.Id)

        result = self.sdk.disputes.GetDocument(document.Id)

        self.assertIsNotNone(result)
        self.assertEqual(result.CreationDate, document.CreationDate)
        self.assertEqual(result.Id, document.Id)
        self.assertEqual(result.RefusedReasonMessage, document.RefusedReasonMessage)
        self.assertEqual(result.RefusedReasonType, document.RefusedReasonType)
        self.assertEqual(result.Status, document.Status)
        self.assertEqual(result.Tag, document.Tag)
        self.assertEqual(result.Type, document.Type)
        self.assertEqual(result.DisputeId, document.DisputeId)

    def test_Disputes_GetDocumentsForDispute(self):
        self.refreshClientDisputes()
        
        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.SUBMITTED):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting dispute\'s documents because there\'s no available disputes with SUBMITTED status in the disputes list.')

        result = self.sdk.disputes.GetDocumentsForDispute(dispute.Id)

        self.assertIsNotNone(result)

    def test_Disputes_GetDocumentsForClient(self):
        result = self.sdk.disputes.GetDocumentsForClient()
        self.assertIsNotNone(result)

    def test_Disputes_SubmitDisputeDocument(self):
        self.refreshClientDisputes()
        
        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.PENDING_CLIENT_ACTION or d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test submitting dispute\'s documents because there\'s no dispute with expected status in the disputes list.')

        disputeDocument = self.sdk.disputes.GetDocumentsForDispute(dispute.Id)[0]

        disputeDocumentPut = DisputeDocument()
        disputeDocumentPut.Id = disputeDocument.Id
        disputeDocumentPut.Status = DisputeDocumentStatus.VALIDATION_ASKED

        result = self.sdk.disputes.SubmitDisputeDocument(disputeDocumentPut, dispute.Id)

        self.assertIsNotNone(result)

    def test_Disputes_GetRepudiation(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.DisputeType != DisputeType.RETRIEVAL):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test getting repudiation because there\'s no dispute of non-RETRIEVAL type in the disputes list.')

        repudiationId = self.sdk.disputes.GetTransactions(dispute.Id)[0].Id

        result = self.sdk.disputes.GetRepudiation(repudiationId)

        self.assertIsNotNone(result)

    def test_Disputes_CreateSettlementTransfer(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.CLOSED and d.DisputeType != DisputeType.RETRIEVAL):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test creating settlement transfer because there\'s no closed dispute in the disputes list.')

        repudiationId = self.sdk.disputes.GetTransactions(dispute.Id)[0].Id
        repudiation = self.sdk.disputes.GetRepudiation(repudiationId)

        debitedFunds = Money()
        fees = Money()
        debitedFunds.Currency = 'EUR'
        debitedFunds.Amount = 1
        fees.Currency = 'EUR'
        fees.Amount = 0

        post = Transfer()
        post.AuthorId = repudiation.AuthorId
        post.DebitedFunds = debitedFunds
        post.Fees = fees

        result = self.sdk.disputes.CreateSettlementTransfer(post, repudiationId)

        self.assertIsNotNone(result)

    def test_Disputes_GetFilteredDisputes(self):

        now = int(time.time())

        filterAfter = FilterTransactions()
        filterBefore = FilterTransactions()
        filterAfter.AfterDate = now
        filterBefore.BeforeDate = now

        pagination = Pagination()

        result1 = self.sdk.disputes.GetAll(pagination, filterAfter)
        result2 = self.sdk.disputes.GetAll(pagination, filterBefore)

        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)
        self.assertTrue(len(result1) == 0)
        self.assertTrue(len(result2) > 0)

    def test_Disputes_GetFilteredDisputeDocuments(self):

        now = int(time.time())

        filterAfter = FilterTransactions()
        filterBefore = FilterTransactions()
        filterAfter.AfterDate = now
        filterBefore.BeforeDate = now

        pagination = Pagination()

        result1 = self.sdk.disputes.GetDocumentsForClient(pagination, filterAfter)
        result2 = self.sdk.disputes.GetDocumentsForClient(pagination, filterBefore)

        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)
        self.assertTrue(len(result1) == 0)
        self.assertTrue(len(result2) > 0)

        filterType = FilterTransactions()
        filterType.Type = result2[0].Type
        result3 = self.sdk.disputes.GetDocumentsForClient(pagination, filterType)
        self.assertIsNotNone(result3)
        self.assertTrue(len(result3) > 0)

        for dd in result3:
            self.assertTrue(dd.Type, result2[0].Type)

    def test_Disputes_ResubmitDispute(self):
        self.refreshClientDisputes()

        dispute = None

        for d in self._clientDisputes:
            if (d.Status == DisputeStatus.REOPENED_PENDING_CLIENT_ACTION):
                dispute = d
                break

        self.assertIsNotNone(dispute, 'Cannot test resubmitting dispute because there\'s no re-opened dispute in the disputes list.')

        result = self.sdk.disputes.ResubmitDispute(dispute.Id)

        self.assertIsNotNone(result)
        self.assertEqual(result.Status, DisputeStatus.SUBMITTED)