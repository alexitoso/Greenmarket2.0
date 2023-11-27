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


# Create your views here.
def home(request):
    return render(request, "home.html")


def producto(request):
    return render(request, "productos.html")


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


def iniciosesion(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Autenticación manual
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")
