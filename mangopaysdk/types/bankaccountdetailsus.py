from mangopaysdk.types.bankaccountdetails import BankAccountDetails


class BankAccountDetailsUS(BankAccountDetails):
    """GB bank account type for BankAccount entity."""

    def __init__(self):
        self.AccountNumber = None
        """Account number"""

        self.ABA = None
        """ABA"""
