from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails


class PayInPaymentDetailsCard(PayInPaymentDetails):
    """Class represents Card type for mean of payment in PayIn entity."""

    # CardType { CB_VISA_MASTERCARD, AMEX }
    CardType = ''

    # URL format expected
    RedirectURL = ''

    # URL format expected
    ReturnURL = ''
