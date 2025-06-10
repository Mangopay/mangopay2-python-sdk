from mangopay.resources import ReportV2
from mangopay.utils import ReportFilter
from tests.test_base import BaseTestLive


class ReportsV2TestLive(BaseTestLive):
    def test_ReportCreate(self):
        report = ReportV2()
        report.report_type = 'COLLECTED_FEES'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'COLLECTED_FEES')
        self.assertEqual(result['status'], 'PENDING')

    def test_ReportFilteredCreate(self):
        report = ReportV2()
        report.report_type = 'USER_WALLET_TRANSACTIONS'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        report.filters = ReportFilter()
        report.filters.currency = 'EUR'
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'USER_WALLET_TRANSACTIONS')
        self.assertEqual(result['status'], 'PENDING')

    def test_ReportGet(self):
        report = ReportV2()
        report.report_type = 'COLLECTED_FEES'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        created = report.save()
        result = ReportV2.get(created['id'])

        self.assertEqual(report.id, result.id)

    def test_Reports_All(self):
        page = ReportV2.all(page=1, per_page=1)
        result = page.data

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
