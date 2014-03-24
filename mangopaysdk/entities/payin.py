from mangopaysdk.entities.transaction import Transaction


class PayIn (Transaction):

    def __init__(self, id = None):
        self.CreditedWalletId = None
        # PayInPaymentType {CARD, BANK_WIRE, AUTOMATIC_DEBIT, DIRECT_DEBIT, PREAUTHORIZED }
        self.PaymentType = None
        # One of PayInPaymentDetails implementations, depending on PaymentType
        self.PaymentDetails = None
        # ExecutionType { WEB, TOKEN, DIRECT, PREAUTHORIZED, RECURRING_ORDER_EXECUTION }
        self.ExecutionType = None
        # One of PayInExecutionDetails implementations, depending on ExecutionType
        self.ExecutionDetails = None
        return super(PayIn, self).__init__(id)    
    
    def GetDependsObjects(self):
        return { 
                'PaymentType': {
                    '_property_name': 'PaymentDetails', 
                    'CARD': 'PayInPaymentDetailsCard',
                    'PREAUTHORIZED': 'PayInPaymentDetailsPreAuthorized',
                    'BANK_WIRE': 'PayInPaymentDetailsBankWire'
                }, 'ExecutionType': {
                    '_property_name': 'ExecutionDetails', 
                    'WEB': 'PayInExecutionDetailsWeb',
                    'DIRECT': 'PayInExecutionDetailsDirect'                
                }
        }

    def GetReadOnlyProperties(self):
        properties = super(PayIn, self).GetReadOnlyProperties()
        properties.append('PaymentType' )        
        properties.append('ExecutionType' )        
        return properties