from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import ClienteForm, ProveedorForm, RegistroForm, LoginForm

from django.shortcuts import redirect
from .models import Comuna, EstadoCivil, Sexo, Usuario, Cliente, Proveedor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password  # Importa make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
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
                request.session["id_usuario"] = usuario.id_usuario

                return render(request, "home.html")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos..!")
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos..!")

    return render(request, "login.html")

@login_required
def signout(request):
    logout(request)
    return redirect("home")

@login_required
def tienda(request):
    return render(request, "tienda.html")

@login_required
def crear_perfil_proveedor(request):
    if request.method == "POST":
        proveedor_form = ProveedorForm(request.POST)
        if proveedor_form.is_valid():
            proveedor = proveedor_form.save(commit=False)
            proveedor.id_usuario_id = request.session["id_usuario"]
            proveedor.save()
            # Puedes redirigir a una página de éxito o realizar otra acción
    else:
        proveedor_form = ProveedorForm()

    return render(request, "crearperfilP.html", {"proveedor_form": proveedor_form})


# # @login_required
# # def crear_perfil_cliente(request):
# #     if request.method == "Get":
# #         cliente_form = ClienteForm(request.POST)
# #         if cliente_form.is_valid():
# #             cliente = cliente_form.save(
# #                 commit=False
# #             )  # Obtén una instancia del modelo sin guardarla aún
# #             cliente.id_usuario_id = request.session[
# #                 "id_usuario"
# #             ]  # Asigna el id_usuario desde la sesión
# #             cliente.save()  # Guarda el objeto Cliente en la base de datos
# #             # Puedes redirigir a una página de éxito o realizar otra acción
# #     else:
# #         cliente_form = ClienteForm()

# #     return render(request, "crearperfilC.html", {"cliente_form": cliente_form})

@login_required
def clientes(request):
        # Obtener el cliente según el id_usuario actual
    id_usuario_actual = request.user.id
    client = Cliente.objects.filter(id_usuario=id_usuario_actual).first()

    return render(request, 'cliente.html', {'client': client})


@login_required
def crear_perfil_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                nueva_carga = form.save(commit=False)
                nueva_carga.id_usuario = request.user
                nueva_carga.save()
                return redirect('cliente')  # Redirige al perfil después de guardar
            except ValueError:
                return render(
                    request,
                    "crearperfilC.html",
                    {"form": form, "error": "Entregue datos válidos"},
                )
        else:
            return render(
                request,
                "crearperfilC.html",
                {"form": form, "error": "Formulario inválido"},
            )
    else:
        form = ClienteForm()  # Si no es un método POST, crea un formulario vacío
        return render(request, "crearperfilC.html", {"form": form})

@login_required
def perfilcliente(request, id_cliente):
    

    if request.method == "GET":
        client = get_object_or_404(Cliente, pk=id_cliente, id_usuario=request.user.id)
        form = ClienteForm(instance=client)
        return render(request, "obtenerperfilC.html", {"client": client, "form": form})
    else:
        try:
            client = get_object_or_404(Cliente, pk=id_cliente, id_usuario=request.user.id)
            form = ClienteForm(request.POST, instance=client)
            form.save()
            return redirect("cliente")
        except ValueError:
            return (
                request,
                "obtenerperfilC.html",
                {
                    "client": client,
                    "form": form,
                    "error": "Error al actualizar el perfil",
                },
            )


@login_required
def mostrar_comunas(request):
    comunas = Comuna.objects.all()
    print(comunas)
    return render(request, "crearperfil.html", {"comunas": comunas})

@login_required
def mostrar_sexo(request):
    sexos = Sexo.objects.all()
    print(sexos)
    return render(request, "crearperfil.html", {"sexos": sexos})

@login_required
def mostrar_estado(request):
    estados = EstadoCivil.objects.all()
    print(estados)
    return render(request, "crearperfil.html", {"estados": estados})
