from django import forms

from .models import FoodItem, Restaurant


class RestaurantForm(forms.ModelForm):
    dayparts = forms.MultipleChoiceField(
        choices=Restaurant.DAYPART_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    restaurant_type = forms.ChoiceField(
        choices=Restaurant.TYPE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'dayparts', 'restaurant_type']

    def clean_dayparts(self):
        return ','.join(self.cleaned_data['dayparts'])


class RestaurantDetailsForm(forms.ModelForm):
    dayparts = forms.MultipleChoiceField(
        choices=Restaurant.DAYPART_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    restaurant_type = forms.ChoiceField(
        choices=Restaurant.TYPE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'dayparts', 'restaurant_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.is_bound:
            self.initial['dayparts'] = self.instance.daypart_list()

    def clean_dayparts(self):
        return ','.join(self.cleaned_data['dayparts'])


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category']
