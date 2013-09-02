from mangopaysdk.types.dto import Dto


class EntityBase(Dto):
    """Abstract class with common properties for all entities."""

    def GetReadOnlyProperties(self):
        return ['Id', 'CreationDate']

    def __init__(self, id = None):
        # String Unique identifier (at this moment values are integers; may be replaced by GUIDs in future)
        self.Id = id
        # String Custom data
        self.Tag = None
        # Integer Unix timestamp of creation
        self.CreationDate = None
