from django import forms

from .models import Restaurant


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
