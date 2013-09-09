from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails


class PayInPaymentDetailsDirectCard(PayInExecutionDetails):
    
    def __init__(self):    
        # CardType { CB_VISA_MASTERCARD, AMEX }
        self.CardType = None    
        self.SecureModeReturnURL = None