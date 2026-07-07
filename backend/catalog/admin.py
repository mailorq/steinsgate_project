from django.contrib import admin

from .models import AnimeDescription, AnimeRating, ViewHistory

admin.site.register(AnimeDescription)
admin.site.register(AnimeRating)
admin.site.register(ViewHistory)
