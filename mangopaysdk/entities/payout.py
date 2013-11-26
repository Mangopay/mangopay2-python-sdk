from mangopaysdk.entities.transaction import Transaction


class PayOut (Transaction):

    def __init__(self, id = None):
        self.DebitedWalletId = None
        # PayInPaymentType (BANK_WIRE, MERCHANT_EXPENSE, AMAZON_GIFTCARD)
        self.PaymentType = None
        # One of PayOutPaymentDetails implementations, depending on PaymentType
        self.MeanOfPaymentDetails = None
        return super(PayOut, self).__init__(id) 
     
    def GetDependsObjects(self):
        return {
            'PaymentType': {'_property_name': 'MeanOfPaymentDetails', 'BANK_WIRE': 'PayOutPaymentDetailsBankWire'}
        }

    def GetReadOnlyProperties(self):
        properties = super(PayOut, self).GetReadOnlyProperties()
        properties.append('PaymentType' )        
        properties.append('ExecutionType' )        
        return properties