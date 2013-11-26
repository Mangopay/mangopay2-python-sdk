from mangopaysdk.entities.entitybase import EntityBase


class User(EntityBase):

    def __init__(self, id = None):
        super(User, self).__init__(id)
        # Required
        self.Email = None
        # PersonType
        self.PersonType = None

    def _setPersonType(self, personType):
        self.PersonType = personType

    def GetReadOnlyProperties(self):
        properties = super(User, self).GetReadOnlyProperties()
        properties.append('PersonType' )        
        return properties