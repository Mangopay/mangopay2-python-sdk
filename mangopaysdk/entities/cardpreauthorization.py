from mangopaysdk.entities.entitybase import EntityBase


class CardPreAuthorization(EntityBase):
    """CardPreAuthorization entity"""
    
    def __init__(self, id = None):
        self.Tag = None
        # The user Id of the author of the pre-authorization
        self.AuthorId = None
        # Money object - amount debited on the bank account of the Author in cents
        self.DebitedFunds = None
        # Mode3DSType { DEFAULT, FORCE }
        self.SecureMode = None
        # This is the URL where users are automatically redirected after 3D secure validation (if activated)
        self.SecureModeReturnURL = None
        # The ID of the registered card (Got through CardRegistration object) 
        self.CardId = None
         # The Id of the associated PayIn
        self.PayInId = None

        # Boolean. The value is 'true' if the SecureMode was used
        self.SecureModeNeeded = None
        # This is the URL where users are automatically redirected after 3D secure validation (if activated)
        self.SecureModeReturnURL = None 
        # returned from API
        self.SecureModeRedirectURL = None
        # CardPreAuthorizationStatus - The status of the payment after the PreAuthorization: WAITING, CANCELED, EXPIRED, VALIDATED
        
        self.PaymentStatus = None
        # TransactionStatus: CREATED, SUCCEEDED, FAILED
        self.Status = None
        self.ResultCode = None
        self.ResultMessage = None
        # How the PreAuthorization has been executed. 
        self.ExecutionType = None
        # The date when the payment is processed
        self.ExpirationDate = None
        self.StatementDescriptor = None

        return super(CardPreAuthorization, self).__init__(id)

    def GetReadOnlyProperties(self):
        properties = super(CardPreAuthorization, self).GetReadOnlyProperties()
        properties.append('ResultMessage')
        properties.append('ResultCode')
        properties.append('Status')
        return properties
    
    def GetSubObjects(self):
        return { 
            'DebitedFunds': 'Money'
        }



    
    
