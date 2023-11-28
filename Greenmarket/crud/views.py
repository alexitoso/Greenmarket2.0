from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegistroForm, LoginForm

from django.shortcuts import redirect
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password  # Importa make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def home(request):
    return render(request, "home.html")


@csrf_protect
def producto(request):
    return render(request, "productos.html")


@csrf_protect
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            tipo_perfil = form.cleaned_data["tipo_perfil"]

            # Encripta la contraseña antes de guardarla
            hashed_password = make_password(password)

            # Crea un nuevo usuario utilizando el modelo TuModeloDeUsuario
            nuevo_usuario = Usuario.objects.create(
                username=username, password=hashed_password, tipo_perfil=tipo_perfil
            )

            # Guarda el nuevo usuario en la base de datos
            nuevo_usuario.save()

            # Redirecciona a alguna página de éxito o a donde desees
            return redirect("home")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


from django.contrib.auth.hashers import check_password


def iniciosesion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            usuario = Usuario.objects.get(username=username)
            if check_password(
                password, usuario.password
            ):  # Verifica la contraseña utilizando check_password
                request.session["username"] = usuario.username
                request.session["tipo_perfil"] = usuario.tipo_perfil

                return render(request, "home.html")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos..!")
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos..!")

    return render(request, "login.html")


def signout(request):
    logout(request)
    return redirect("home")


def tienda(request):
    return render(request, "tienda.html")
