from mangopaysdk.entities.entitybase import EntityBase


class DisputeDocument (EntityBase):
    """DisputeDocument entity."""

    def __init__(self, id = None):
        self.DisputeId = None
        # DisputeDocumentType:
        self.Type = None
        # DisputeDocumentStatus
        self.Status = None
        self.RefusedReasonType = None
        self.RefusedReasonMessage = None
        return super(DisputeDocument, self).__init__(id)

    def GetReadOnlyProperties(self):
        properties = super(DisputeDocument, self).GetReadOnlyProperties()
        properties.append('CreationDate')
        properties.append('RefusedReasonType')
        properties.append('RefusedReasonMessage')
        return properties