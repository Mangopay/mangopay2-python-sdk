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