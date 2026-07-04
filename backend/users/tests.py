from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .forms import RegisterForm

# Тесты, требовавшие рендера HTML-шаблонов (неверный код верификации, отображение ошибок формы), удалены вместе с HTML-слоем и вернутся при переходе на django-ninja

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
        self.assertFalse(User.objects.filter(username='kurisu').exists())
        self.assertIn('verification_code', self.client.session)
        self.assertIn('registration_data', self.client.session)

        code = self.client.session['verification_code']
        self.client.post(reverse('email_verification'), {'code': str(code)})

        self.assertTrue(User.objects.filter(username='kurisu').exists())

        user = User.objects.get(username='kurisu')
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
