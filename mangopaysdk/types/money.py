from mangopaysdk.types.dto import Dto


class Money(Dto):
    """Class represents money value with currency."""

    # Text with currency code with ISO 4217 standard
    Currency = ''

    Amount = 0

    def __init__(self, amount = 0, currency = 'EUR'):
        self.Amount = amount
        self.Currency = currency
