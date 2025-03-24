from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверные учетные данные')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Пользователь с таким email уже существует!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=firstname, 
                        last_name=lastname, 
                        email=email, 
                        username=username, 
                        password=password
                    )
                    user.save()
                    
                    # Сразу авторизуем пользователя
                    auth.login(request, user)
                    messages.success(request, 'Вы успешно зарегистрировались и вошли в систему')
                    return redirect('dashboard')
        else:
            messages.error(request, 'Пароли не совпадают')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    



def register_ajax(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        response_data = {}

        if password != confirm_password:
            response_data['status'] = 'error'
            response_data['message'] = 'Пароли не совпадают'
            return JsonResponse(response_data)

        if User.objects.filter(username=username).exists():
            response_data['status'] = 'error'
            response_data['message'] = 'Пользователь с таким логином уже существует!'
            return JsonResponse(response_data)

        if User.objects.filter(email=email).exists():
            response_data['status'] = 'error'
            response_data['message'] = 'Пользователь с таким email уже существует!'
            return JsonResponse(response_data)

        try:
            user = User.objects.create_user(
                first_name=firstname, 
                last_name=lastname, 
                email=email, 
                username=username, 
                password=password
            )
            user.save()
            
            # Авторизуем пользователя
            auth.login(request, user)
            
            response_data['status'] = 'success'
            response_data['message'] = 'Вы успешно зарегистрировались и вошли в систему.'
            response_data['redirect_url'] = '/dashboard/'  # URL для перенаправления после успеха
            
            return JsonResponse(response_data)
        except Exception as e:
            response_data['status'] = 'error'
            response_data['message'] = f'Ошибка при регистрации: {str(e)}'
            return JsonResponse(response_data)
            
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})

@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    # count = Contact.objects.order_by('-create_date').filter(user_id=request.user.id).count()

    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
