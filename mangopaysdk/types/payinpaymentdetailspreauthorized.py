from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsPreAuthorized(PayInPaymentDetails):
    
    def __init__(self):    
        # The ID of the Preauthorization object
        self.PreauthorizationId = None