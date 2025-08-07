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

    def test_CreateIntentReport(self):
        report = ReportV2()
        report.report_type = 'ECHO_INTENT'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        filters = ReportFilter()
        filters.payment_method = 'PAYPAL'
        filters.status = 'CAPTURED'
        filters.type = 'PAYIN'
        report.filters = filters
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'ECHO_INTENT')
        self.assertEqual(result['status'], 'PENDING')
        self.assertEqual(result['filters'].payment_method, 'PAYPAL')
        self.assertEqual(result['filters'].status, 'CAPTURED')

    def test_CreateIntentActionsReport(self):
        report = ReportV2()
        report.report_type = 'ECHO_INTENT_ACTION'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        filters = ReportFilter()
        filters.payment_method = 'PAYPAL'
        filters.status = 'CAPTURED'
        filters.type = 'PAYIN'
        report.filters = filters
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'ECHO_INTENT_ACTION')
        self.assertEqual(result['status'], 'PENDING')
        self.assertEqual(result['filters'].payment_method, 'PAYPAL')
        self.assertEqual(result['filters'].status, 'CAPTURED')

    def test_CreateSettlementReport(self):
        report = ReportV2()
        report.report_type = 'ECHO_SETTLEMENT'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        filters = ReportFilter()
        filters.payment_method = 'PAYPAL'
        filters.status = 'RECONCILED'
        report.filters = filters
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'ECHO_SETTLEMENT')
        self.assertEqual(result['status'], 'PENDING')
        self.assertEqual(result['filters'].status, 'RECONCILED')

    def test_CreateSplitReport(self):
        report = ReportV2()
        report.report_type = 'ECHO_SPLIT'
        report.download_format = 'CSV'
        report.after_date = 1740787200
        report.before_date = 1743544740
        filters = ReportFilter()
        filters.payment_method = 'PAYPAL'
        filters.status = 'COMPLETED'
        filters.scheduled = False
        filters.intent_id = 'int_0197f975-63f6-714e-8fc6-4451e128170f'
        report.filters = filters
        report.columns = ['IntentId', 'FeesAmount']
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])
        self.assertEqual(result['report_type'], 'ECHO_SPLIT')
        self.assertEqual(result['status'], 'PENDING')
        self.assertEqual(result['filters'].status, 'COMPLETED')
        self.assertEqual(result['filters'].scheduled, False)
        self.assertEqual(result['filters'].intent_id, 'int_0197f975-63f6-714e-8fc6-4451e128170f')
        self.assertEqual(2, len(result['columns']))
