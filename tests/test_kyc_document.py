from mangopay.resources import Document
from tests.test_base import BaseTestLive


class KYCDocumentTestLive(BaseTestLive):

    def test_GetKycDocuments(self):
        documents = Document.all()

        self.assertTrue(documents)

        result = Document.all(page=1, per_page=2, Sort='CreationDate:ASC')

        self.assertTrue(result)

        result2 = Document.all(page=1, per_page=2, Sort='CreationDate:DESC')

        self.assertTrue(result2)
        self.assertFalse(result.data[0].id == result2.data[0].id)

    def test_GetKycDocument(self):
        johns_document = BaseTestLive.get_johns_kyc_document()
        document = Document.get(johns_document.id)

        self.assertTrue(document)
        self.assertEqual(document.id, johns_document.id)
        self.assertEqual(document.status, johns_document.status)
        self.assertEqual(document.type, johns_document.type)
