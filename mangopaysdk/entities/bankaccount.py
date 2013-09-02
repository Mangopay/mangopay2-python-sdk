from mangopaysdk.entities.entitybase import EntityBase


class BankAccount(EntityBase):
    """Bank Account entity."""

    UserId = 0

    # Type of bank account
    Type = 'IBAN'

    OwnerName = ''

    OwnerAddress = '';

    # must be valid ^[a-zA-Z]{2}\d{2}\s*(\w{4}\s*){2,7}\w{1,4}$
    IBAN = ''

    # example BREXPLPWKRA
    BIC = ''

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('UserId' )        
        return properties