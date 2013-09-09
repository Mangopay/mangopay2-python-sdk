from mangopaysdk.entities.entitybase import EntityBase


class Client (EntityBase):
    """Client entity."""
    
    def __init__(self, id = None):
        # Client identifier
        self.ClientId = None
        # Name of client
        self.Name = None
        # Email of client
        self.Email = None
        # Password for client
        self.Passphrase = None
        return super().__init__(id)
    
