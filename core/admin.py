from django.contrib import admin
from .models import Testimonial, GalleryItem

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'testimonial_type', 'rating', 'is_active', 'order']
    list_filter = ['testimonial_type', 'is_active']
    search_fields = ['student_name', 'quote']

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'media_type', 'uploaded_at']
    list_filter = ['category', 'media_type']
    search_fields = ['title', 'caption']