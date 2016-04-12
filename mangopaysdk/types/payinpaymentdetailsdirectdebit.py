from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsDirectDebit(PayInPaymentDetails):
    
    def __init__(self):
        self.DirectDebitType = None
        self.MandateId = None