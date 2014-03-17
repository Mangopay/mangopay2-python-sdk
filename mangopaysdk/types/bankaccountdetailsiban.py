from mangopaysdk.types.bankaccountdetails import BankAccountDetails


class BankAccountDetailsIBAN(BankAccountDetails):
    """IBAN bank account type for BankAccount entity."""

    def __init__(self):
        self.IBAN = None
        """IBAN number"""

        self.BIC = None
        """BIC"""
