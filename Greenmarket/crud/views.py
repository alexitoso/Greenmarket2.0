from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegistroForm
from django.shortcuts import redirect
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm


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

            # Aquí debes crear tu nuevo usuario utilizando el modelo TuModeloDeUsuario
            nuevo_usuario = Usuario.objects.create(
                username=username, password=password, tipo_perfil=tipo_perfil
            )

            # Guarda el nuevo usuario en la base de datos
            nuevo_usuario.save()

            # Redirecciona a alguna página de éxito o a donde desees
            return redirect("home")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


def iniciosesion(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "home.html",
                {
                    "form": AuthenticationForm,
                    "error": "usuario o contraseña incorrectas",
                },
            )
        else:
            iniciosesion(request, user)
            return redirect("home")


def signout(request):
    logout(request)
    return redirect("home.html")
