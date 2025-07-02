from django.shortcuts import render, get_object_or_404
from .models import Food, Category

def food_list(request):
    foods = Food.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu/food_list.html', {
        'foods': foods,
        'categories': categories,
    })

def food_detail(request, slug):
    food = get_object_or_404(Food, slug=slug)
    return render(request, 'menu/food_detail.html', {
        'food': food,
    })
