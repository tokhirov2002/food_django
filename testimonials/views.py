from django.shortcuts import render
from .models import Testimonial

def testimonial_list(request):
    """Testimoniallar ro'yxati"""
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'testimonials/testimonial_list.html', context)