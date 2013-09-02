from mangopaysdk.entities.transaction import Transaction


class PayIn (Transaction):

    CreditedWalletId = 0

    # PayInPaymentType {CARD, BANK_WIRE, AUTOMATIC_DEBIT, DIRECT_DEBIT }
    PaymentType = None

    # One of PayInPaymentDetails implementations, depending on PaymentType
    PaymentDetails = None

    # ExecutionType { WEB, TOKEN, DIRECT, PREAUTHORIZED, RECURRING_ORDER_EXECUTION }
    ExecutionType = ''

    # One of PayInExecutionDetails implementations, depending on ExecutionType
    ExecutionDetails = None

    def GetDependsObjects(self):
        return { 
                'PaymentType': {'_property_name': 'PaymentDetails', 'CARD': 'PayInPaymentDetailsCard'},
                'ExecutionType': {'_property_name': 'ExecutionDetails', 'WEB': 'PayInExecutionDetailsWeb'} 
               }

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('PaymentType' )        
        properties.append('ExecutionType' )        
        return properties