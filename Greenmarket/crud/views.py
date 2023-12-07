from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.contrib.auth import (
    login,
    logout,
    authenticate,
    get_user_model,
)
from .forms import (
    ClienteForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
    ProductoForm,
    ProveedorForm,
    # RegistroForm,
)

from django.shortcuts import redirect
from .models import (
    Comuna,
    CustomUser,
    EstadoCivil,
    OrdenCompra,
    Producto,
    Sexo,
    Usuario,
    Cliente,
    Proveedor,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password  # Importa make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


# Create your views here.
@login_required
def home(request):
    tiene_perfil_cliente = Cliente.objects.filter(id_usuario=request.user).exists()
    tiene_perfil_proveedor = Proveedor.objects.filter(id_usuario=request.user).exists()

    return render(
        request,
        "home.html",
        {
            "tiene_perfil_cliente": tiene_perfil_cliente,
            "tiene_perfil_proveedor": tiene_perfil_proveedor,
        },
    )


def signout(request):
    logout(request)
    # Redirigir a la página de inicio u otra página después de cerrar sesión
    return redirect("home")


@login_required
@csrf_protect
def producto(request):
    return render(request, "productos.html")


# def tienda(request):
#     return render(request, "tienda.html")


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            password_confirmation = form.cleaned_data["password2"]

            if password != password_confirmation:
                form.add_error("password2", "Las contraseñas no coinciden.")
                return render(request, "registro.html", {"form": form})

            user = form.save()

            # Autenticación después de crear el usuario
            user = authenticate(request, username=user.username, password=password)
            login(request, user)

            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "registro.html", {"form": form})


def iniciosesion(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirige al usuario a la página 'next' si está definida, de lo contrario, redirige a 'home'
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()

    return render(request, "login.html", {"form": form})


# cliente


@never_cache
def crear_perfil_cliente(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo_cliente = form.save(commit=False)
            nuevo_cliente.id_usuario = request.user  # Asigna el usuario actual
            nuevo_cliente.save()
            return redirect("Cliente")  # Redirige al perfil después de guardar
    else:
        form = ClienteForm(
            initial={
                "id_sexo": Sexo.objects.first(),  # Ejemplo para obtener el primer objeto
                "id_estado": EstadoCivil.objects.first(),
                "id_comuna": Comuna.objects.first(),
            }
        )

    return render(request, "crearperfilC.html", {"form": form})


# def obtener_perfil_cliente(request):
#     try:
#         perfil_cliente = Cliente.objects.get(id_usuario=request.user)
#     except Cliente.DoesNotExist:
#         perfil_cliente = None

#     if request.method == "POST":
#         form = ClienteForm(request.POST, instance=perfil_cliente)
#         if form.is_valid():
#             form.save()
#             return redirect("Cliente")  # Redirige al perfil después de guardar
#     else:
#         form = ClienteForm(instance=perfil_cliente)

#     return render(request, "obtenerperfilC.html", {"form": form})


def editar_perfil_cliente(request):
    perfil_cliente = get_object_or_404(Cliente, id_usuario=request.user)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=perfil_cliente)
        if form.is_valid():
            form.save()
            return redirect(
                "Cliente"
            )  # Redirige a la página del perfil después de guardar

    else:
        form = ClienteForm(instance=perfil_cliente)

    return render(request, "cliente.html", {"form": form})


# proveedor


@never_cache
def crear_perfil_proveedor(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = ProveedorForm(request.POST)
        if form.is_valid():
            nuevo_proveedor = form.save(commit=False)
            nuevo_proveedor.id_usuario = request.user  # Asigna el usuario actual
            nuevo_proveedor.save()
            return redirect("Proveedor")  # Redirige al perfil después de guardar
    else:
        form = ProveedorForm()

    return render(request, "crearperfilP.html", {"form": form})


# def obtener_perfil_proveedor(request):
#     try:
#         perfil_proveedor = Proveedor.objects.get(id_usuario=request.user)
#     except Proveedor.DoesNotExist:
#         perfil_proveedor = None

#     if request.method == "POST":
#         form = ProveedorForm(request.POST, instance=perfil_proveedor)
#         if form.is_valid():
#             form.save()
#             return redirect("Proveedor")  # Redirige al perfil después de guardar
#     else:
#         form = ProveedorForm(instance=perfil_proveedor)

#     return render(request, "obtenerperfilP.html", {"form": form})


def editar_perfil_proveedor(request):
    perfil_proveedor = get_object_or_404(Proveedor, id_usuario=request.user)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=perfil_proveedor)
        if form.is_valid():
            form.save()
            return redirect(
                "Proveedor"
            )  # Redirige a la página del perfil después de guardar

    else:
        form = ProveedorForm(instance=perfil_proveedor)

    return render(request, "proveedor.html", {"form": form})


# carga de productos
def cargar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "home"
            )  # Cambia 'pagina_de_inicio' por la URL a la que quieras redirigir después de guardar el producto
    else:
        form = ProductoForm()

    return render(request, "crearproducto.html", {"form": form})


# MOSTRAR EN TIENDA
# def mostrar_productos(request):
#     # Obtener los productos asociados a la sesión actual
#     productos_usuario = Producto.objects.filter(usuario=request.user)

#     return render(request, "tienda.html", {"productos": productos_usuario})
from django.shortcuts import render
from .models import Producto


def mostrar_productos(request):
    # Obtener todos los productos y sus proveedores a través de OrdenDeCompra
    productos_con_proveedor = []
    productos = Producto.objects.all()

    for producto in productos:
        orden_compra = OrdenCompra.objects.filter(producto=producto).first()
        proveedor = OrdenCompra.id_proveedor
        usuario_proveedor = Proveedor.id_usuario

        # Agregar los datos del producto y su proveedor a la lista
        productos_con_proveedor.append(
            {
                "producto": producto,
                "proveedor": proveedor,
                "usuario_proveedor": usuario_proveedor,
            }
        )

    return render(
        request, "tienda.html", {"productos_con_proveedor": productos_con_proveedor}
    )
