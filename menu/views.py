from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Food

def food_list(request):
    """Barcha ovqatlar ro'yxati"""
    try:
        categories = Category.objects.all()
        selected_category = request.GET.get('category')
        
        if selected_category:
            foods = Food.objects.filter(
                category_id=selected_category, 
                is_available=True
            )
            try:
                active_category = Category.objects.get(id=selected_category)
            except Category.DoesNotExist:
                active_category = None
        else:
            foods = Food.objects.filter(is_available=True)
            active_category = None
        
        context = {
            'categories': categories,
            'foods': foods,
            'active_category': active_category,
        }
    except Exception as e:
        context = {
            'categories': [],
            'foods': [],
            'active_category': None,
            'error': str(e)
        }
    
    return render(request, 'menu/food_list.html', context)

def food_by_category(request, category_id):
    """Kategoriya bo'yicha ovqatlar"""
    try:
        category = get_object_or_404(Category, id=category_id)
        foods = Food.objects.filter(category=category, is_available=True)
        categories = Category.objects.all()
        
        context = {
            'category': category,
            'foods': foods,
            'categories': categories,
            'active_category': category,
        }
    except Exception as e:
        context = {
            'categories': [],
            'foods': [],
            'active_category': None,
            'error': str(e)
        }
    
    return render(request, 'menu/food_list.html', context)

def food_detail(request, food_id):
    """Ovqat tafsilotlari"""
    try:
        food = get_object_or_404(Food, id=food_id, is_available=True)
        related_foods = Food.objects.filter(
            category=food.category, 
            is_available=True
        ).exclude(id=food_id)[:4]
        
        context = {
            'food': food,
            'related_foods': related_foods,
        }
    except Exception as e:
        context = {
            'food': None,
            'related_foods': [],
            'error': str(e)
        }
    
    return render(request, 'menu/food_detail.html', context)

def add_to_cart(request, food_id):
    """Savatchaga qo'shish"""
    if request.method == 'POST':
        try:
            food = get_object_or_404(Food, id=food_id)
            quantity = int(request.POST.get('quantity', 1))
            
            # Session orqali cart boshqarish
            cart = request.session.get('cart', {})
            
            if str(food_id) in cart:
                cart[str(food_id)]['quantity'] += quantity
            else:
                cart[str(food_id)] = {
                    'name': food.name,
                    'price': float(food.price),
                    'quantity': quantity,
                    'image': food.image.url if food.image else ''
                }
            
            request.session['cart'] = cart
            messages.success(request, f'{food.name} savatchaga qo\'shildi!')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Savatchaga qo\'shildi!'})
            
            return redirect('menu:food_detail', food_id=food_id)
        except Exception as e:
            messages.error(request, 'Xatolik yuz berdi!')
            return redirect('menu:food_list')
    
    return redirect('menu:food_list')