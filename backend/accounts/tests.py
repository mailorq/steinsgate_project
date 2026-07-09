from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from . import lockout, services
from .models import EmailVerificationCode

User = get_user_model()


def csrf_headers(client):
    client.get("/api/auth/csrf")
    return {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}


class RegistrationServiceTest(TestCase):

    def test_email_domain_validation(self):
        with self.assertRaises(services.RegistrationError):
            services.register_user(
                username='test', email='test@blocked.com', password='complex_pass_123'
            )

    def test_duplicate_email_rejected(self):
        User.objects.create_user(username='taken', email='taken@gmail.com', password='x')

        with self.assertRaises(services.RegistrationError):
            services.register_user(
                username='newuser', email='taken@gmail.com', password='complex_pass_123'
            )

    def test_duplicate_username_rejected(self):
        User.objects.create_user(username='taken', email='one@gmail.com', password='x')

        with self.assertRaises(services.RegistrationError):
            services.register_user(
                username='taken', email='two@gmail.com', password='complex_pass_123'
            )

    def test_weak_password_rejected(self):
        with self.assertRaises(services.RegistrationError):
            services.register_user(
                username='test', email='test@gmail.com', password='12345678'
            )


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


class LockoutTest(TestCase):

    def setUp(self):
        cache.clear()
        User.objects.create_user(username='okabe', password='correct_horse_1')

    def login(self, password):
        return self.client.post(
            '/api/auth/login',
            {'username': 'okabe', 'password': password},
            content_type='application/json',
        )

    def test_soft_block_after_five_failures(self):
        for _ in range(5):
            self.assertEqual(self.login('wrong').status_code, 400)

        blocked = self.login('wrong')
        self.assertEqual(blocked.status_code, 429)
        self.assertIn('Повторите через', blocked.json()['detail'])

        also_blocked_with_correct = self.login('correct_horse_1')
        self.assertEqual(also_blocked_with_correct.status_code, 429)

    def test_success_resets_counter(self):
        for _ in range(4):
            self.login('wrong')

        self.assertEqual(self.login('correct_horse_1').status_code, 200)

        for _ in range(5):
            self.assertEqual(self.login('wrong').status_code, 400)

    def test_hard_block_after_twenty_failures(self):
        for _ in range(lockout.HARD_LIMIT):
            lockout.register_failure('login', '1.2.3.4')

        with self.assertRaises(lockout.LockedOut) as caught:
            lockout.check_blocked('login', '1.2.3.4')

        self.assertGreater(caught.exception.retry_after, lockout.SOFT_BLOCK_SECONDS)

    def test_five_fresh_attempts_after_block_expires(self):
        for _ in range(5):
            lockout.register_failure('login', '5.6.7.8')

        with self.assertRaises(lockout.LockedOut):
            lockout.check_blocked('login', '5.6.7.8')

        cache.delete('lockout:login:5.6.7.8:block')

        for _ in range(4):
            lockout.register_failure('login', '5.6.7.8')
        lockout.check_blocked('login', '5.6.7.8')

        lockout.register_failure('login', '5.6.7.8')
        with self.assertRaises(lockout.LockedOut):
            lockout.check_blocked('login', '5.6.7.8')

    def test_verify_email_lockout(self):
        response = self.client.post(
            '/api/auth/register',
            {'username': 'kurisu', 'email': 'kurisu@gmail.com', 'password': 'complex_pass_123'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)

        for _ in range(5):
            wrong = self.client.post(
                '/api/auth/verify-email', {'code': '000000'}, content_type='application/json'
            )
            self.assertEqual(wrong.status_code, 400)

        blocked = self.client.post(
            '/api/auth/verify-email', {'code': '000000'}, content_type='application/json'
        )
        self.assertEqual(blocked.status_code, 429)


class AuthApiTest(TestCase):

    def setUp(self):
        cache.clear()

    REGISTER_PAYLOAD = {
        'username': 'kurisu',
        'email': 'kurisu@gmail.com',
        'password': 'complex_pass_123',
    }

    def register(self):
        return self.client.post(
            '/api/auth/register', self.REGISTER_PAYLOAD, content_type='application/json'
        )

    def test_register_creates_inactive_user_and_sends_email(self):
        response = self.register()

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='kurisu')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('verification', mail.outbox[0].subject.lower())

    def test_register_rejects_bad_domain(self):
        response = self.client.post(
            '/api/auth/register',
            {**self.REGISTER_PAYLOAD, 'email': 'kurisu@blocked.com'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='kurisu').exists())

    def test_full_registration_flow(self):
        self.register()
        user = User.objects.get(username='kurisu')

        wrong = self.client.post(
            '/api/auth/verify-email', {'code': '000000'}, content_type='application/json'
        )
        self.assertEqual(wrong.status_code, 400)

        response = self.client.post(
            '/api/auth/verify-email',
            {'code': user.verification_code.code},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['username'], 'kurisu')
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertEqual(user.profile.nickname, 'kurisu')

    def test_verify_without_pending_registration(self):
        response = self.client.post(
            '/api/auth/verify-email', {'code': '123456'}, content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_login_and_session(self):
        User.objects.create_user(username='daru', password='super_haker_123')

        anonymous = self.client.get('/api/auth/session')
        self.assertIsNone(anonymous.json()['user'])

        bad = self.client.post(
            '/api/auth/login',
            {'username': 'daru', 'password': 'wrong'},
            content_type='application/json',
        )
        self.assertEqual(bad.status_code, 400)

        response = self.client.post(
            '/api/auth/login',
            {'username': 'daru', 'password': 'super_haker_123'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['username'], 'daru')

        session = self.client.get('/api/auth/session')
        self.assertEqual(session.json()['user']['username'], 'daru')

    def test_logout(self):
        User.objects.create_user(username='daru', password='super_haker_123')
        self.client.login(username='daru', password='super_haker_123')

        response = self.client.post('/api/auth/logout', **csrf_headers(self.client))

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.client.get('/api/auth/session').json()['user'])


class ProfileApiTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.client.login(username='okabe', password='elpsykongroo')

    def test_update_nickname(self):
        response = self.client.patch(
            '/api/profile',
            {'nickname': 'Hououin Kyouma'},
            content_type='application/json',
            **csrf_headers(self.client),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nickname'], 'Hououin Kyouma')
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.nickname, 'Hououin Kyouma')

    def test_anonymous_cannot_update_profile(self):
        self.client.logout()

        response = self.client.patch(
            '/api/profile', {'nickname': 'x'}, content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
