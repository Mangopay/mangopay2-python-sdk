from mangopaysdk.entities.entitybase import EntityBase


class Dispute (EntityBase):
    """Dispute entity."""
    
    def __init__(self, id = None):
        
        self.InitialTransactionId = None
        self.InitialTransactionType = None
        self.DisputeType = None
        self.ContestDeadlineDate = None
        self.DisputeReason = None
        self.DisputedFunds = None
        self.ContestedFunds = None
        self.Status = None
        self.StatusMessage = None
        self.ResultCode = None
        self.ResultMessage = None

        return super(Dispute, self).__init__(id)