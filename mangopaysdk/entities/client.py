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
        return super(Client, self).__init__(id)
    
