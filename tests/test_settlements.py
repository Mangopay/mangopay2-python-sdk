# -*- coding: utf-8 -*-
import os

from mangopay.resources import Settlement
from tests.test_base import BaseTestLive


class SettlementTestLive(BaseTestLive):
    _settlement = None

    def test_upload_settlement(self):
        uploaded = self.create_new_settlement()
        self.assertEqual('UPLOADED', uploaded.status)

    def test_get_settlement(self):
        uploaded = self.create_new_settlement()
        fetched = Settlement.get(uploaded.settlement_id)
        self.assertEqual('UPLOADED', fetched.status)

    def test_update_settlement(self):
        before_update = self.create_new_settlement()
        self.assertEqual('UPLOADED', before_update.status)

        file_path = os.path.join(os.path.dirname(__file__), 'resources', 'settlement_sample.csv')
        with open(file_path, 'rb') as f:
            data = f.read()
        after_update = Settlement(**Settlement.update_file(before_update.settlement_id, data))

        self.assertEqual('UPLOADED', after_update.status)

    @staticmethod
    def create_new_settlement():
        if SettlementTestLive._settlement is None:
            file_path = os.path.join(os.path.dirname(__file__), 'resources', 'settlement_sample.csv')
            with open(file_path, 'rb') as f:
                data = f.read()
            SettlementTestLive._settlement = Settlement(**Settlement.upload(data))
        return SettlementTestLive._settlement
