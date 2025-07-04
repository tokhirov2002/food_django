from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('category/<int:category_id>/', views.food_by_category, name='food_by_category'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
]