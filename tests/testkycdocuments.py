import unittest
from tests.testbase import TestBase
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.tools.sorting import Sorting
from mangopaysdk.tools.enums import SortDirection

class Test_KycDocuments(TestBase):
    """Test methods for KYC documents."""

    
    def test_KycDocuments_GetAll(self):
        kycDocument = self.getUserKycDocument()
        pagination = Pagination(1, 100)
        self.sdk.kycdocuments.GetAll(pagination)
        pagination.Page = pagination.TotalPages
        list = self.sdk.kycdocuments.GetAll(pagination)

        kycFromList = self.getEntityFromList(kycDocument.Id, list)
        
        self.assertTrue(isinstance(kycFromList, KycDocument))
        self.assertEqualInputProps(kycDocument, kycFromList)
        self.assertEqual(pagination.ItemsPerPage, 100)

    def test_KycDocuments_GetAll_SortByCreationDate(self):
        pagination = Pagination(1, 10)
        sorting = Sorting()
        sorting.AddField('CreationDate', SortDirection.DESC)

        list = self.sdk.kycdocuments.GetAll(pagination, sorting)

        self.assertTrue(list[0].CreationDate >= list[1].CreationDate)