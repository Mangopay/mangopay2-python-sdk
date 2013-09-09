from mangopaysdk.types.dto import Dto


class Money(Dto):
    """Class represents money value with currency."""

    def __init__(self, amount = 0, currency = 'EUR'):
        self.Amount = amount
        # Text with currency code with ISO 4217 standard
        self.Currency = currency
