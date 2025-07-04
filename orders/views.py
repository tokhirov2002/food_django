from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from menu.models import Food
import json

def cart(request):
    """Savatcha sahifasi"""
    try:
        cart = request.session.get('cart', {})
        items = []
        subtotal = 0
        
        for food_id, item_data in cart.items():
            try:
                food = Food.objects.get(id=food_id)
                item_total = item_data['price'] * item_data['quantity']
                items.append({
                    'id': food_id,
                    'food': food,
                    'quantity': item_data['quantity'],
                    'price': item_data['price'],
                    'total': item_total
                })
                subtotal += item_total
            except Food.DoesNotExist:
                continue
        
        tax = subtotal * 0.08  # 8% soliq
        total = subtotal + tax + 5.00  # +5$ delivery
        
        context = {
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
        }
    except Exception as e:
        context = {
            'items': [],
            'subtotal': 0,
            'tax': 0,
            'total': 5.00,
            'error': str(e)
        }
    
    return render(request, 'orders/cart.html', context)

def checkout(request):
    """To'lov sahifasi"""
    try:
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.warning(request, 'Savatchangiz bo\'sh!')
            return redirect('orders:cart')
        
        if request.method == 'POST':
            # Bu yerda buyurtma yaratish logic yoziladi
            # Hozircha faqat session ni tozalaymiz
            request.session['cart'] = {}
            messages.success(request, 'Buyurtmangiz muvaffaqiyatli qabul qilindi!')
            return redirect('orders:order_success')
        
        # Cart ma'lumotlarini hisoblash
        items = []
        subtotal = 0
        
        for food_id, item_data in cart.items():
            try:
                food = Food.objects.get(id=food_id)
                item_total = item_data['price'] * item_data['quantity']
                items.append({
                    'food': food,
                    'quantity': item_data['quantity'],
                    'total': item_total
                })
                subtotal += item_total
            except Food.DoesNotExist:
                continue
        
        tax = subtotal * 0.08
        total = subtotal + tax + 5.00
        
        context = {
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
        }
    except Exception as e:
        context = {
            'items': [],
            'subtotal': 0,
            'tax': 0,
            'total': 5.00,
            'error': str(e)
        }
    
    return render(request, 'orders/checkout.html', context)

@csrf_exempt
@require_POST
def update_cart(request, item_id):
    """Savatcha miqdorini yangilash"""
    try:
        cart = request.session.get('cart', {})
        
        if str(item_id) in cart:
            data = json.loads(request.body)
            change = data.get('change', 0)
            
            cart[str(item_id)]['quantity'] += change
            
            if cart[str(item_id)]['quantity'] <= 0:
                del cart[str(item_id)]
            
            request.session['cart'] = cart
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def remove_from_cart(request, item_id):
    """Savatchadan olib tashlash"""
    try:
        cart = request.session.get('cart', {})
        
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def order_success(request):
    """Buyurtma muvaffaqiyatli sahifasi"""
    return render(request, 'orders/order_success.html')