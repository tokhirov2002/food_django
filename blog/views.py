from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost

def blog_list(request):
    """Blog postlari ro'yxati"""
    try:
        posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(posts, 6)  # Har sahifada 6 ta post
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Kategoriyalar
        categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
        
        # Eng mashhur postlar
        popular_posts = BlogPost.objects.filter(is_published=True).order_by('-views')[:5]
        
        context = {
            'page_obj': page_obj,
            'posts': page_obj,
            'categories': categories,
            'popular_posts': popular_posts,
        }
    except Exception as e:
        context = {
            'page_obj': None,
            'posts': [],
            'categories': [],
            'popular_posts': [],
            'error': str(e)
        }
    
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, post_id):
    """Blog post tafsilotlari"""
    try:
        post = get_object_or_404(BlogPost, id=post_id, is_published=True)
        
        # Ko'rishlar sonini oshirish
        post.views += 1
        post.save()
        
        # Tegishli postlar
        related_posts = BlogPost.objects.filter(
            category=post.category,
            is_published=True
        ).exclude(id=post_id)[:3]
        
        context = {
            'post': post,
            'related_posts': related_posts,
        }
    except Exception as e:
        context = {
            'post': None,
            'related_posts': [],
            'error': str(e)
        }
    
    return render(request, 'blog/blog_detail.html', context)

def blog_by_category(request, category):
    """Kategoriya bo'yicha blog postlari"""
    try:
        posts = BlogPost.objects.filter(
            category=category,
            is_published=True
        ).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'posts': page_obj,
            'page_obj': page_obj,
            'category': category,
        }
    except Exception as e:
        context = {
            'posts': [],
            'page_obj': None,
            'category': category,
            'error': str(e)
        }
    
    return render(request, 'blog/blog_list.html', context)