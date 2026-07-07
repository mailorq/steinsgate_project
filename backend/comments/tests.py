from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.tests import csrf_headers
from catalog.models import AnimeDescription

from . import services
from .models import Comment

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


class CommentsApiTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='mayuri', password='tuturu_tuturu')
        self.anime = AnimeDescription.objects.get(slug='steins-gate')
        self.url = '/api/anime/steins-gate/comments'

    def login(self):
        self.client.login(username='mayuri', password='tuturu_tuturu')
        return csrf_headers(self.client)

    def test_anonymous_cannot_comment(self):
        response = self.client.post(
            self.url, {'text': 'Тест коммент'}, content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Comment.objects.count(), 0)

    def test_logged_in_user_can_comment(self):
        headers = self.login()

        response = self.client.post(
            self.url, {'text': 'Tuturu~!'}, content_type='application/json', **headers
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['text'], 'Tuturu~!')
        self.assertEqual(data['author']['username'], 'mayuri')
        self.assertEqual(Comment.objects.count(), 1)

    def test_spam_link_rejected(self):
        headers = self.login()

        response = self.client.post(
            self.url,
            {'text': 'заходите на spam.xyz срочно'},
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Comment.objects.count(), 0)

    def test_pagination(self):
        for i in range(7):
            Comment.objects.create(user=self.user, anime=self.anime, text=f'Комментарий {i}')

        first = self.client.get(self.url).json()
        second = self.client.get(f'{self.url}?page=2').json()

        self.assertEqual(len(first['items']), 6)
        self.assertEqual(first['total_pages'], 2)
        self.assertEqual(first['total'], 7)
        self.assertEqual(len(second['items']), 1)

    def test_reaction_flow(self):
        comment = Comment.objects.create(user=self.user, anime=self.anime, text='El Psy Kongroo')
        headers = self.login()

        response = self.client.post(
            f'/api/comments/{comment.id}/reaction',
            {'is_like': True},
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'likes': 1, 'dislikes': 0, 'rating': 1})

        listed = self.client.get(self.url).json()
        self.assertEqual(listed['items'][0]['my_reaction'], 'like')
