from mangopaysdk.entities.entitybase import EntityBase


class CardRegistration(EntityBase):
    """CardRegistration entity"""
    
    def __init__(self, id = None):
        self.UserId = None
        self.AccessKey = None
        self.PreregistrationData = None
        self.CardRegistrationURL = None
        self.CardId = None
        self.RegistrationData = None
        self.ResultCode = None
        self.Currency = None
        # CardRegistrationStatus CREATED, ERROR, VALIDATED
        self.Status = None	
        return super().__init__(id)
   

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('AccessKey')
        properties.append('PreregistrationData')
        properties.append('CardRegistrationURL')
        properties.append('CardId')
        properties.append('ResultCode')
        properties.append('Status')
        return properties