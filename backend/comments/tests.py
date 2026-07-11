from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from accounts.tests import csrf_headers
from catalog.models import AnimeDescription

from . import moderation, services
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


class ModerationTest(TestCase):

    REJECTED = [
        '!!!!!!!!!!!!!!!!!',
        'тоооооп',
        'аааааааааа',
        'лоллоллоллоллол',
        'ну ты и дебил',
        'что за хуйня',
        'fuck this show',
        'f*ck you',
        '😭' * 13,
        ')))))))))))',
    ]
    ACCEPTED = [
        'Лучшее аниме в моей жизни!',
        'Топ, ждали!!',
        'ааа, ну такое себе',
        'блин, вот это поворот',
        'damn, what an episode',
        'лол, ну и концовка',
        'Okabe = Hououin Kyouma!!',
        '😭' * 10,
        'El Psy Kongroo',
    ]

    def test_rejected_samples(self):
        for text in self.REJECTED:
            self.assertIsNotNone(moderation.check_comment(text), text)

    def test_accepted_samples(self):
        for text in self.ACCEPTED:
            self.assertIsNone(moderation.check_comment(text), text)


class CommentLimitsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.anime = AnimeDescription.objects.get(slug='steins-gate')

    def test_comment_over_limit_rejected(self):
        with self.assertRaises(services.CommentRejected):
            services.create_comment(user=self.user, anime=self.anime, text='ня ' * 400)

    def test_spoiler_markers_do_not_count_against_limit(self):
        text = '||' + 'спойлер тут ' * 70 + '||'
        comment = services.create_comment(user=self.user, anime=self.anime, text=text)

        self.assertIn('||', comment.text)

    def test_profane_text_inside_spoiler_rejected(self):
        with self.assertRaises(services.CommentRejected):
            services.create_comment(user=self.user, anime=self.anime, text='||что за хуйня||')


class CommentDeleteTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.other = User.objects.create_user(username='daru', password='super_haker_1')
        self.admin = User.objects.create_user(
            username='admin', password='admin_pass_123', is_staff=True
        )
        self.anime = AnimeDescription.objects.get(slug='steins-gate')
        self.comment = Comment.objects.create(
            user=self.author, anime=self.anime, text='El Psy Kongroo'
        )

    def delete(self):
        return self.client.delete(
            f'/api/comments/{self.comment.id}', **csrf_headers(self.client)
        )

    def test_author_can_delete_own_comment(self):
        self.client.login(username='okabe', password='elpsykongroo')

        response = self.delete()

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='daru', password='super_haker_1')

        response = self.delete()

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_staff_can_delete_any_comment(self):
        self.client.login(username='admin', password='admin_pass_123')

        response = self.delete()

        self.assertEqual(response.status_code, 204)

    def test_anonymous_gets_401(self):
        response = self.client.delete(f'/api/comments/{self.comment.id}')

        self.assertEqual(response.status_code, 401)

    def test_can_delete_flag_in_listing(self):
        listing_url = '/api/anime/steins-gate/comments'

        self.client.login(username='okabe', password='elpsykongroo')
        self.assertTrue(self.client.get(listing_url).json()['items'][0]['can_delete'])

        self.client.login(username='daru', password='super_haker_1')
        self.assertFalse(self.client.get(listing_url).json()['items'][0]['can_delete'])

        self.client.login(username='admin', password='admin_pass_123')
        self.assertTrue(self.client.get(listing_url).json()['items'][0]['can_delete'])


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


class CommentsQueryCountTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.anime = AnimeDescription.objects.get(slug='steins-gate')

    def add_comments(self, count):
        for i in range(count):
            Comment.objects.create(user=self.author, anime=self.anime, text=f'Комментарий {i}')

    def query_count(self):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/anime/steins-gate/comments')
        self.assertEqual(response.status_code, 200)
        return len(context)

    def test_anonymous_list_has_constant_query_count(self):
        self.add_comments(2)
        small = self.query_count()

        self.add_comments(10)
        large = self.query_count()

        self.assertEqual(small, large)

    def test_authenticated_list_has_constant_query_count(self):
        self.client.login(username='okabe', password='elpsykongroo')
        self.add_comments(2)
        small = self.query_count()

        self.add_comments(10)
        large = self.query_count()

        self.assertEqual(small, large)


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

    def test_newest_comment_comes_first(self):
        for i in range(3):
            Comment.objects.create(user=self.user, anime=self.anime, text=f'Комментарий {i}')

        items = self.client.get(self.url).json()['items']

        self.assertEqual(
            [item['text'] for item in items],
            ['Комментарий 2', 'Комментарий 1', 'Комментарий 0'],
        )

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
