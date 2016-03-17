from mangopaysdk.entities.entitybase import EntityBase

class Mandate(EntityBase):
    """Mandate entity."""

    def __init__(self, id = None):
        self.BankAccountId = None
        self.Scheme = None
        self.Culture = None
        self.DocumentURL = None
        self.RedirectURL = None
        self.ReturnURL = None
        self.UserId = None
        self.Status = None
        self.ResultCode = None
        self.ResultMessage = None
        self.MandateType = None
        self.ExecutionType = None
        return super(Mandate, self).__init__(id)