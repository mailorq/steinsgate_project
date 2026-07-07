from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.tests import csrf_headers

from . import services
from .models import AnimeDescription, ViewHistory

User = get_user_model()


class SeedDataTest(TestCase):

    def test_all_titles_seeded(self):
        slugs = set(AnimeDescription.objects.values_list('slug', flat=True))

        self.assertEqual(slugs, {
            'steins-gate',
            'steins-gate-zero',
            'steins-gate-load-region-of-deja-vu',
            'steins-gate-kyoukaimenjou-no-missing-link',
        })

    def test_seeded_title_fields(self):
        anime = AnimeDescription.objects.get(slug='steins-gate')

        self.assertEqual(anime.name, 'Steins;Gate')
        self.assertEqual(anime.appearing, '2011 весна')
        self.assertTrue(anime.description)


class AnimeModelTest(TestCase):

    def setUp(self):
        self.anime = AnimeDescription.objects.get(slug='steins-gate')

    def test_anime_str_representation(self):
        self.assertEqual(str(self.anime), 'Steins;Gate')

    def test_anime_has_no_comments_initially(self):
        self.assertEqual(self.anime.comments.count(), 0)


class CatalogServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='okabe', password='elpsykongroo')
        self.anime = AnimeDescription.objects.get(slug='steins-gate')

    def test_view_event_deduplicated_for_user(self):
        services.register_view_event(anime=self.anime, user=self.user, ip_address='1.1.1.1')
        services.register_view_event(anime=self.anime, user=self.user, ip_address='1.1.1.1')

        self.assertEqual(ViewHistory.objects.count(), 1)

    def test_view_event_deduplicated_for_anonymous_by_ip(self):
        services.register_view_event(anime=self.anime, user=None, ip_address='2.2.2.2')
        services.register_view_event(anime=self.anime, user=None, ip_address='2.2.2.2')
        services.register_view_event(anime=self.anime, user=None, ip_address='3.3.3.3')

        self.assertEqual(ViewHistory.objects.count(), 2)

    def test_rate_anime_updates_existing_rating(self):
        services.rate_anime(user=self.user, anime=self.anime, rating=3)
        avg = services.rate_anime(user=self.user, anime=self.anime, rating=5)

        self.assertEqual(self.anime.ratings.count(), 1)
        self.assertEqual(avg, 5.0)

    def test_rate_anime_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            services.rate_anime(user=self.user, anime=self.anime, rating=6)


class CatalogApiTest(TestCase):

    def test_anime_list(self):
        response = self.client.get('/api/anime')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        self.assertIn('steins-gate', [item['slug'] for item in response.json()])

    def test_anime_detail_registers_deduplicated_view(self):
        response = self.client.get('/api/anime/steins-gate')
        self.client.get('/api/anime/steins-gate')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Steins;Gate')
        self.assertEqual(data['season'], '2011 весна')
        self.assertIsNone(data['avg_rating'])
        self.assertEqual(ViewHistory.objects.count(), 1)

    def test_unknown_slug_returns_404(self):
        response = self.client.get('/api/anime/unknown')

        self.assertEqual(response.status_code, 404)

    def test_rating_requires_auth(self):
        response = self.client.post(
            '/api/anime/steins-gate/rating', {'rating': 5}, content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_rating_flow(self):
        User.objects.create_user(username='okabe', password='elpsykongroo')
        self.client.login(username='okabe', password='elpsykongroo')

        response = self.client.post(
            '/api/anime/steins-gate/rating',
            {'rating': 5},
            content_type='application/json',
            **csrf_headers(self.client),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'avg_rating': 5.0, 'user_rating': 5})

    def test_rating_out_of_range_rejected(self):
        User.objects.create_user(username='okabe', password='elpsykongroo')
        self.client.login(username='okabe', password='elpsykongroo')

        response = self.client.post(
            '/api/anime/steins-gate/rating',
            {'rating': 6},
            content_type='application/json',
            **csrf_headers(self.client),
        )

        self.assertEqual(response.status_code, 422)
