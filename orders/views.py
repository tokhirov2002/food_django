from django.shortcuts import redirect, get_object_or_404, render
from menu.models import Food
from .models import Order, OrderItem

def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    # Ochiq Order topamiz yoki yaratamiz
    order, created = Order.objects.get_or_create(is_paid=False)

    # OrderItem qo‘shamiz yoki yangilaymiz
    item, created = OrderItem.objects.get_or_create(order=order, food=food)
    if not created:
        item.quantity += 1
        item.save()

    return redirect('view_cart')

def view_cart(request):
    order = Order.objects.filter(is_paid=False).first()
    items = order.orderitem_set.all() if order else []
    return render(request, 'orders/cart.html', {'items': items})
