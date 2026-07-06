from django.urls import path
from django.views.generic import RedirectView

from .views import (
    future_gadget_laboratory_page,
    rate_anime,
    steins_gate_load_region_page,
    steins_gate_missing_link,
    steins_gate_page,
    steins_gate_zero_page,
)

urlpatterns = [
    path("future-gadget-laboratory/", future_gadget_laboratory_page, name="future_gadget_laboratory"),
    path("", RedirectView.as_view(pattern_name='steins_gate_page')),
    path("steins-gate/", steins_gate_page, name="steins_gate_page"),
    path("steins-gate-zero/", steins_gate_zero_page, name="steins_gate_zero_page"),
    path("steins-gate-load-region-of-deja-vu/", steins_gate_load_region_page, name="steins_gate_load_region"),
    path("steins-gate-kyoukaimenjou-no-missing-link/", steins_gate_missing_link, name="steins_gate_missing_link"),
    path("anime/<int:anime_id>/rate/", rate_anime, name="rate_anime"),
]
