from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'yum'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='yum/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='yum:login'), name='logout'),

    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('new/', views.create_restaurant, name='create_restaurant'),

    path('randomize/', views.randomizer, name='randomizer'),

    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:pk>/add-item/', views.add_food_item, name='add_food_item'),
    path('restaurant/<int:pk>/delete-item/<int:item_pk>/', views.delete_food_item, name='delete_food_item'),
    path('restaurant/<int:pk>/delete/', views.delete_restaurant_confirm, name='delete_restaurant_confirm'),
]
