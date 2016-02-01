from mangopaysdk.entities.entitybase import EntityBase

class IdempotencyResponse(EntityBase):
    """IdempotencyResponse entity."""

    def __init__(self, id = None):
        self.StatusCode = None
        self.ContentLength = None
        self.ContentType = None
        self.Date = None
        self.Resource = None
        return super(IdempotencyResponse, self).__init__(id)