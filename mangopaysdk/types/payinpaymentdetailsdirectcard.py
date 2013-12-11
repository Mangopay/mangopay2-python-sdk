from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails


class PayInPaymentDetailsDirectCard(PayInExecutionDetails):
    
    def __init__(self):    
        # CardType enum
        self.CardType = None    
        self.SecureModeReturnURL = None