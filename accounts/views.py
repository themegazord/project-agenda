from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import FormContact


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=user, password=password)

    if not user:
        messages.error(request, 'Usuário ou senha inválido')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso')
    return render(request, 'accounts/dashboard.html')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    password_confirm = request.POST.get('confirm_password')

    if not name or not last_name or not email or not user or not password or not password_confirm:
        messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/register.html')
    
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')


    if len(password) < 6:
        messages.error(request, 'Senha precisa ter 6 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if len(user) < 6:
        messages.error(request, 'Usuário precisa ter 6 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if password != password_confirm:
        messages.error(request, 'Senhas não conferem')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, 'Usuário existente')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso! Faça seu login')
    user = User.objects.create_user(
        username=user,
        email=email,
        password=password,
        first_name=name,
        last_name=last_name,
    )
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.erro(request, 'Erro ao enviar formulário')
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    if len(request.POST.get('description')) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres')
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato: {request.POST.get("name")} salvo com sucesso!!!')
    return redirect('dashboard') 
