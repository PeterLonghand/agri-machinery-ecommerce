# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Создаем базовый объект Contact
        contact = Contact(
            car_id=car_id,
            car_title=car_title,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            email=email,
            phone=phone,
            message=message,
        )
        
        # Если это лизинговая заявка, сохраняем дополнительные параметры
        if customer_need == 'Лизинг':
            
            contact.leasing_advance = request.POST.get('leasing_advance')
            contact.leasing_term = request.POST.get('leasing_term')
            contact.leasing_payment_type = request.POST.get('leasing_payment_type')
            contact.leasing_monthly_payment = request.POST.get('leasing_monthly_payment')
            contact.leasing_full_payment = request.POST.get('leasing_full_payment')
        
        contact.save()
        
        messages.success(request, 'Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
        return redirect('/catalog/' + car_id)
    



@login_required
def delete_inquiry(request, inquiry_id):
    # Получаем заявку по ID
    inquiry = get_object_or_404(Contact, id=inquiry_id)
    
    # Проверяем, принадлежит ли заявка текущему пользователю
    if str(inquiry.user_id) != str(request.user.id):
        messages.error(request, 'У вас нет прав для удаления этой заявки')
        return redirect('dashboard')
    
    # Проверяем статус заявки
    if inquiry.status != 'processing':
        messages.error(request, 'Нельзя удалить заявку, которая уже обработана')
        return redirect('dashboard')
    
    # Название техники для сообщения
    car_title = inquiry.car_title
    
    # Удаляем заявку
    inquiry.delete()
    
    # Показываем сообщение об успехе
    messages.success(request, f'Заявка на технику "{car_title}" успешно удалена')
    
    # Перенаправляем на страницу со списком заявок
    return redirect('dashboard')