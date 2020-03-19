from mangopay import constants
from mangopay.resources import UboDeclaration, Ubo
from mangopay.utils import Birthplace
from tests.test_base import BaseTestLive
from datetime import date


class UbosTests(BaseTestLive):
    def test_create_ubo_declaration(self):
        self.get_user_legal(True)
        created_ubo = self.get_ubo_declaration(True)
        self.assertIsNotNone(created_ubo)

    def test_list_ubo_declarations(self):
        legal_user = self.get_user_legal(True)
        self.get_ubo_declaration(True)
        declarations = UboDeclaration.all(**{"user_id": legal_user.id})
        self.assertIsNotNone(declarations)
        self.assertEqual(1, len(declarations))
        self.assertEqual(self.get_ubo_declaration().id, declarations[0].id)

    def test_get_ubo_declaration(self):
        legal_user = self.get_user_legal(True)
        self.get_ubo_declaration(True)
        fetched_declaration = UboDeclaration.get(self.get_ubo_declaration().get_pk(),
                                                 **{"user_id": legal_user.get_pk()})
        self.assertIsNotNone(fetched_declaration)
        self.assertEqual(self.get_ubo_declaration().id, fetched_declaration.id)

    def test_create_ubo(self):
        new_ubo = self.get_ubo(True)
        self.assertIsNotNone(new_ubo)
        self.assertIsNotNone(new_ubo.id)
        self.assertEqual('Victor', new_ubo.first_name)
        self.assertEqual('Hugo', new_ubo.last_name)
        self.assertEqual('FR', new_ubo.nationality)
        self.assertEqual(date(1970, 1, 15), new_ubo.birthday)
        self.assertEqual(Birthplace(city='Paris', country='FR'), new_ubo.birthplace)

    def test_update_ubo(self):
        to_be_updated = self.get_ubo(True)
        user = self.get_user_legal()
        ubo_declaration = self.get_ubo_declaration()
        address = to_be_updated.address
        address.address_line_1 = 'UpdatedLine1'
        birthplace = to_be_updated.birthplace
        birthplace.country = 'GB'
        params_to_be_updated = {
            "user_id": user.get_pk(),
            "ubo_declaration_id": ubo_declaration.get_pk(),
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "address": address,
            "birthday": 25755342,
            "nationality": "GB",
            "birthplace": birthplace,
            "isActive": True
        }
        updated_ubo = to_be_updated.update(to_be_updated.get_pk(), **params_to_be_updated).execute()

        self.assertEqual(updated_ubo['first_name'], "UpdatedFirstName")
        self.assertEqual(updated_ubo['nationality'], "GB")
        self.assertEqual(updated_ubo["isActive"], True)

    def test_get_ubo(self):
        existing_ubo = self.get_ubo(True)
        user = self.get_user_legal()
        ubo_declaration = self.get_ubo_declaration()

        fetched_ubo = Ubo.get(existing_ubo.get_pk(), **{'user_id' : user.id, 'ubo_declaration_id': ubo_declaration.id })
        self.assertIsNotNone(fetched_ubo)
        self.assertEquals(existing_ubo.first_name, fetched_ubo.first_name)
        self.assertEquals(existing_ubo.last_name, fetched_ubo.last_name)
        self.assertEquals(existing_ubo.address, fetched_ubo.address)
        self.assertEquals(existing_ubo.nationality, fetched_ubo.nationality)
        self.assertEquals(existing_ubo.birthday, fetched_ubo.birthday)
        self.assertEquals(existing_ubo.birthplace, fetched_ubo.birthplace)

    def test_submit_for_validation(self):
        self.get_ubo(True)
        user = self.get_user_legal()
        ubo_declaration = self.get_ubo_declaration()
        params = {
            'user_id': user.id,
            'status': constants.UBO_DECLARATION_STATUS_CHOICES.validation_asked
        }
        new_ubo_declaration = ubo_declaration.update(ubo_declaration.get_pk(), **params).execute()
        self.assertEqual(ubo_declaration.id, new_ubo_declaration['id'])
