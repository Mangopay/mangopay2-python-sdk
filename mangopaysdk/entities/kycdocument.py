from mangopaysdk.entities.entitybase import EntityBase


class KycDocument (EntityBase):
    """KycDocument entity."""
    
    def __init__(self, id = None):
        self.Tag = ''
        # KycDocumentType:
        self.Type = None
        # KycDocumentStatus
        self.Status = None
        # timestamp
        self.CreationDate = None
        self.RefusedReasonType = None
        self.RefusedReasonMessage = None     
        return super().__init__(id)

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('CreationDate')        
        properties.append('RefusedReasonType') 
        properties.append('RefusedReasonMessage')        
        return properties