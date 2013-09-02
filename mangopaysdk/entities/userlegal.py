from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.entities.user import User
from mangopaysdk.tools.enums import PersonType


class UserLegal (User):

    def __init__(self, id = None):
        super(UserLegal, self).__init__(id)
        self._setPersonType(PersonType.Legal)

        self.Name = None
        # Type for legal user. Possible: BUSINESS, ORGANIZATION
        self.LegalPersonType = None
        self.HeadquartersAddress = None
        self.LegalRepresentativeFirstName = None
        self.LegalRepresentativeLastName = None
        self.LegalRepresentativeAddress = None
        self.LegalRepresentativeEmail = None
        self.LegalRepresentativeBirthday = None
        self.LegalRepresentativeNationality = None
        self.LegalRepresentativeCountryOfResidence = None
        self._statute = None
        self._proofOfRegistration = None
        self._shareholderDeclaration = None

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('Statute' )        
        properties.append('ProofOfRegistration' )        
        properties.append('ShareholderDeclaration' )        
        return properties
