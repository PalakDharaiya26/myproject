from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPass123"
        )

    # -----------------------
    # 1. REGISTER TEST
    # -----------------------
    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "NewPass123",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # -----------------------
    # 2. LOGIN TEST
    # -----------------------
    def test_login_user(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "TestPass123"}
        )

        self.assertEqual(response.status_code, 302)

    # -----------------------
    # 3. PROFILE UPDATE TEST
    # -----------------------
    def test_profile_update(self):
        self.client.login(username="testuser", password="TestPass123")

        response = self.client.post(
            reverse("profile"),
            {
                "username": "updateduser",
                "mobile_number": "9876543210",
                "address": "Rajkot",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    # -----------------------
    # 4. PASSWORD CHANGE TEST
    # -----------------------
    def test_password_change(self):
        self.client.login(username="testuser", password="TestPass123")

        response = self.client.post(
            reverse("profile"),
            {
                "username": "testuser",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
                "old_password": "TestPass123",
                "new_password": "NewPass123",
                "confirm_password": "NewPass123",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123"))

    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "NewPass123",
                "confirm_password": "NewPass123",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
