import re

from django.shortcuts import render

from .constants import COURSES, SITE, TRAINER
from .models import GalleryItem, Testimonial


def _youtube_embed(url):
    if not url:
        return None
    m = re.search(r"youtu\.be/([^?&]+)", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    m = re.search(r"[?&]v=([^&]+)", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    if "youtube.com/embed/" in url:
        return url
    return None


def home(request):
    return render(request, "home.html", {"site": SITE})


def about(request):
    return render(request, "about.html", {"site": SITE, "trainer": TRAINER})


def courses(request):
    return render(request, "courses.html", {"site": SITE, "courses": COURSES})


def testimonials(request):
    video_testimonials = list(
        Testimonial.objects.filter(testimonial_type="video", is_active=True)
    )
    for t in video_testimonials:
        t.embed_url = _youtube_embed(t.youtube_url)

    text_testimonials = list(
        Testimonial.objects.filter(testimonial_type="text", is_active=True).order_by("order")
    )
    for t in text_testimonials:
        r = t.rating or 0
        t.star_string = "★" * r + "☆" * (5 - r)

    return render(
        request,
        "testimonials.html",
        {
            "site": SITE,
            "video_testimonials": video_testimonials,
            "text_testimonials": text_testimonials,
        },
    )


def gallery(request):
    items = list(GalleryItem.objects.all())
    for item in items:
        if item.media_type == "video":
            item.embed_url = _youtube_embed(item.youtube_url)

    gallery_dict = {
        "certificates": [],
        "fashion_work": [],
        "aari_work": [],
        "events": [],
        "classes": [],
    }
    for item in items:
        if item.category in gallery_dict:
            gallery_dict[item.category].append(item)

    return render(request, "gallery.html", {"site": SITE, "gallery": gallery_dict})


def lets_connect(request):
    return render(request, "lets_connect.html", {"site": SITE})
