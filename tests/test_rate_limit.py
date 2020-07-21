from tests.test_base import BaseTest, BaseTestLive
from mangopay.api import APIRequest as api


class RateLimit(BaseTest):

    def test_rate_limits_update(self):
        apis = api()
        self.assertIsNone(apis.get_rate_limits())
        BaseTestLive.get_ubo_declaration()

        rate_limits = apis.get_rate_limits()
        self.assertIsNotNone(rate_limits)
        self.assertTrue(len(rate_limits) == 4)