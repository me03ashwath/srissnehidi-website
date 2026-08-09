from django.contrib import admin

from .models import FoodItem, Restaurant


class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'restaurant_type', 'dayparts', 'order']
    list_filter = ['restaurant_type']
    search_fields = ['name', 'location']
    inlines = [FoodItemInline]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'order']
    list_filter = ['category']
    search_fields = ['name']
