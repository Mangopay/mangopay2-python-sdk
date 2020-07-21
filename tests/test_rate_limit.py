from tests.test_base import BaseTest, BaseTestLive
from tests.resources import CardRegistration
from mangopay.api import APIRequest as api

class RateLimit(BaseTest):

    def test_rate_limits_update(self):
        self.assertIsNone(api.rate_limits)
        user = BaseTestLive.get_john()
        card_registration = CardRegistration()
        card_registration.user = user
        card_registration.currency = "EUR"

        card_registration.save()

        rate_limits = api.rate_limits
        self.assertIsNotNone(rate_limits)
        self.assertTrue(len(rate_limits) == 4)