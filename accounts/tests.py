from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

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
                "confirm_password": "NewPass123",
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
                "email": "test@example.com",
                "mobile_number": "9876543210",
                "address": "Rajkot",
            },
        )

        self.assertEqual(response.status_code, 302)

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
                "email": "test@example.com",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
                "old_password": "TestPass123",
                "new_password": "NewPass123",
                "confirm_password": "NewPass123",   
            },
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123"))
        
    #----------------------
    # 5. REGISTER PASSWORD MISMATCH
    #----------------------
    def test_register_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "user1",
                "email": "user1@example.com",
                "password": "TestPass123",
                "confirm_password": "WrongPass123",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="user1").exists())

    #-------------------
    #6.LOGIN WRONG PASSWORD
    #-------------------
    def test_login_invalid_password(self):
        response = self.client.post(
           reverse("login"),
            {
               "username": "testuser",
               "password": "WrongPassword",
            },
        )

        self.assertEqual(response.status_code, 200)
        
    #-------------------
    #7.PROFILE WITHOUT LOGIN
    #-------------------
    def test_profile_without_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        
    #-----------------------------------
    #8.PASSWORD CHANGE WRONG OLD PASSWORD
    #------------------------------------
    def test_password_change_wrong_old_password(self):
        self.client.login(username="testuser", password="TestPass123")

        response = self.client.post(
           reverse("profile"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
                "old_password": "WrongPassword",
                "new_password": "NewPass123",
                "confirm_password": "NewPass123",
            },
        )

        self.assertEqual(response.status_code, 200)
    
    # -----------------------
# 5. FORGOT PASSWORD TEST (VALID EMAIL)
# -----------------------
@patch("accounts.views.send_mail")
def test_forgot_password_valid_email(self, mock_send_mail):
    response = self.client.post(
        reverse("forgot_password"),
        {
            "email": "test@example.com",
        },
    )

    self.assertEqual(response.status_code, 302)


# -----------------------
# 6. FORGOT PASSWORD TEST (INVALID EMAIL)
# -----------------------
def test_forgot_password_invalid_email(self):
    response = self.client.post(
        reverse("forgot_password"),
        {
            "email": "wrong@example.com",
        },
    )

    self.assertEqual(response.status_code, 200)


# -----------------------
# 7. VERIFY OTP TEST
# -----------------------
def test_verify_valid_otp(self):
    session = self.client.session
    session["reset_otp"] = "123456"
    session["reset_user"] = self.user.id
    session["otp_expiry"] = "2099-01-01T12:00:00"
    session.save()

    response = self.client.post(
        reverse("verify_otp"),
        {
            "otp": "123456",
        },
    )

    self.assertEqual(response.status_code, 302)


# -----------------------
# 8. RESET PASSWORD TEST
# -----------------------
def test_reset_password(self):
    session = self.client.session
    session["reset_user"] = self.user.id
    session.save()

    response = self.client.post(
        reverse("reset_password"),
        {
            "new_password": "NewPass123",
            "confirm_password": "NewPass123",
        },
    )

    self.assertEqual(response.status_code, 302)

    self.user.refresh_from_db()
    self.assertTrue(self.user.check_password("NewPass123"))