from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    """Aloqa sahifasi"""
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Email yuborish (ixtiyoriy)
            try:
                full_message = f"""
                Ism: {first_name} {last_name}
                Email: {email}
                Telefon: {phone}
                
                Xabar: {message}
                """
                
                # Console ga chiqarish (development uchun)
                print("=== YANGI XABAR ===")
                print(f"Mavzu: {subject}")
                print(full_message)
                print("==================")
                
                messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi!')
            except Exception as e:
                messages.success(request, 'Xabaringiz qabul qilindi!')
            
            return redirect('contact:contact')
        except Exception as e:
            messages.error(request, 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.')
    
    return render(request, 'contact/contact.html')