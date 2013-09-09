from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsCard(PayInPaymentDetails):
    """Class represents Card type for mean of payment in PayIn entity."""

    def __init__(self):
        # CardType { CB_VISA_MASTERCARD, AMEX }
        self.CardType = None