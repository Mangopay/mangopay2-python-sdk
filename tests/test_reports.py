import time

from mangopay.resources import ReportTransactions, Report
from mangopay.utils import ReportTransactionsFilters
from tests.test_base import BaseTestLive
import unittest


class ReportsTestLive(BaseTestLive):
    @unittest.skip("reason for skipping")
    def test_ReportCreate(self):
        report = ReportTransactions()
        report.report_type = 'transactions'
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])

    @unittest.skip("reason for skipping")
    def test_ReportFilteredCreate(self):
        report = ReportTransactions()
        report.report_type = 'transactions'
        report.filters = ReportTransactionsFilters()
        report.filters.author_id = BaseTestLive.get_john().id
        report.filters.wallet_id = BaseTestLive.get_johns_wallet().id
        result = report.save()

        self.assertIsNotNone(result)
        self.assertIsNotNone(result['filters'])
        self.assertTrue(result['filters'].author_id)
        self.assertTrue(result['filters'].wallet_id)
        self.assertTrue(result['id'])
        self.assertEqual(report.filters.author_id, result['filters'].author_id)
        self.assertEqual(report.filters.wallet_id, result['filters'].wallet_id)

    @unittest.skip("reason for skipping")
    def test_ReportGet(self):
        report = BaseTestLive.get_johns_report()
        result = Report.get(report.id)

        self.assertEqual(report.id, result.id)

    @unittest.skip("reason for skipping")
    def test_Reports_All(self):
        time.sleep(3)
        report = BaseTestLive.get_johns_report(recreate=True)

        page = Report.all(page=1, per_page=1, sort='CreationDate:DESC')
        result = page.data

        self.assertIsNotNone(result[0])
        self.assertEqual(report.id, result[0].id)

        page = Report.all(AfterDate=result[0].creation_date, BeforeDate=int(time.time() - 2000),
                          sort='CreationDate:DESC')
        result = page.data

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 0)

        page = Report.all(AfterDate=int(time.time() - 315569260), BeforeDate=int(time.time()),
                          sort='CreationDate:DESC')
        result = page.data

        self.assertTrue(result)
