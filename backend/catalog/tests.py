from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import AnimeDescription, ViewHistory
from . import services

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
