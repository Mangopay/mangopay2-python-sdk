import time

from mangopay.resources import Document
from tests.test_base import BaseTestLive


class KYCDocumentTestLive(BaseTestLive):

    def test_GetKycDocuments(self):
        johns_document = BaseTestLive.get_johns_kyc_document()
        current_time = round(time.time())
        documents = Document.all(BeforeDate=current_time + 1000,
                                 AfterDate=current_time - 1000)

        self.assertTrue(len(documents.data) > 0)

        result = Document.all(page=1, per_page=2, Sort='CreationDate:ASC',
                              BeforeDate=current_time + 1000,
                              AfterDate=current_time - 1000)

        self.assertTrue(len(result.data) > 0)

        result2 = Document.all(page=1, per_page=2, Sort='CreationDate:DESC',
                               BeforeDate=current_time + 1000,
                               AfterDate=current_time - 1000)

        self.assertTrue(len(result.data) > 0)
        self.assertFalse(result.data[0].id == result2.data[0].id)

    def test_GetKycDocument(self):
        johns_document = BaseTestLive.get_johns_kyc_document()
        document = Document.get(johns_document.id)

        self.assertTrue(document)
        self.assertEqual(document.id, johns_document.id)
        self.assertEqual(document.status, johns_document.status)
        self.assertEqual(document.type, johns_document.type)
