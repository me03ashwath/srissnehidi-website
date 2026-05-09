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


def home(request):
    return render(request, "home.html", {
        "site": SITE,
        "meta": {
            "title": "Sris Snehidi Fashion Institute | Aari Embroidery & Fashion Designing Classes in Chennai",
            "description": "Learn Aari embroidery and fashion designing at Sris Snehidi Fashion Institute, Chennai. Certified courses in Madipakkam, Velachery, Pallikarani area. Online Aari classes available across India.",
            "keywords": "aari embroidery classes Chennai, fashion designing course Chennai, online aari course India, tailoring class Chennai, blouse embroidery class, chudithar stitching, Madipakkam aari class, Velachery fashion institute, Pallikarani embroidery, Medavakkam tailoring",
            "url": "https://srissnehidi.com/",
        },
    })


def about(request):
    return render(request, "about.html", {
        "site": SITE,
        "trainer": TRAINER,
        "meta": {
            "title": "About Us | Sris Snehidi Fashion Institute Chennai",
            "description": "Meet our expert trainer at Sris Snehidi Fashion Institute. 25+ years of fashion expertise, 11+ years of teaching. MSME registered institute offering certified fashion and Aari embroidery courses in Chennai.",
            "keywords": "fashion institute Chennai, aari embroidery trainer Chennai, fashion designing teacher Chennai, MSME registered fashion institute",
            "url": "https://srissnehidi.com/about/",
        },
    })


def courses(request):
    return render(request, "courses.html", {
        "site": SITE,
        "courses": COURSES,
        "meta": {
            "title": "Courses | Aari Embroidery & Fashion Designing Classes | Sris Snehidi Chennai",
            "description": "Certified courses in Aari Embroidery and Fashion Designing at Sris Snehidi, Chennai. Online and offline classes. Basic and advanced Aari, blouse and chudithar stitching, fashion business training.",
            "keywords": "aari embroidery course Chennai, fashion designing course Chennai, online aari embroidery class, blouse stitching class, chudithar stitching Chennai, embroidery certificate course, fashion designing certificate Chennai",
            "url": "https://srissnehidi.com/courses/",
        },
    })


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
            "meta": {
                "title": "Student Reviews | Sris Snehidi Fashion Institute Chennai",
                "description": "Read what our students say about Sris Snehidi Fashion Institute Chennai. 300+ women trained in Aari embroidery and fashion designing. Real reviews from students across Chennai and India.",
                "keywords": "sris snehidi reviews, fashion institute Chennai reviews, aari embroidery class reviews Chennai",
                "url": "https://srissnehidi.com/testimonials/",
            },
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

    return render(request, "gallery.html", {
        "site": SITE,
        "gallery": gallery_dict,
        "meta": {
            "title": "Gallery | Student Work & Events | Sris Snehidi Fashion Institute",
            "description": "View student work, certificates, events and classes at Sris Snehidi Fashion Institute Chennai. See Aari embroidery and fashion designing work by our students.",
            "keywords": "aari embroidery student work Chennai, fashion designing student work, embroidery certificate Chennai",
            "url": "https://srissnehidi.com/gallery/",
        },
    })


def lets_connect(request):
    return render(request, "lets_connect.html", {
        "site": SITE,
        "meta": {
            "title": "Contact Us | Sris Snehidi Fashion Institute Chennai",
            "description": "Contact Sris Snehidi Fashion Institute in Chennai. Call or WhatsApp to enroll in Aari embroidery or fashion designing courses. Located near Madipakkam, Velachery, Pallikarani, Medavakkam, Nanganallur.",
            "keywords": "sris snehidi contact, fashion institute Chennai contact, aari class enrollment Chennai, fashion course admission Chennai",
            "url": "https://srissnehidi.com/lets-connect/",
        },
    })


def robots_txt(request):
    content = "User-agent: *\nAllow: /\nSitemap: https://srissnehidi.com/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")
