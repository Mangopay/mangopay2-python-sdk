import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.transfer import Transfer


class Test_Transfers(TestBase):
    "Tests basic methods for transfers"
     
    def test_Transfers_Create(self):
       john = self.getJohn()
       transfer = self.getJohnsTransfer()
       self.assertTrue(int(transfer.Id) > 0)
       self.assertEqual(transfer.AuthorId, john.Id)
       self.assertEqual(transfer.CreditedUserId, john.Id)
    
    def test_Transfers_Get(self):
       john = self.getJohn()
       transfer = self.getJohnsTransfer()
       getTransfer = self.sdk.transfers.Get(transfer.Id)
       self.assertEqual(transfer.Id, getTransfer.Id)
       self.assertEqual(getTransfer.AuthorId, john.Id)
       self.assertEqual(getTransfer.CreditedUserId, john.Id)
       self.assertEqualInputProps(transfer, getTransfer)

if __name__ == '__main__':
    unittest.main()