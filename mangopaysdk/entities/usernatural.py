from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.entities.user import User
from mangopaysdk.tools.enums import PersonType
from mangopaysdk.tools.enums import KYCLevel
from mangopaysdk.types.address import Address


class UserNatural(User):

    def __init__(self, id = None):
        super(UserNatural, self).__init__(id)
        self._setPersonType(PersonType.Natural)
        # Required
        self.FirstName = None
        # Required
        self.LastName = None
        self.Address = None
        # Required Date of birth: Unix timestamp
        self.Birthday = None
        # Required
        self.Nationality = None
        # Required
        self.CountryOfResidence = None
        self.Occupation = None
        # Int
        self.IncomeRange = None
        self.ProofOfIdentity = None
        self.ProofOfAddress = None

    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {'Address' : 'Address'}

    def GetReadOnlyProperties(self):
        properties = super(UserNatural, self).GetReadOnlyProperties()
        properties.append('ProofOfIdentity' )        
        properties.append('ProofOfAddress' )        
        return properties