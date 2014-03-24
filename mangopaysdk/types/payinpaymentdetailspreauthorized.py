from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsPreAuthorized(PayInPaymentDetails):
    """Class represents PreAuthorized type for mean of payment in PayIn entity."""
    
    def __init__(self):    
        # The ID of the Preauthorization object
        self.PreauthorizationId = None