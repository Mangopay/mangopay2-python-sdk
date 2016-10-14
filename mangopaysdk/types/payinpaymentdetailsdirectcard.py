from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsDirectCard(PayInPaymentDetails):
    def __init__(self):
        # CardType enum
        self.CardType = None
        self.SecureModeReturnURL = None
