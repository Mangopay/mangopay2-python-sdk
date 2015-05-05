from mangopaysdk.types.dto import Dto


class RefundReason(Dto):
    """Class represents refund reason."""

    def __init__(self):
        self.RefundReasonMessage = None
        self.RefundReasonType = None
