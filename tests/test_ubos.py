import requests
import responses

from mangopay import constants
from mangopay.resources import UboDeclaration, Ubo
from mangopay.utils import Address, Birthplace
from tests.test_base import BaseTest

requests_session = requests.Session()


class UbosTests(BaseTest):

    @responses.activate
    def test_create_ubo_declaration(self):
        self.mock_ubo_declaration()
        ubo_declaration, user = self.legal_user_ubo_declaration

        self.assertTrue(isinstance(ubo_declaration, UboDeclaration))
        self.assertIsNotNone(ubo_declaration.id)
        self.assertEquals(ubo_declaration.id, "122341")
        self.assertEquals(ubo_declaration.status, "CREATED")

    @responses.activate
    def test_list_ubo_declarations(self):
        self.mock_list_ubo_declarations()
        ubo_declaration, user = self.legal_user_ubo_declaration

        declarations = UboDeclaration.all(**{"user_id": "11694190"})
        self.assertIsNotNone(declarations)
        self.assertEquals(1, len(declarations))
        self.assertEquals(ubo_declaration.id, declarations[0].id)

    @responses.activate
    def test_get_ubo_declaration(self):
        self.mock_get_ubo_declaration()

        ubo_declaration, user = self.legal_user_ubo_declaration
        fetched_declaration = UboDeclaration.get(ubo_declaration.get_pk(), **{"user_id": user.get_pk()})
        self.assertIsNotNone(fetched_declaration)
        self.assertEquals(ubo_declaration.id, fetched_declaration.id)

    @responses.activate
    def test_create_ubo(self):
        self.mock_ubo_creation()

        ubo_declaration, user = self.legal_user_ubo_declaration
        ubo = self.ubo_declaration_ubo

        params = {
            "user": user,
            "ubo_declaration": ubo_declaration,
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": 1231432,
            "nationality": "FR",
            "birthplace": Birthplace(city='Paris', country='FR')
        }
        new_ubo = Ubo.create(**params)

        self.assertIsNotNone(new_ubo)
        self.assertIsNotNone(new_ubo.id)
        self.assertEquals(ubo.first_name, new_ubo.first_name)
        self.assertEquals(ubo.last_name, new_ubo.last_name)
        self.assertEquals(ubo.address, new_ubo.address)
        self.assertEquals(ubo.nationality, new_ubo.nationality)
        self.assertEquals(ubo.birthday, new_ubo.birthday)
        self.assertEquals(ubo.birthplace, new_ubo.birthplace)

    @responses.activate
    def test_update_ubo(self):
        self.mock_ubo_creation()
        self.mock_get_ubo()
        self.mock_update_ubo()
        ubo_declaration, user = self.legal_user_ubo_declaration

        params = {
            "user": user,
            "ubo_declaration": ubo_declaration,
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": 1231432,
            "nationality": "FR",
            "birthplace": Birthplace(city='Paris', country='FR')
        }
        to_be_updated = Ubo.create(**params)

        params_to_be_updated = {
            "user_id": user.get_pk(),
            "ubo_declaration_id": ubo_declaration.get_pk(),
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "address": Address(address_line_1='UpdatedLine1'),
            "birthday": 25755342,
            "nationality": "GB",
            "birthplace": Birthplace(country='GB')
        }
        updated_ubo = to_be_updated.update(to_be_updated.get_pk(), **params_to_be_updated).execute()

        self.assertEquals(updated_ubo['first_name'], "UpdatedFirstName")
        self.assertEquals(updated_ubo['nationality'], "GB")

    @responses.activate
    def test_get_ubo(self):
        self.mock_ubo_creation()
        self.mock_get_ubo()

        ubo_declaration, user = self.legal_user_ubo_declaration
        params = {
            "user": user,
            "ubo_declaration": ubo_declaration,
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": 1231432,
            "nationality": "FR",
            "birthplace": Birthplace(city='Paris', country='FR')
        }
        existing_ubo = Ubo.create(**params)

        params = {
            "user_id": user.id,
            "ubo_declaration_id": ubo_declaration.id,
            "ubo_id": existing_ubo.get_pk()
        }

        fetched_ubo = Ubo.get("", **params)
        self.assertIsNotNone(fetched_ubo)
        self.assertEquals(existing_ubo.first_name, fetched_ubo.first_name)
        self.assertEquals(existing_ubo.last_name, fetched_ubo.last_name)
        self.assertEquals(existing_ubo.address, fetched_ubo.address)
        self.assertEquals(existing_ubo.nationality, fetched_ubo.nationality)
        self.assertEquals(existing_ubo.birthday, fetched_ubo.birthday)
        self.assertEquals(existing_ubo.birthplace, fetched_ubo.birthplace)

    @responses.activate
    def test_submit_for_validation(self):
        self.mock_submit_ubo_declaration()

        ubo_declaration, user = self.legal_user_ubo_declaration
        ubo_declaration.status = constants.UBO_DECLARATION_STATUS_CHOICES.validation_asked
        new_ubo_declaration = ubo_declaration.update(ubo_declaration.get_pk(), **{"user_id": user.get_pk()}).execute()
        self.assertEquals(ubo_declaration.id, new_ubo_declaration['id'])
