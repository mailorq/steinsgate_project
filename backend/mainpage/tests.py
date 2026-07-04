from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import AnimeDescription, Comment

# Тесты, проверявшие рендер страниц и пагинацию через шаблоны, удалены вместе с HTML-слоем: UI переехал в frontend/. HTTP-слой будет покрыт тестами заново при переходе на django-ninja

User = get_user_model()


class AnimeModelTest(TestCase):

    def setUp(self):
        self.anime = AnimeDescription.objects.create(
            name="Steins;Gate",
            description="Аниме про путешествия во времени"
        )

    def test_anime_str_representation(self):
        self.assertEqual(str(self.anime), "Steins;Gate")

    def test_anime_has_no_comments_initially(self):
        self.assertEqual(self.anime.comments.count(), 0)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='okabe',
            email='okabe@lab.mem',
            password='elpsykongroo'
        )
        self.anime = AnimeDescription.objects.create(
            name="Steins;Gate 0"
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user,
            anime=self.anime,
            text="Лучшее аниме!"
        )

        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.anime, self.anime)
        self.assertIn("Лучшее", comment.text)

    def test_comment_belongs_to_anime(self):
        Comment.objects.create(
            user=self.user,
            anime=self.anime,
            text="test"
        )

        self.assertEqual(self.anime.comments.count(), 1)
        self.assertEqual(self.anime.comments.first().user, self.user)


class CommentFunctionalityTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='mayuri',
            password='tuturu'
        )
        self.anime = AnimeDescription.objects.create(name="Steins;Gate")
        self.url = reverse('steins_gate_page')

    def test_anonymous_user_cannot_comment(self):
        response = self.client.post(self.url, {
            'comment': 'Тест коммент'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_logged_in_user_can_comment(self):
        self.client.login(username='mayuri', password='tuturu')

        response = self.client.post(self.url, {
            'comment': 'Tuturu~!'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'Tuturu~!')
        self.assertEqual(comment.user, self.user)

    def test_empty_comment_not_saved(self):
        self.client.login(username='mayuri', password='tuturu')

        self.client.post(self.url, {'comment': '   '})

        self.assertEqual(Comment.objects.count(), 0)


class URLTest(TestCase):

    def test_steins_gate_url_resolves(self):
        url = reverse('steins_gate_page')
        self.assertEqual(url, '/steins-gate/')

    def test_steins_gate_zero_url_resolves(self):
        url = reverse('steins_gate_zero_page')
        self.assertEqual(url, '/steins-gate-zero/')

    def test_future_gadget_lab_url_resolves(self):
        url = reverse('future_gadget_laboratory')
        self.assertEqual(url, '/future-gadget-laboratory/')
