import time

from mangopay.exceptions import APIError
from mangopay.resources import BankWirePayOut, IdempotencyResponse
from mangopay.utils import Money
from tests.test_base import BaseTestLive


class IdempotencyTestLive(BaseTestLive):

    def test_Idempotency(self):
        key = str(int(time.time())) + 'abcdefg'
        pay_out = None

        #create bankwire
        try:
            pay_out_post = BankWirePayOut()
            pay_out_post.author = BaseTestLive.get_john()
            pay_out_post.debited_wallet = BaseTestLive.get_johns_wallet()
            debited_funds = Money()
            debited_funds.amount = 10
            debited_funds.currency = 'EUR'
            pay_out_post.debited_funds = debited_funds
            fees = Money()
            fees.amount = 5
            fees.currency = 'EUR'
            pay_out_post.fees = fees
            pay_out_post.bank_account = BaseTestLive.get_johns_account()
            pay_out_post.bank_wire_ref = "Johns bank wire ref"
            pay_out_post.tag = "DefaultTag"
            pay_out_post.credited_user = BaseTestLive.get_john()
            pay_out = pay_out_post.save(idempotency_key=key)
        except Exception as e:
            self.assertFalse(True, str(e))

        self.assertIsNotNone(pay_out)

        #test existing key
        result = None
        try:
            result = IdempotencyResponse.get(key)
        except Exception as e:
            self.assertFalse(True, str(e))

        self.assertIsNotNone(result)

        #test non existing key
        try:
            IdempotencyResponse.get(key+'_no')

            #expecting a APIError to be thrown
            self.assertFalse(True, 'Api Error should have been thrown')
        except APIError as e:
            self.assertEqual(e.content['Type'], 'correlationid_not_found')
            self.assertTrue(e.code == 400)
        except Exception as ex:
            self.assertFalse(True, str(ex))
