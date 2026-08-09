from django.db import models


class Restaurant(models.Model):
    DAYPART_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    TYPE_CHOICES = [
        ('snacks', 'Snacks'),
        ('meal', 'Meal'),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    dayparts = models.CharField(max_length=40)  # comma-separated daypart keys
    restaurant_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.location}"

    def daypart_list(self):
        return [d for d in self.dayparts.split(',') if d]

    def daypart_labels(self):
        labels = dict(self.DAYPART_CHOICES)
        return [labels.get(d, d) for d in self.daypart_list()]


class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('good', 'Good'),
        ('ok', 'Ok'),
        ('bad', 'Bad'),
    ]

    restaurant = models.ForeignKey(Restaurant, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.restaurant.name}"
