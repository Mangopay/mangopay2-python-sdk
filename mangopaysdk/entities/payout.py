from mangopaysdk.entities.transaction import Transaction


class PayOut (Transaction):

    DebitedWalletId = 0

    # PayInPaymentType (BANK_WIRE, MERCHANT_EXPENSE, AMAZON_GIFTCARD)
    PaymentType = ''

    # One of PayOutPaymentDetails implementations, depending on $PaymentType
    MeanOfPaymentDetails = None

    def GetDependsObjects(self):
        return {
            'PaymentType': {'_property_name': 'MeanOfPaymentDetails', 'BANK_WIRE': 'PayOutPaymentDetailsBankWire'}
        }

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('PaymentType' )        
        properties.append('ExecutionType' )        
        return properties