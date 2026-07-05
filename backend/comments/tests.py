from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import AnimeDescription

from .models import Comment
from . import services

User = get_user_model()


class CommentServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.anime = AnimeDescription.objects.get(slug='steins-gate')

    def test_link_is_rejected(self):
        with self.assertRaises(services.CommentRejected):
            services.create_comment(
                user=self.user, anime=self.anime, text='смотрите https://spam.example'
            )

        self.assertEqual(Comment.objects.count(), 0)

    def test_short_text_is_rejected(self):
        with self.assertRaises(services.CommentRejected):
            services.create_comment(user=self.user, anime=self.anime, text='ok')

    def test_html_is_stripped(self):
        comment = services.create_comment(
            user=self.user, anime=self.anime, text='<b>Tuturu</b>, Okabe!'
        )

        self.assertEqual(comment.text, 'Tuturu, Okabe!')

    def test_toggle_reaction_switches_and_removes(self):
        comment = services.create_comment(
            user=self.user, anime=self.anime, text='El Psy Kongroo'
        )
        other = User.objects.create_user(username='daru', password='super_haker')

        result = services.toggle_reaction(user=other, comment=comment, is_like=True)
        self.assertEqual((result['likes'], result['dislikes']), (1, 0))

        result = services.toggle_reaction(user=other, comment=comment, is_like=False)
        self.assertEqual((result['likes'], result['dislikes']), (0, 1))

        result = services.toggle_reaction(user=other, comment=comment, is_like=False)
        self.assertEqual((result['likes'], result['dislikes']), (0, 0))


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='okabe',
            email='okabe@lab.mem',
            password='elpsykongroo'
        )
        self.anime = AnimeDescription.objects.get(slug='steins-gate-zero')

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
        self.anime = AnimeDescription.objects.get(slug='steins-gate')
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
