from django.test import SimpleTestCase
from Login.models import Users, userType


class LoginModelContractTests(SimpleTestCase):
    def test_custom_user_configuration(self):
        self.assertEqual(Users.USERNAME_FIELD, "email")
        self.assertTrue(Users._meta.get_field("email").unique)

    def test_user_type_model_is_available(self):
        self.assertEqual(userType._meta.model_name, "usertype")
