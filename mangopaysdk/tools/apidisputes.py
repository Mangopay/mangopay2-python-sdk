from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool
from mangopaysdk.entities.dispute import Dispute
from mangopaysdk.entities.transaction import Transaction
from mangopaysdk.entities.repudiation import Repudiation
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.entities.settlement import Settlement


class ApiDisputes(ApiBase):
    """MangoPay API methods for disputes."""

    def Get(self, disputeId):
        """Get Dispute by ID.
        param Dispute identifier
        return Dispute object returned from API
        """
        return self._getObject('disputes_get', disputeId, 'Dispute')

    def GetAll(self, pagination = None, filter = None, sorting = None):
        """Get all client's disputes.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with disputes
        """
        return self._getList('disputes_get_all', pagination, 'Dispute', None, filter, sorting)

    def GetTransactions(self, disputeId, pagination = None, filter = None, sorting = None):
        """Get dispute transactions.
        param Dispute identifier.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with transactions
        """
        return self._getList('disputes_get_transactions', pagination, 'Transaction', disputeId, filter, sorting)

    def GetDisputesForWallet(self, walletId, pagination = None, filter = None, sorting = None):
        """Get disputes for wallet.
        param Wallet identifier.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with disputes
        """
        return self._getList('disputes_get_for_wallet', pagination, 'Dispute', walletId, filter, sorting)

    def GetDisputesForUser(self, userId, pagination = None, filter = None, sorting = None):
        """Get disputes for user.
        param User identifier.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with disputes
        """
        return self._getList('disputes_get_for_user', pagination, 'Dispute', userId, filter, sorting)

    def GetDocument(self, disputeDocumentId):
        """Get dispute document by ID.
        param Dispute document identifier
        return DisputeDocument object returned from API
        """
        return self._getObject('disputes_document_get', disputeDocumentId, 'DisputeDocument')

    def CreateDocument(self, disputeDocument, disputeId):
        """Create dispute document.
        param DisputeDocument entity
        param Dispute identifier
        return DisputeDocument object returned from API
        """
        return self.CreateDocumentIdempotent(None, disputeDocument, disputeId)

    def CreateDocumentIdempotent(self, idempotencyKey, disputeDocument, disputeId):
        """Create dispute document.
        param string idempotencyKey Idempotency key for this request
        param DisputeDocument entity
        param Dispute identifier
        return DisputeDocument object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'disputes_document_create', disputeDocument, 'DisputeDocument', disputeId)

    def CreatePage(self, disputePage, disputeId, disputeDocumentId):
        """Create DisputePage for existing DisputeDocument.
        param DisputePage entity (File should be base64 string)
        param Dispute identifier
        param DisputeDocument identifier
        """
        return self.CreatePageIdempotent(None, disputePage, disputeId, disputeDocumentId)

    def CreatePageIdempotent(self, idempotencyKey, disputePage, disputeId, disputeDocumentId):
        """Create DisputePage for existing DisputeDocument.
        param string idempotencyKey Idempotency key for this request
        param DisputePage entity (File should be base64 string)
        param Dispute identifier
        param DisputeDocument identifier
        """
        return self._createObjectIdempotent(idempotencyKey, 'disputes_document_page_create', disputePage, None, disputeId, disputeDocumentId)

    def ContestDispute(self, contestedFunds, disputeId):
        """Contest dispute.
        param Contested funds
        param Dispute identifier
        return Dispute object returned from API
        """
        dispute = Dispute()
        dispute.ContestedFunds = contestedFunds

        return self._saveObject('disputes_save_contest_funds', dispute, 'Dispute', disputeId)

    def UpdateTag(self, newTag, disputeId):
        """Update dispute tag.
        param New tag text
        param Dispute identifier
        return Dispute object returned from API
        """
        dispute = Dispute()
        dispute.Tag = newTag

        return self._saveObject('disputes_save_tag', dispute, 'Dispute', disputeId)

    def CloseDispute(self, disputeId):
        """Close dispute.
        param Dispute identifier
        return Dispute object returned from API
        """
        dispute = Dispute()
        return self._saveObject('disputes_save_close', dispute, 'Dispute', disputeId)

    def GetDocumentsForDispute(self, disputeId, pagination = None, filter = None, sorting = None):
        """Get dispute documents for dispute.
        param Dispute identifier.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with DisputeDocument objects
        """
        return self._getList('disputes_document_get_for_dispute', pagination, 'DisputeDocument', disputeId, filter, sorting)

    def GetDocumentsForClient(self, pagination = None, filter = None, sorting = None):
        """Get dispute documents for client.
        param Pagination object
        param Filter object
        param Sorting object
        return Array with DisputeDocument objects
        """
        return self._getList('disputes_document_get_for_client', pagination, 'DisputeDocument', None, filter, sorting)

    def SubmitDisputeDocument(self, disputeDocument, disputeId):
        """Submit dispute document.
        param Dispute document object
        param Dispute identifier
        return DisputeDocument object returned from API
        """
        return self._saveObject('disputes_document_submit', disputeDocument, 'DisputeDocument', disputeId, disputeDocument.Id)

    def GetRepudiation(self, repudiationId):
        """Get repudiation.
        param Repudiation identifier
        return Repudiation object returned from API
        """
        return self._getObject('disputes_repudiation_get', repudiationId, 'Repudiation')

    def CreateSettlementTransfer(self, settlementTransfer, repudiationId):
        """Create settlement transfer.
        param Settlement transfer object
        param Repudiation identifier
        return Transfer object returned from API
        """
        return self.CreateSettlementTransferIdempotent(None, settlementTransfer, repudiationId)

    def CreateSettlementTransferIdempotent(self, idempotencyKey, settlementTransfer, repudiationId):
        """Create settlement transfer.
        param string idempotencyKey Idempotency key for this request
        param Settlement transfer object
        param Repudiation identifier
        return Transfer object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'disputes_repudiation_create_settlement', settlementTransfer, 'Transfer', repudiationId)

    def ResubmitDispute(self, disputeId):
        return self._saveObject('disputes_save_contest_funds', None, 'Dispute', disputeId)

    def GetSettlementTransfer(self, settlementId):
        """Get settlement transfer.
        param string settlementId SettlementTransfer identifier
        return Settlement instance returned from API
        """
        return self._getObject('settlement_get', settlementId, 'Settlement')