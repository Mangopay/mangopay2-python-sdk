import unittest
import random, string, time
from tests.testbase import TestBase
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.types.money import Money
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.entities.idempotencyresponse import IdempotencyResponse
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.user import User
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.usernatural import UserNatural

class Test_Idempotency(TestBase):
    """Test methods for idempotency."""


    def test_Idempotency(self):
        key = random.randrange(100000000000000000, 999999999999999999)
        wallet = self.getJohnsWallet()
        user = self.getJohn()
        account = self.getJohnsAccount()
        
        payOutPost = PayOut()
        payOutPost.AuthorId = user.Id
        payOutPost.DebitedWalletId = wallet.Id
        payOutPost.DebitedFunds = Money(10, 'EUR')
        payOutPost.Fees = Money(5, 'EUR')
        payOutPost.MeanOfPaymentDetails = PayOutPaymentDetailsBankWire()
        payOutPost.MeanOfPaymentDetails.BankAccountId = account.Id
        payOutPost.MeanOfPaymentDetails.BankWireRef = 'Johns bank wire ref'
        payOutPost.Tag = 'DefaultTag'
        payOutPost.CreditedUserId = user.Id

        payOut = self.sdk.payOuts.CreateIdempotent(key, payOutPost)

        self.assertIsNotNone(payOut)

        # test existing key
        result = self.sdk.idempotency.Get(key)
        self.assertIsNotNone(result)

        # test non-existing key
        try:
            result = self.sdk.idempotency.Get(key + '_no')

            # expecting a response error
            self.assertTrue(1 == 0)
        except:
            result = None