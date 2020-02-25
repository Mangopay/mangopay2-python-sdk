# -*- coding: utf-8 -*-

from mangopay.resources import Repudiation
from tests.test_base import BaseTestLive


class RepudiationsTestLive(BaseTestLive):

    def test_Repudiation_GetRefunds(self):
        repudiation = Repudiation.get('41631014')

        refunds_page = repudiation.get_refunds()

        self.assertIsNotNone(refunds_page.data)
        self.assertIsInstance(refunds_page.data, list)
