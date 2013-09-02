from mangopaysdk.entities.entitybase import EntityBase


class Client (EntityBase):
    """Client entity."""
    
    # Client identifier
    ClientId = 0
    
    # Name of client
    Name = ''
    
    # Email of client
    Email = ''
    
    # Password for client
    Passphrase = ''
