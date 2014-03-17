from mangopaysdk.types.bankaccountdetails import BankAccountDetails


class BankAccountDetailsCA(BankAccountDetails):
    """CA bank account type for BankAccount entity."""

    def __init__(self):
        self.BankName = None
        """Bank name"""
    
        self.InstitutionNumber = None
        """Institution number"""
    
        self.BranchCode = None
        """Branch code"""
    
        self.AccountNumber = None
        """Account number"""
