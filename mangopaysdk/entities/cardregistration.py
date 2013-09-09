from mangopaysdk.entities.entitybase import EntityBase


class CardRegistration(EntityBase):
    """CardRegistration entity"""

    UserId = ''
    AccessKey = ''
    PreregistrationData = ''
    CardRegistrationURL = ''
    CardId = ''
    CardRegistrationData = ''
    ResultCode = ''
    Currency = ''
    
    # CardRegistrationStatus CREATED, ERROR, VALIDATED
    Status = None	
    
    # Boolean
    Reusable = None

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('AccessKey')
        properties.append('PreregistrationData')
        properties.append('CardRegistrationURL')
        properties.append('CardId')
        properties.append('ResultCode')
        properties.append('Status')
        return properties