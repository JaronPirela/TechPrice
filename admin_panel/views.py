from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from scrap import views


# Create your views here.

# Renderizar Home
def home(request):
    return render(request, 'home.html')

# Renderizar Welcome

def welcome(request):
    return render(request, 'welcome.html')

# Renderizar y formulario de Sign In

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(views.main)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

# Funcion de boton Signout


def signout(request):
    logout(request)
    return redirect('home')


# Renderizar y formulario de Login
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_view.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login_view.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect(views.main)


# Admin-Dashboard

# Decorador para verificar si el usuario es superuser o admin

def admin_required(user):
    return user.is_superuser

# Renderizar Login de Admin


@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    if request.method == 'GET':
        return render(request, 'admin.html')

# Renderizar y clasificar lista de usuarios


@login_required
@user_passes_test(admin_required)
def user_list(request):
    superusers = User.objects.filter(is_superuser=True)
    normal_users = User.objects.filter(is_superuser=False)
    return render(request, 'user_list.html', {'superusers': superusers, 'normal_users': normal_users})


# Renderizar detalles de usuario
@login_required
@user_passes_test(admin_required)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_detail.html', {'user': user})

# login de Admin

def login_admin(request):
    if request.method == 'GET':
        return render(request, 'login_admin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login_admin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('admin_dashboard')

# Modificar usuario
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, "No puedes editar un superusuario.")
        return redirect('user_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        # Actualizar los datos del usuario
        user.username = username
        user.email = email

        # Cambiar la contraseña si se proporciona una nueva
        if new_password:
            user.password = make_password(new_password)

        user.save()
        messages.success(request, "Usuario actualizado con éxito.")
        return redirect('user_list')

    return render(request, 'edit_user.html', {'user': user})


# Borrar usuario
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
    return redirect('user_list')
