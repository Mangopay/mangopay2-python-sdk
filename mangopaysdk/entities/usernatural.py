from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.entities.user import User
from mangopaysdk.tools.enums import PersonType


class UserNatural(User):

    def __init__(self, id = None):
        super(UserNatural, self).__init__(id)
        self._setPersonType(PersonType.Natural)

        self.FirstName = None
        self.LastName = None
        self.Address = None
        # Date of birth: Unix timestamp
        self.Birthday = None
        self.Nationality = None
        self.CountryOfResidence = None
        self.Occupation = None
        # Int
        self.IncomeRange = None
        self.ProofOfIdentity = None
        self.ProofOfAddress = None

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('ProofOfIdentity' )        
        properties.append('ProofOfAddress' )        
        return properties