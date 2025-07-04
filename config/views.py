from django.shortcuts import render
from django.http import Http404
from menu.models import Category, Food
from blog.models import BlogPost
from testimonials.models import Testimonial

def home(request):
    """Bosh sahifa"""
    try:
        categories = Category.objects.all()[:4]  # Faqat 4 ta kategoriya
    except:
        categories = []
    
    try:
        latest_foods = Food.objects.filter(is_available=True)[:6]  # Eng yangi ovqatlar
    except:
        latest_foods = []
    
    try:
        testimonials = Testimonial.objects.filter(is_active=True)[:3]  # 3 ta testimonial
    except:
        testimonials = []
    
    context = {
        'categories': categories,
        'latest_foods': latest_foods,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    """Biz haqimizda sahifasi"""
    try:
        testimonials = Testimonial.objects.filter(is_active=True)[:3]
    except:
        testimonials = []
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def book_table(request):
    """Stol bron qilish sahifasi"""
    if request.method == 'POST':
        # Bu yerda booking logic yoziladi
        # Hozircha faqat sahifani ko'rsatamiz
        pass
    
    return render(request, 'book_table.html')

def custom_404(request, exception):
    """404 xato sahifasi"""
    return render(request, '404.html', status=404)