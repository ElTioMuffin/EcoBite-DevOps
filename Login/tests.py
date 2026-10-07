from django.test import Client, SimpleTestCase

from Login.models import Users, userType


class LoginModelContractTests(SimpleTestCase):
    def test_custom_user_configuration(self):
        self.assertEqual(Users.USERNAME_FIELD, "email")
        self.assertTrue(Users._meta.get_field("email").unique)

    def test_user_type_model_is_available(self):
        self.assertEqual(userType._meta.model_name, "usertype")


class HealthCheckTests(SimpleTestCase):
    def test_health_check_reports_version(self):
        response = Client().get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "ok",
            "service": "EcoBite",
            "version": "1.1.0",
        })
