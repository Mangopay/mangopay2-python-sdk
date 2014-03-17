from mangopaysdk.types.bankaccountdetails import BankAccountDetails


class BankAccountDetailsOTHER(BankAccountDetails):
    """OTHER bank account type for BankAccount entity."""

    def __init__(self):
        self.Type = None
        """Type"""
    
        self.Country = None
        """The Country associate to the BankAccount,
        ISO 3166-1 alpha-2 format is expected"""
    
        self.BIC = None
        """Valid BIC format"""
    
        self.AccountNumber = None
        """Account number"""
