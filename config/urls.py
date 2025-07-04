from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book-table/', views.book_table, name='book_table'),
    path('menu/', include('menu.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('orders/', include('orders.urls')),
]

# Static va media fayllar uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 404 sahifa uchun
handler404 = 'config.views.custom_404'