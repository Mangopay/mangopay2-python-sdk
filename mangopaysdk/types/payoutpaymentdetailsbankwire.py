from mangopaysdk.types.payoutpaymentdetails import PayOutPaymentDetails


class PayOutPaymentDetailsBankWire(PayOutPaymentDetails):
    """Class represents BankWire type for mean of payment in PayOut entity."""

    def __init__(self):
        self.BankAccountId = None
        self.BankWireRef = None
