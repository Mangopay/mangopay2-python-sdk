from mangopaysdk.types.bankaccountdetails import BankAccountDetails


class BankAccountDetailsGB(BankAccountDetails):
    """GB bank account type for BankAccount entity."""

    def __init__(self):
        self.AccountNumber = None
        """Account number"""

        self.SortCode = None
        """Sort code"""
