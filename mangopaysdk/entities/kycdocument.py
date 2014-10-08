from mangopaysdk.entities.entitybase import EntityBase


class KycDocument (EntityBase):
    """KycDocument entity."""

    def __init__(self, id = None):
        self.Tag = ''
        self.UserId = None
        # KycDocumentType:
        self.Type = None
        # KycDocumentStatus
        self.Status = None
        # timestamp
        self.CreationDate = None
        self.RefusedReasonType = None
        self.RefusedReasonMessage = None
        return super(KycDocument, self).__init__(id)

    def GetReadOnlyProperties(self):
        properties = super(KycDocument, self).GetReadOnlyProperties()
        properties.append('CreationDate')
        properties.append('RefusedReasonType')
        properties.append('RefusedReasonMessage')
        return properties