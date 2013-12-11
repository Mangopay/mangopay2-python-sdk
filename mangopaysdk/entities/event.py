from mangopaysdk.entities.entitybase import EntityBase


class Event (EntityBase):
    """Event entity."""
    
    def __init__(self, id = None):
        self.ResourceId = ''
        # EventType enum
        self.EventType = None
        # Unix timestamp
        self.Date = None
       
        return super(Event, self).__init__(id)
    
