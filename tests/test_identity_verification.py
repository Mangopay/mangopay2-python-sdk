import unittest

from mangopay.resources import IdentityVerification, IdentityVerificationCheck
from mangopay.utils import timestamp_from_datetime
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

    @unittest.skip("api returning 404")
    def test_get_checks(self):
        self.create_new_identity_verification()
        # can be fetched in 2 ways:

        # checks: IdentityVerificationCheck = IdentityVerificationCheck.get(
        #     IdentityVerificationTest._identity_verification.id)
        checks: IdentityVerificationCheck = IdentityVerificationTest._identity_verification.get_checks()

        self.assertIsNotNone(checks)
        self.assertEqual(checks.status, 'PENDING')
        self.assertTrue(timestamp_from_datetime(checks.creation_date) > 0)
        self.assertTrue(timestamp_from_datetime(checks.last_update) > 0)
        self.assertIsNotNone(checks.checks)

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
