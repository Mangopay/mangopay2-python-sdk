import time

from mangopay.resources import ReportTransactions, Report
from mangopay.utils import ReportTransactionsFilters
from tests.test_base import BaseTestLive


class ReportsTestLive(BaseTestLive):
    def test_ReportCreate(self):
        report = ReportTransactions()
        report.report_type = 'transactions'
        result = report.save()

        self.assertIsNotNone(result)
        self.assertTrue(result['id'])

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

    def test_ReportFilteredCreate_SpecificUseCase(self):
        report = ReportTransactions()
        report.report_type = 'transactions'
        report.tag = 'Created using Mangopay Python SDK'
        report.download_format = 'CSV'
        report.callback_url = 'https://mangopay.com/docs/please-ignore'
        report.preview = False
        report.filters = ReportTransactionsFilters(
            before_date=1714435201,
            after_date=1714348799,
            status=['SUCCEEDED'],
            nature=['REGULAR'],
            wallet_id=None,
            author_id=None,
            min_debited_funds_amount=0,
            min_debited_funds_currency='EUR',
            max_debited_funds_amount=1000000,
            max_debited_funds_currency='EUR'
        )
        report.columns = [
            'Id',
            'Tag',
            'CreationDate',
            'ExecutionDate',
            'AuthorId',
            'CreditedUserId',
            'DebitedFundsAmount',
            'DebitedFundsCurrency',
            'CreditedFundsAmount',
            'CreditedFundsCurrency',
            'FeesAmount',
            'FeesCurrency',
            'Status',
            'ResultCode',
            'ResultMessage',
            'Type',
            'Nature',
            'CreditedWalletId',
            'DebitedWalletId'
        ]
        report.sort = 'CreationDate: DESC'
        result = report.save()

        self.assertIsNotNone(result)
        self.assertIsNotNone(result['filters'])

        self.assertEqual(report.filters.before_date, result['filters'].before_date)
        self.assertEqual(report.filters.after_date, result['filters'].after_date)
        self.assertEqual(report.filters.status, result['filters'].status)
        self.assertEqual(report.filters.nature, result['filters'].nature)
        self.assertEqual(report.filters.min_debited_funds_amount, result['filters'].min_debited_funds_amount)
        self.assertEqual(report.filters.min_debited_funds_currency, result['filters'].min_debited_funds_currency)
        self.assertEqual(report.filters.max_debited_funds_amount, result['filters'].max_debited_funds_amount)
        self.assertEqual(report.filters.max_debited_funds_currency, result['filters'].max_debited_funds_currency)
        self.assertIsNone(result['filters'].wallet_id)
        self.assertIsNone(result['filters'].author_id)

    def test_ReportGet(self):
        report = BaseTestLive.get_johns_report()
        result = Report.get(report.id)

        self.assertEqual(report.id, result.id)

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
