from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthTests(TestCase):
    def setUp(self):
        self.username = "testcook"
        self.password = "secret123"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="Test",
            last_name="Cook",
            years_of_experience=5,
        )

    def test_login_valid_user(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.username, "password": self.password}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.username, "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "kitchen/registration/logged_out.html")
