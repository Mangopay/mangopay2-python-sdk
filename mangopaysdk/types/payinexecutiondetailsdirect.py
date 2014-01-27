from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails


class PayInExecutionDetailsDirect(PayInExecutionDetails):
        
    def __init__(self):
        # direct card
        self.CardId = None
        self.SecureModeReturnURL = None
        # Mode3DSType { DEFAULT, FORCE }
        self.SecureMode = None