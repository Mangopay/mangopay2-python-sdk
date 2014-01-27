from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails

class PayInPaymentDetailsBankWire(PayInPaymentDetails):
    """Class represents BankWire type for mean of payment in PayIn entity."""

    def __init__(self):
        self.BankAccount = None
        self.WireReference = None
        self.DeclaredDebitedFunds = None
        self.DeclaredFees = None

    def GetSubObjects(self):
        return {'BankAccount': 'BankAccount'}