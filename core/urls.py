from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # Single-page app: one route renders every section.
    path("", views.index, name="home"),

    # Legacy page URLs now redirect (301) to the matching section anchor,
    # preserving SEO link equity from the old multi-page structure.
    path("about/",        RedirectView.as_view(url="/#about",        permanent=True), name="about"),
    path("courses/",      RedirectView.as_view(url="/#courses",      permanent=True), name="courses"),
    path("testimonials/", RedirectView.as_view(url="/#testimonials", permanent=True), name="testimonials"),
    path("gallery/",      RedirectView.as_view(url="/#gallery",      permanent=True), name="gallery"),
    path("lets-connect/", RedirectView.as_view(url="/#lets-connect", permanent=True), name="lets_connect"),
]
