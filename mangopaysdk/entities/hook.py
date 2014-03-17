from mangopaysdk.entities.entitybase import EntityBase

class Hook(EntityBase):
    """Hooks and Notifications entity."""

    def __init__(self, id = None):
        self.Url = None
        self.Status = None
        self.Validity = None
        self.EventType = None
        return super(Hook, self).__init__(id)