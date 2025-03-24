from django.shortcuts import render, redirect
from .models import Team
from cars.models import Machineryy
from cars.models import Machinery, Tractor, Harvester, SelfPropelledSprayer, Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home(request):
    teams = Team.objects.all()

    featured_cars = [m.get_real_instance() for m in Machinery.objects.all().order_by('-created_date').filter(condition='new')]
    #all_cars = Machineryy.objects.order_by('-created_date')
    #all_cars = Machinery.objects.all().order_by('-created_date')
    all_cars = [m.get_real_instance() for m in Machinery.objects.all().order_by('-created_date')]

    '''for car in all_cars:
        if car.machinery_type == 'selfpropelledsprayer':  # Убедись, что тип совпадает с choices!
            print(f"\n\n{car.tank_capacity}")  # Теперь ошибки не будет 🚀
    '''

        

    brand_search = Machinery.objects.values_list('manufacturer', flat=True).distinct().order_by('manufacturer')
    year_search = Machinery.objects.values_list('year', flat=True).distinct().order_by('-year')
    types_search = [choice[1] for choice in sorted(Machinery.MACHINERY_TYPES, key=lambda x: x[1])]
    max_price = Machinery.objects.all().order_by('-price').first().price + 1000000
    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'brand_search': brand_search,
        'year_search': year_search,
        'types_search': types_search,
        'max_price': max_price,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        email_subject = 'You have a new message from CarDealer Website regarding ' + subject
        message_body = 'Name: ' + name + '. Email: ' + email + '. Phone: ' + phone + '. Message: ' + message

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
                email_subject,
                message_body,
                'petervdlonghand@gmail.com',
                [admin_email],
                fail_silently=False,
            )
        messages.success(request, 'Thank you for contacting us. We will get back to you shortly')
        return redirect('contact')

    return render(request, 'pages/contact.html')
