from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import PasswordResetOTP

User = get_user_model()


class AccountsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
        )

    # -----------------------
    # REGISTER SUCCESS TEST
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
    # REGISTER PASSWORD MISMATCH
    # -----------------------
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

    # -----------------------
    # LOGIN SUCCESS TEST
    # -----------------------
    def test_login_user(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "TestPass123",
            },
        )

        self.assertEqual(response.status_code, 302)

    # -----------------------
    # LOGIN WRONG PASSWORD
    # -----------------------
    def test_login_invalid_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "WrongPassword",
            },
        )

        self.assertEqual(response.status_code, 200)

    # -----------------------
    # PROFILE UPDATE TEST
    # -----------------------
    def test_profile_update(self):
        self.client.login(
            username="testuser",
            password="TestPass123",
        )

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
    # PASSWORD CHANGE TEST
    # -----------------------
    def test_password_change(self):
        self.client.login(
            username="testuser",
            password="TestPass123",
        )

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

    # -----------------------
    # WRONG OLD PASSWORD TEST
    # -----------------------
    def test_password_change_wrong_old_password(self):
        self.client.login(
            username="testuser",
            password="TestPass123",
        )

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
    # PROFILE WITHOUT LOGIN
    # -----------------------
    def test_profile_without_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)

    # -----------------------
    # FORGOT PASSWORD SUCCESS
    # -----------------------
    @patch("accounts.views.send_mail")
    def test_forgot_password_success(self, mock_send_mail):

        response = self.client.post(
            reverse("forgot_password"),
            {
                "email": "test@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)

        session = self.client.session

        self.assertTrue(PasswordResetOTP.objects.filter(user=self.user).exists())

        self.assertEqual(session["reset_user"], self.user.id)

        mock_send_mail.assert_called_once()

    # -----------------------
    # FORGOT PASSWORD INVALID EMAIL
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
    # VERIFY OTP SUCCESS
    # -----------------------
    def test_verify_valid_otp(self):

        session = self.client.session

        PasswordResetOTP.objects.create(
            user=self.user,
            otp="123456",
            expiry_time=timezone.now() + timedelta(minutes=2),
        )

        session = self.client.session
        session["reset_user"] = self.user.id
        session.save()

        response = self.client.post(
            reverse("verify_otp"),
            {
                "otp": "123456",
            },
        )

        self.assertEqual(response.status_code, 302)

    # -----------------------
    # VERIFY OTP INVALID
    # -----------------------
    def test_verify_invalid_otp(self):

        session = self.client.session

        PasswordResetOTP.objects.create(
            user=self.user,
            otp="123456",
            expiry_time=timezone.now() + timedelta(minutes=2),
        )

        session = self.client.session
        session["reset_user"] = self.user.id
        session.save()

        response = self.client.post(
            reverse("verify_otp"),
            {
                "otp": "000000",
            },
        )

        self.assertEqual(response.status_code, 200)

    # -----------------------
    # RESET PASSWORD SUCCESS
    # -----------------------
    def test_reset_password(self):

        session = self.client.session
        session["reset_user"] = self.user.id
        session["otp_verified"] = True
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

    # -----------------------
    # LOGOUT TEST
    # -----------------------
    def test_logout_user(self):

        self.client.login(
            username="testuser",
            password="TestPass123",
        )

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)

    # -----------------------
    # DASHBOARD TEST
    # -----------------------
    def test_dashboard_view(self):

        self.client.login(
            username="testuser",
            password="TestPass123",
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    # -----------------------
    # VERIFY OTP NOT FOUND
    # -----------------------
    def test_verify_otp_not_found(self):
        session = self.client.session
        session["reset_user"] = self.user.id
        session.save()

        response = self.client.post(
            reverse("verify_otp"),
            {
                "otp": "123456",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("forgot_password"))

    # -----------------------
    # VERIFY OTP EXPIRED
    # -----------------------
    def test_verify_expired_otp(self):

        PasswordResetOTP.objects.create(
            user=self.user,
            otp="123456",
            expiry_time=timezone.now() - timedelta(minutes=1),
        )

        session = self.client.session
        session["reset_user"] = self.user.id
        session.save()

        response = self.client.post(
            reverse("verify_otp"),
            {
                "otp": "123456",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("forgot_password"))

    # -----------------------
    # RESET PASSWORD USER NOT FOUND
    # -----------------------
    def test_reset_password_user_not_found(self):

        session = self.client.session
        session["reset_user"] = 99999
        session["otp_verified"] = True
        session.save()

        response = self.client.get(reverse("reset_password"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("forgot_password"))

    # -----------------------
    # RESEND OTP USER NOT FOUND
    # -----------------------
    @patch("accounts.views.send_mail")
    def test_resend_otp_user_not_found(self, mock_send_mail):

        session = self.client.session
        session["reset_user"] = 99999
        session["otp_verified"] = True
        session.save()

        response = self.client.get(reverse("resend_otp"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("forgot_password"))

        mock_send_mail.assert_not_called()

    # -----------------------
    # DUPLICATE EMAIL REGISTRATION
    # -----------------------
    def test_register_duplicate_email(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "TestPass123",
                "confirm_password": "TestPass123",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.filter(email="test@example.com").count(),
            1,
        )

    # -----------------------
    # RESET PASSWORD WEAK PASSWORD
    # ------------------------
    def test_reset_password_weak_password(self):

        session = self.client.session
        session["reset_user"] = self.user.id
        session["otp_verified"] = True
        session.save()

        response = self.client.post(
            reverse("reset_password"),
            {
                "new_password": "123456",
                "confirm_password": "123456",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertFalse(self.user.check_password("123456"))

    # -----------------------
    # PROFILE DUPLICATE USERNAME
    # -----------------------
    def test_profile_duplicate_username(self):

        User.objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="TestPass123",
        )

        self.client.login(
            username="testuser",
            password="TestPass123",
        )

        response = self.client.post(
            reverse("profile"),
            {
                "username": "anotheruser",
                "email": "test@example.com",
                "mobile_number": "1234567890",
                "address": "Ahmedabad",
            },
        )

        self.assertEqual(response.status_code, 200)

    # -----------------------
    # RESEND OTP MULTIPLE TIMES
    # -----------------------
    @patch("accounts.views.send_mail")
    def test_resend_otp_multiple_times(self, mock_send_mail):

        session = self.client.session
        session["reset_user"] = self.user.id
        session["otp_verified"] = True
        session.save()

        self.client.get(reverse("resend_otp"))
        self.client.get(reverse("resend_otp"))
        self.client.get(reverse("resend_otp"))

        self.assertEqual(
            PasswordResetOTP.objects.filter(user=self.user).count(),
            1,
        )

        self.assertEqual(mock_send_mail.call_count, 3)

    # -----------------------
    # RESET PASSWORD WITHOUT SESSION
    # -----------------------
    def test_reset_password_without_session(self):

        response = self.client.get(reverse("reset_password"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("forgot_password"))
