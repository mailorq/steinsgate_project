from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from . import services
from .forms import RegisterForm
from .models import EmailVerificationCode

User = get_user_model()


class RegisterFormTest(TestCase):

    def test_email_domain_validation(self):
        form = RegisterForm(data={
            'username': 'test',
            'email': 'test@blocked.com',
            'password': 'pass_123',
            'confirm_password': 'pass_123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'complex_pass_123',
            'confirm_password': 'different_pass_123',
        })

        self.assertFalse(form.is_valid())

    def test_duplicate_email_rejected(self):
        User.objects.create_user(username='taken', email='taken@gmail.com', password='x')

        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'taken@gmail.com',
            'password': 'complex_pass_123',
            'confirm_password': 'complex_pass_123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class VerificationServiceTest(TestCase):

    def setUp(self):
        self.user = services.register_user(
            username='kurisu',
            email='kurisu@gmail.com',
            password='complex_pass_123',
        )

    def test_registered_user_is_inactive_with_code(self):
        self.assertFalse(self.user.is_active)
        self.assertEqual(len(self.user.verification_code.code), 6)

    def test_correct_code_activates_user(self):
        services.verify_email(user=self.user, code=self.user.verification_code.code)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertFalse(EmailVerificationCode.objects.filter(user=self.user).exists())

    def test_wrong_code_raises_and_keeps_user_inactive(self):
        with self.assertRaises(services.VerificationError):
            services.verify_email(user=self.user, code='000000')

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_attempts_are_limited(self):
        for _ in range(EmailVerificationCode.MAX_ATTEMPTS):
            with self.assertRaises(services.VerificationError):
                services.verify_email(user=self.user, code='000000')

        with self.assertRaises(services.VerificationError):
            services.verify_email(user=self.user, code=self.user.verification_code.code)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_expired_code_rejected(self):
        record = self.user.verification_code
        record.created_at = timezone.now() - EmailVerificationCode.TTL - timedelta(minutes=1)
        record.save(update_fields=['created_at'])

        with self.assertRaises(services.VerificationError):
            services.verify_email(user=self.user, code=record.code)

    def test_inactive_user_cannot_login(self):
        logged_in = self.client.login(username='kurisu', password='complex_pass_123')

        self.assertFalse(logged_in)


class AuthenticationTest(TestCase):

    def test_user_can_register_with_email_verification(self):
        response = self.client.post(reverse('register'), {
            'username': 'kurisu',
            'email': 'kurisu@gmail.com',
            'password': 'complex_pass_123',
            'confirm_password': 'complex_pass_123'
        })

        self.assertRedirects(
            response, reverse('email_verification'), fetch_redirect_response=False
        )

        user = User.objects.get(username='kurisu')
        self.assertFalse(user.is_active)

        code = user.verification_code.code
        self.client.post(reverse('email_verification'), {'code': code})

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.nickname, 'kurisu')

    def test_register_sends_email(self):
        self.client.post(reverse('register'), {
            'username': 'daru',
            'email': 'daru@gmail.com',
            'password': 'super_haker_123',
            'confirm_password': 'super_haker_123'
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('verification', mail.outbox[0].subject.lower())
        self.assertEqual(mail.outbox[0].to, ['daru@gmail.com'])

    def test_user_can_login(self):
        User.objects.create_user(username='daru', password='super_haker')

        logged_in = self.client.login(username='daru', password='super_haker')

        self.assertTrue(logged_in)
