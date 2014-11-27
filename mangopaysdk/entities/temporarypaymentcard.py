from mangopaysdk.entities.entitybase import EntityBase


class TemporaryPaymentCard(EntityBase):
    """WARNING! 
    This is temporary entity and will be removed in future.
    Contact support before using these features or if have any queries.
    
    TemporaryPaymentCard entity
    """
    
    def __init__(self, id = None):
        self.UserId = None
        self.Culture = None
        self.ReturnURL = None
        self.TemplateURL = None
        self.RedirectURL = None
        self.Alias = None
        return super(TemporaryPaymentCard, self).__init__(id)
    
