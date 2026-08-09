# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Django 5.2 website for **Sris Snehidi Fashion Institute** — a fashion training institute. The site displays courses, gallery, testimonials, and contact info. Media is hosted on Cloudinary; the database is PostgreSQL in production.

The project also hosts **`yum`**, an unrelated private food journal app for the site owner, mounted at an obscure path and not linked from anywhere public. See [Yum app](#yum-app) below.

## Development Commands

```bash
# Activate virtual environment (Windows)
venv/Scripts/activate

# Run dev server
python manage.py runserver          # http://127.0.0.1:8000

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser    # Create admin user

# Static files (production)
python manage.py collectstatic

# Sync gallery items from Cloudinary
python manage.py sync_cloudinary_gallery
```

There are no automated tests in this project.

## Environment Setup

Copy `.env.example` to `.env` and fill in:
- `SECRET_KEY` — Django secret key
- `DEBUG` — `True` for development
- `ALLOWED_HOSTS` — comma-separated hostnames
- `DATABASE_URL` — PostgreSQL connection string
- `CLOUDINARY_URL` — Cloudinary credentials

## Architecture

```
URL router (srissnehidi/urls.py)
  → core app views (core/views.py)       # 6 function-based views
      → core/constants.py                # Static site content (SITE, TRAINER, COURSES)
      → core/models.py                   # DB-backed content (Testimonial, GalleryItem)
  → templates/                           # Django HTML templates (all extend base.html)
  → static/css/main.css                  # Single stylesheet, ~1300 lines
```

**Pages and their routes:** `/` home, `/about/`, `/courses/`, `/testimonials/`, `/gallery/`, `/lets-connect/`

## Content Architecture

Site content comes from two sources:

1. **`core/constants.py`** — hardcoded content: institute name, tagline, trainer bio, course details (name, description, fee, schedule). Edit this file to change any copy that isn't managed via the admin.

2. **Django admin (`/admin/`)** — database-driven content:
   - `Testimonial` — video (YouTube URL) or text quotes with star rating and display order
   - `GalleryItem` — images (via Cloudinary) or YouTube videos, grouped into 5 categories: `certificates`, `fashion_work`, `aari_work`, `events`, `classes`

## Key Patterns

- **YouTube URLs**: The view helper `_youtube_embed()` in `core/views.py` converts share URLs to embed format. Pass a share URL; the template receives the embed URL.
- **Cloudinary images**: Use `CloudinaryField` on models; reference via `{{ item.image.url }}` in templates.
- **Static content vs. DB content**: If content needs admin editing, put it in a model. If it's structural/permanent, put it in `constants.py`.
- **Ordering**: Both `Testimonial` and `GalleryItem` have an `order` integer field; use it when querying to control display order.
- **Frontend**: No build step — plain HTML/CSS/vanilla JS. The single `main.css` uses a pink/magenta theme (`#C2185B`). Responsive breakpoints at 640px, 768px, 1024px.

## Yum App

`yum` is a separate Django app for the site owner's personal food/restaurant journal. It shares this project's deployment but is otherwise unrelated to the fashion institute content.

- **Mounted at `/yum-x7f2/`** (`srissnehidi/urls.py`), an unguessable path chosen so it isn't discoverable — not `/yum/`. Keep this path obscured; don't link to it from public pages or `sitemap.xml`. It's also disallowed in `robots.txt` (`core/views.py::robots_txt`).
- **Auth**: every view is wrapped in `yum.decorators.yum_required`, which requires an authenticated **superuser** and 404s (not 403/redirect) for anyone else. `LOGIN_URL = 'yum:login'` in settings.py points at `yum`'s own login view — there's no self-service signup, only superusers created via `createsuperuser`.
- **Models** (`yum/models.py`): `Restaurant` (name, location, `dayparts` — comma-separated morning/afternoon/evening, `restaurant_type` — snacks/meal) and `FoodItem` (belongs to a restaurant, categorized good/ok/bad).
- **Features**: browse/search restaurants and food items, add restaurants and items, and a "randomizer" that picks a random restaurant matching a daypart + type filter (`yum/views.py::randomizer`) — useful for "where should I eat" decisions.
- **Templates**: `yum/templates/yum/` — separate from the main site's `templates/` and doesn't extend `base.html`.
