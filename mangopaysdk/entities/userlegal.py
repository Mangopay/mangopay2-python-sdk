from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.entities.user import User
from mangopaysdk.tools.enums import PersonType
from mangopaysdk.tools.enums import KYCLevel
from mangopaysdk.types.address import Address


class UserLegal (User):

    def __init__(self, id = None):
        super(UserLegal, self).__init__(id)
        self._setPersonType(PersonType.Legal)

        self.Name = None
        # Required  LegalPersonType: BUSINESS, ORGANIZATION, SOLETRADER
        self.LegalPersonType = None
        self.HeadquartersAddress = None
        # Required
        self.LegalRepresentativeFirstName = None
        # Required
        self.LegalRepresentativeLastName = None
        self.LegalRepresentativeAddress = None
        self.LegalRepresentativeEmail = None
        # Required
        self.LegalRepresentativeBirthday = None
        # Required
        self.LegalRepresentativeNationality = None
        # Required
        self.LegalRepresentativeCountryOfResidence = None
        self._statute = None
        self._proofOfRegistration = None
        self._shareholderDeclaration = None
        self._legalRepresentativeProofOfIdentity = None

    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {
            'HeadquartersAddress' : 'Address',
            'LegalRepresentativeAddress' : 'Address'
        }

    def GetReadOnlyProperties(self):
        properties = super(UserLegal, self).GetReadOnlyProperties()
        properties.append('Statute' )        
        properties.append('ProofOfRegistration' )        
        properties.append('ShareholderDeclaration' )
        properties.append('LegalRepresentativeProofOfIdentity' )
        return properties
