from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("courses/", views.courses, name="courses"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("gallery/", views.gallery, name="gallery"),
    path("lets-connect/", views.lets_connect, name="lets_connect"),
]
