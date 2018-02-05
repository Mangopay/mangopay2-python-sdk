# -*- coding: utf-8 -*-

from .test_base import BaseTestLive

from mangopay.resources import Repudiation


class RepudiationsTestLive(BaseTestLive):

    def test_Repudiation_GetRefunds(self):
        repudiation = Repudiation.get('41631014')

        get_refunds = repudiation.get_refunds()

        self.assertIsNotNone(get_refunds)
        self.assertIsInstance(get_refunds, list)
