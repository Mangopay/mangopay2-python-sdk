from mangopay.api import APIRequest as api
from tests.test_base import BaseTest, BaseTestLive


class RateLimit(BaseTest):

    def test_rate_limits_update(self):
        apis = api()
        self.assertIsNone(apis.get_rate_limits())
        BaseTestLive.get_ubo_declaration()

        rate_limits = apis.get_rate_limits()
        self.assertIsNotNone(rate_limits)
        self.assertTrue(len(rate_limits) > 0)

        self.assertEqual(1, rate_limits[0].interval_minutes)
        self.assertEqual(5, rate_limits[1].interval_minutes)
        self.assertEqual(15, rate_limits[2].interval_minutes)
        self.assertEqual(30, rate_limits[3].interval_minutes)
        self.assertEqual(60, rate_limits[4].interval_minutes)
        self.assertEqual(1440, rate_limits[5].interval_minutes)

