import re

from django.http import HttpResponse
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


def index(request):
    """Single-page view: renders every section (home, about, courses,
    testimonials, gallery, lets-connect) into one template."""

    # --- Testimonials (DB) ---
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

    # --- Gallery (DB) grouped by category ---
    gallery_dict = {
        "certificates": [],
        "fashion_work": [],
        "aari_work": [],
        "events": [],
        "classes": [],
    }
    for item in GalleryItem.objects.all():
        if item.media_type == "video":
            item.embed_url = _youtube_embed(item.youtube_url)
        if item.category in gallery_dict:
            gallery_dict[item.category].append(item)

    # --- Combined SEO meta for the single homepage ---
    # The six former pages are now sections of one page, so their meta
    # descriptions and keywords are merged here for the homepage.
    meta = {
        "title": "Sris Snehidi Fashion Institute | Aari Embroidery & Fashion Designing Classes in Chennai",
        "description": (
            "Sris Snehidi Fashion Institute, Chennai — certified Aari embroidery and "
            "fashion designing courses (online & offline). MSME registered institute with "
            "25+ years of fashion expertise and 11+ years of teaching. 300+ women trained. "
            "Serving Madipakkam, Velachery, Pallikarani, Medavakkam and Nanganallur. "
            "Explore courses, student work, reviews and contact us to enroll."
        ),
        "keywords": (
            "aari embroidery classes Chennai, fashion designing course Chennai, "
            "online aari course India, tailoring class Chennai, blouse embroidery class, "
            "chudithar stitching, Madipakkam aari class, Velachery fashion institute, "
            "Pallikarani embroidery, Medavakkam tailoring, MSME registered fashion institute, "
            "embroidery certificate course, sris snehidi reviews, aari class enrollment Chennai"
        ),
        "url": "https://srissnehidi.com/",
        # Per-section descriptions, surfaced as extra section meta tags.
        "sections": [
            {"name": "about", "description": "Meet our expert trainer at Sris Snehidi Fashion Institute. 25+ years of fashion expertise, 11+ years of teaching. MSME registered institute offering certified fashion and Aari embroidery courses in Chennai."},
            {"name": "courses", "description": "Certified courses in Aari Embroidery and Fashion Designing at Sris Snehidi, Chennai. Online and offline classes. Basic and advanced Aari, blouse and chudithar stitching, fashion business training."},
            {"name": "testimonials", "description": "Read what our students say about Sris Snehidi Fashion Institute Chennai. 300+ women trained in Aari embroidery and fashion designing. Real reviews from students across Chennai and India."},
            {"name": "gallery", "description": "View student work, certificates, events and classes at Sris Snehidi Fashion Institute Chennai. See Aari embroidery and fashion designing work by our students."},
            {"name": "lets-connect", "description": "Contact Sris Snehidi Fashion Institute in Chennai. Call or WhatsApp to enroll in Aari embroidery or fashion designing courses. Located near Madipakkam, Velachery, Pallikarani, Medavakkam, Nanganallur."},
        ],
    }

    return render(request, "index.html", {
        "site": SITE,
        "trainer": TRAINER,
        "courses": COURSES,
        "video_testimonials": video_testimonials,
        "text_testimonials": text_testimonials,
        "gallery": gallery_dict,
        "meta": meta,
    })


def robots_txt(request):
    content = "User-agent: *\nAllow: /\nSitemap: https://srissnehidi.com/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")
