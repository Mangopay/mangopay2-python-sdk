from tests import settings
from tests.resources import Document, Page, DisputeDocument, DocumentConsult, Dispute
from tests.test_base import BaseTest
import responses
import base64
import sys
import os
import unittest


class DocumentConsultTests(BaseTest):
    def setUp(self):
        self._client_disputes = Dispute.all()
        self.assertTrue(self._client_disputes, "INITIALIZATION FAILURE - cannot test disputes")

    @responses.activate
    def test_kyc_document_without_pages(self):
        self.mock_legal_user()
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169420/KYC/documents',
                'body': {
                    "Id": "1173359",
                    "Tag": "custom tag",
                    "CreationDate": 1384450979,
                    "Type": "IDENTITY_PROOF",
                    "Status": "CREATED",
                    "RefusedReasonType": None,
                    "RefusedReasonMessage": None
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/KYC/documents/1173359/consult',
                'body': [],
                'status': 200
            }])

        params = {
            "type": "IDENTITY_PROOF",
            "tag": "custom tag",
            "user": self.legal_user
        }
        document = Document(**params)
        document.save()

        document_consult = DocumentConsult.get_kyc_document_consult(document.id)

        self.assertEqual(0, len(document_consult))

    @responses.activate
    def test_kyc_document_with_pages(self):
        self.mock_legal_user()

        file_path = os.path.join(os.path.dirname(__file__), 'images', 'image.jpg')
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        decoded_string = encoded_string if sys.version_info < (3, 0) else encoded_string.decode('utf-8')

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169420/KYC/documents',
                'body': {
                    "Id": "1173359",
                    "Tag": "custom tag",
                    "CreationDate": 1384450979,
                    "Type": "IDENTITY_PROOF",
                    "Status": "CREATED",
                    "RefusedReasonType": None,
                    "RefusedReasonMessage": None
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169420/KYC/documents/1173359/pages',
                'body': {
                    "File": decoded_string
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/KYC/documents/1173359/consult',
                'body': [
                    {
                        "Url": "https://api.sandbox.mangopay.com/public/documents/c2a145/consult/B26MPGOXXMW1GIPKryp23QDK3w",
                        "ExpirationDate": 1504476880
                    },
                    {
                        "Url": "https://api.sandbox.mangopay.com/public/documents/c2a145/consult/VK6xayepqMdwWsMvMpOxLywv",
                        "ExpirationDate": 1504476880
                    }
                ],
                'status': 200
            }])

        params = {
            "type": "IDENTITY_PROOF",
            "tag": "custom tag",
            "user": self.legal_user
        }
        document = Document(**params)
        document.save()

        params = {
            "file": encoded_string,
            "user": self.legal_user,
            "document": document
        }
        page1 = Page(**params)
        page2 = Page(**params)
        page1.save()
        page2.save()

        document_consult = DocumentConsult.get_kyc_document_consult(document.id)

        self.assertEqual(2, len(document_consult))

    @responses.activate
    def test_dispute_document_without_pages(self):
        self.register_mock(
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/dispute-documents/9103600/consult',
                'body': [],
                'status': 200
            })
        disputeDocId = 9103600
        document_consult = DocumentConsult.get_dispute_document_consult(disputeDocId)

        self.assertEqual(0, len(document_consult))

    @responses.activate
    def test_dispute_document_with_pages(self):
        self.register_mock(
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/dispute-documents/9103602/consult',
                'body': [
                    {
                        "Url": "https://api.sandbox.mangopay.com/public/documents/c2a145/consult/WDjXAdp1okXw7T8Oo3ZbO1qVvX",
                        "ExpirationDate": 1504561430
                    }
                ],
                'status': 200
            })
        disputeDocId = 9103602
        document_consult = DocumentConsult.get_dispute_document_consult(disputeDocId)

        self.assertEqual(1, len(document_consult))

    @unittest.skip('Skip dispute tests because there is a lack of data.')
    def test_dispute_document_with_pages_from_disputes(self):
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
        result_document = document.save()

        document_consult = DocumentConsult.get_dispute_document_consult(result_document.id)

        self.assertIsNotNone(document_consult)
