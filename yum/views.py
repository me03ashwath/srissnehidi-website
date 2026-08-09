import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

DAYPART_ORDER = ['morning', 'afternoon', 'evening']


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

from .decorators import yum_required
from .forms import RestaurantForm
from .models import FoodItem, Restaurant


def _panels(restaurant):
    items = restaurant.items.all()
    return [
        {'key': 'good', 'label': 'Good', 'items': items.filter(category='good')},
        {'key': 'ok', 'label': 'Ok', 'items': items.filter(category='ok')},
        {'key': 'bad', 'label': 'Bad', 'items': items.filter(category='bad')},
    ]


@yum_required
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'yum/home.html', {'restaurants': restaurants})


@yum_required
def search(request):
    mode = request.GET.get('mode', 'restaurant')
    if mode not in ('restaurant', 'food'):
        mode = 'restaurant'
    query = request.GET.get('q', '').strip()

    restaurants = []
    if query:
        if mode == 'restaurant':
            restaurants = Restaurant.objects.filter(name__icontains=query)
        else:
            restaurants = Restaurant.objects.filter(items__name__icontains=query).distinct()

    context = {'mode': mode, 'query': query, 'restaurants': restaurants}
    if _is_ajax(request):
        return render(request, 'yum/_search_results.html', context)
    return render(request, 'yum/search.html', context)


@yum_required
def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save()
            return redirect('yum:restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm()
    return render(request, 'yum/create_restaurant.html', {'form': form})


@yum_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'yum/restaurant_detail.html', {
        'restaurant': restaurant,
        'panels': _panels(restaurant),
    })


@yum_required
@require_POST
def add_food_item(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    category = request.POST.get('category')
    name = request.POST.get('name', '').strip()

    item = None
    if name and category in dict(FoodItem.CATEGORY_CHOICES):
        next_order = restaurant.items.filter(category=category).count()
        item = FoodItem.objects.create(restaurant=restaurant, name=name, category=category, order=next_order)

    if _is_ajax(request):
        if item:
            return JsonResponse({'id': item.id, 'name': item.name, 'category': item.category})
        return JsonResponse({'error': 'invalid'}, status=400)

    return redirect('yum:restaurant_detail', pk=restaurant.pk)


@yum_required
@require_POST
def delete_food_item(request, pk, item_pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    item = get_object_or_404(FoodItem, pk=item_pk, restaurant=restaurant)
    item.delete()
    return redirect('yum:restaurant_detail', pk=restaurant.pk)


@yum_required
def delete_restaurant_confirm(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('yum:home')
    return render(request, 'yum/delete_restaurant_confirm.html', {'restaurant': restaurant})


@yum_required
def randomizer(request):
    result = None
    no_match = False
    daypart = 'afternoon'
    restaurant_type = 'snacks'

    if request.method == 'POST':
        daypart = request.POST.get('daypart', daypart)
        restaurant_type = request.POST.get('restaurant_type', restaurant_type)
        candidates = [
            r for r in Restaurant.objects.filter(restaurant_type=restaurant_type)
            if daypart in r.daypart_list()
        ]
        if candidates:
            result = random.choice(candidates)
        else:
            no_match = True

    daypart_index = DAYPART_ORDER.index(daypart) if daypart in DAYPART_ORDER else 1

    return render(request, 'yum/randomizer.html', {
        'daypart': daypart,
        'daypart_index': daypart_index,
        'restaurant_type': restaurant_type,
        'result': result,
        'no_match': no_match,
    })
