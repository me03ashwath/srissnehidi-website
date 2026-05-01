from django.db import models
from cloudinary.models import CloudinaryField

class Testimonial(models.Model):
    TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
    ]
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    student_name = models.CharField(max_length=100)
    testimonial_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    youtube_url = models.URLField(blank=True, null=True)
    quote = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student_name} ({self.testimonial_type})"

    class Meta:
        ordering = ['order']


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('certificates', 'Certificates Issued'),
        ('fashion_work', "Fashion Student's Work"),
        ('aari_work', "Aari Student's Work"),
        ('events', 'Events'),
        ('classes', 'Classes'),
    ]
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    image = CloudinaryField('image', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.category}"

    class Meta:
        ordering = ['order', '-uploaded_at']