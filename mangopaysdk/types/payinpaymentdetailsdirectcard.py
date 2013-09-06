from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails


class PayInPaymentDetailsDirectCard(PayInExecutionDetails):
        
    # CardType { CB_VISA_MASTERCARD, AMEX }
    CardType = None
    
    SecureModeReturnURL = ''