from mangopay.resources import IdentityVerification
from tests.test_base import BaseTestLive


class IdentityVerificationTest(BaseTestLive):
    _identity_verification = None

    def test_create_identity_verification(self):
        self.create_new_identity_verification()
        self.assertIsNotNone(IdentityVerificationTest._identity_verification)
        self.assertIsNotNone(IdentityVerificationTest._identity_verification.return_url)
        self.assertIsNotNone(IdentityVerificationTest._identity_verification.hosted_url)
        self.assertEqual(IdentityVerificationTest._identity_verification.status, 'PENDING')

    def test_get_identity_verification(self):
        self.create_new_identity_verification()
        fetched = IdentityVerification.get(IdentityVerificationTest._identity_verification.id)

        self.assertIsNotNone(fetched)
        self.assertEqual(IdentityVerificationTest._identity_verification.hosted_url, fetched.hosted_url)
        self.assertEqual(IdentityVerificationTest._identity_verification.return_url, fetched.return_url)
        self.assertEqual(IdentityVerificationTest._identity_verification.status, fetched.status)

    def test_get_all_identity_verifications_for_user(self):
        self.create_new_identity_verification()
        john = BaseTestLive.get_john()
        fetched = IdentityVerification.get_all(john.id)

        self.assertIsNotNone(fetched)
        self.assertIsInstance(fetched.data, list)
        self.assertTrue(len(fetched.data) > 0)

    @staticmethod
    def create_new_identity_verification():
        if IdentityVerificationTest._identity_verification is None:
            john = BaseTestLive.get_john()

            identity_verification = IdentityVerification()
            identity_verification.return_url = "https://example.com"
            identity_verification.tag = "created by the Python SDK"

            IdentityVerificationTest._identity_verification = IdentityVerification(
                **identity_verification.create(john.id))
        return IdentityVerificationTest._identity_verification
