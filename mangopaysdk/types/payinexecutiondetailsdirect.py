from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails


class PayInExecutionDetailsDirect(PayInExecutionDetails):
        
    def __init__(self):
        # direct card
        self.CardId = None
        self.SecureModeReturnURL = None
        self.SecureModeRedirectURL = None
        self.SecureModeNeeded = None
        # Mode3DSType { DEFAULT, FORCE }
        self.SecureMode = None
        self.StatementDescriptor = None
