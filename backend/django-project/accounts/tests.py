from django.test import override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from accounts.models import User


@override_settings(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
)
class AccountsAuthTests(APITestCase):
    def setUp(self):
        self.client: APIClient
        self.user = User.objects.create_user(
            email="tester@example.edu",
            username="tester",
            password="testpass123",
        )

    def test_me_requires_auth(self):
        resp = self.client.get("/api/accounts/me/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_with_token(self):
        resp_login = self.client.post(
            "/api/login/",
            {"email": "tester@example.edu", "password": "testpass123"},
            format="json",
        )
        token = resp_login.cookies.get("auth_token")
        self.assertIsNotNone(token)
        self.client.cookies["auth_token"] = token.value

        resp = self.client.get("/api/accounts/me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], "tester@example.edu")
