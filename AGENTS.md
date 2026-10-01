# AGENTS.md

## Project

- Django 5.2 website for Sris Snehidi Fashion Institute.
- The public site uses Django templates, plain HTML/CSS, and vanilla JavaScript; there is no frontend build step.
- Production uses PostgreSQL and Cloudinary for media.

## Development

```powershell
venv/Scripts/activate
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py sync_cloudinary_gallery
```

- This repository has no automated test suite. For changes, run the most relevant Django checks or manual verification when feasible.
- Configure local secrets in `.env` from `.env.example`; do not commit credentials.

## Architecture and content

- Public routes are defined in `srissnehidi/urls.py`; the main views are function-based in `core/views.py`.
- Templates extend `base.html`. Site styling lives in `static/css/main.css`; preserve the existing pink/magenta visual system and responsive breakpoints (640px, 768px, 1024px) unless a task calls for a redesign.
- Structural/permanent public copy belongs in `core/constants.py`. Admin-editable testimonials and gallery content belong in the corresponding Django models.
- Preserve explicit `order` fields when querying `Testimonial` and `GalleryItem`.
- Use `CloudinaryField` for gallery images and `{{ item.image.url }}` in templates. Keep YouTube URL handling through `_youtube_embed()` in `core/views.py`.

## Yum app privacy

`yum` is a private, unrelated food journal. Treat its isolation as a security and privacy requirement:

- Keep it mounted only at `/yum-x7f2/`; do not expose, link, or mention it on public pages or in `sitemap.xml`.
- Keep the path disallowed by `robots.txt`.
- Preserve `yum_required` protection: access requires an authenticated superuser and unauthorized requests return 404 rather than a redirect or 403.
- Do not add self-service signup or weaken its separate authentication flow.
