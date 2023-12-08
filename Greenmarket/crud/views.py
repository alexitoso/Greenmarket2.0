from datetime import date
from decimal import ROUND_HALF_UP, Decimal
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

from crud.carrito import Carrito
from .forms import (
    ClienteForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
    OrdenCompraForm,
    ProductoForm,
    ProveedorForm,
    # RegistroForm,
)

from django.shortcuts import redirect
from .models import (
    Comuna,
    CustomUser,
    Envio,
    EstadoCivil,
    OrdenCompra,
    Pago,
    Producto,
    Sexo,
    Cliente,
    Proveedor,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password  # Importa make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


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


# crud de productos como proveedor
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, "listarproductos.html", {"productos": productos})


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            if request.user.is_authenticated:
                proveedor_actual = Proveedor.objects.get(id_usuario=request.user)
                producto.id_proveedor = proveedor_actual
                producto.save()
                return redirect("listar_productos")
    else:
        form = ProductoForm()
    return render(request, "crear_producto.html", {"form": form})


def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("listar_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "editar_producto.html", {"form": form})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect("listar_productos")
    return render(request, "eliminar_producto.html", {"producto": producto})


# mostrar productos en la tienda como cliente


def mostrar_productos(request):
    proveedores_con_productos = Proveedor.objects.filter(
        producto__isnull=False
    ).distinct()
    return render(request, "tienda.html", {"proveedores": proveedores_con_productos})


# detalle producto como cliente
def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id_producto=producto_id)
    return render(request, "detalleproducto.html", {"producto": producto})


# carrito de compra


# def agregar_al_carrito(request, producto_id, cantidad):
#     producto = get_object_or_404(Producto, id_producto=producto_id)

#     # Verificar si hay suficientes existencias para la cantidad deseada
#     if producto.stock >= cantidad:
#         # Agregar al carrito en la sesión del usuario
#         if "carrito" not in request.session:
#             request.session["carrito"] = {}

#         carrito = request.session["carrito"]

#         if producto_id not in carrito:
#             carrito[producto_id] = {
#                 "id_producto": producto.id_producto,
#                 "nombre": producto.nombre,
#                 "precio": producto.precio,
#                 # Otros detalles del producto que quieras guardar en el carrito
#                 "cantidad": cantidad,  # Guardar la cantidad en el carrito
#             }
#             request.session.modified = True

#             # Reducir la cantidad en el stock de la base de datos
#             producto.stock -= cantidad
#             producto.save()

#         return redirect(
#             "carrito"
#         )  # Redirigir al carrito después de agregar el producto
#     else:
#         messages.error(request, "No hay suficientes existencias de este producto.")
#         return redirect("carrito")  # Redirigir al carrito con el mensaje de error

# #orden de compra
# def crear_orden_compra(request):
#     if request.method == "POST":
#         # Obtener datos del formulario (id_envio, id_pago, lista de productos, etc.)
#         lista_productos = request.POST.getlist('productos')  # Ejemplo, obtener una lista de productos
#         producto_id = request.POST.get("producto_id")
#         producto = Producto.objects.get(id=producto_id)
#         precio = producto.precio
#         iva_porcentaje = 19  # Supongamos un 19% de IVA
#         # Calcular valores de la orden de compra (valor neto, iva, precio total, etc.)
#         valor_neto = ((precio * (iva_porcentaje / 100))*(lista_productos))
#         iva = calcular_iva(valor_neto)
#         precio_total = valor_neto + iva

#         # Obtener el ID del cliente desde la sesión (suponiendo que está autenticado)
#         id_cliente = request.user.id  # Asegúrate de tener acceso al ID del cliente autenticado

#         # Crear la orden de compra y guardarla en la base de datos
#         orden_compra = OrdenCompra.objects.create(
#             id_cliente=id_cliente,
#             id_envio=id_envio,
#             id_pago=id_pago,
#             valor_neto=valor_neto,
#             iva=iva,
#             precio_total=precio_total
#         )

#         # Asociar los productos a la orden de compra (asumiendo que 'lista_productos' contiene los IDs de los productos)
#         for producto_id in lista_productos:
#             producto = Producto.objects.get(pk=producto_id)
#             orden_compra.productos.add(producto)

#         return redirect('detalle_orden_compra', pk=orden_compra.pk)  # Redirigir a la página de detalle de la orden
#     else:
#         # Lógica para mostrar el formulario para seleccionar envío, pago y productos
#         # ...

#     return render(request, 'crear_orden_compra.html', context)


# def ver_carrito(request):
#     carrito = request.session.get("carrito", {})
#     productos_carrito = carrito.values()
#     total = sum(item["precio"] for item in productos_carrito)

#     return render(
#         request,
#         "carrito.html",
#         {"productos_carrito": productos_carrito, "total": total},
#     )


# def eliminar_del_carrito(request, producto_id):
#     if "carrito" in request.session:
#         carrito = request.session["carrito"]
#         if producto_id in carrito:
#             del carrito[producto_id]
#             request.session.modified = True

#     return redirect("carrito")


# carro
def agregar_carro(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.agregar(producto)
    return redirect("carro")


def eliminar_carro(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.eliminar(producto)
    return redirect("carro")


def restar_carro(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.restar(producto)
    return redirect("carro")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carro")


# orden de compra
# def confirmar_compra(request):
#     # Obtener datos del carrito desde la sesión
#     carrito = request.session.get("carrito", {})

#     # Calcular los valores para la orden de compra
#     total_cantidad = sum(item["cantidad"] for item in carrito.values())
#     valor_neto = sum(item["acumulado"] for item in carrito.values())
#     iva = Decimal("0.19") * valor_neto  # Suponiendo un IVA del 19%
#     valor_total = valor_neto + iva

#     # Rellenar el formulario con los valores calculados
#     form = OrdenCompraForm(
#         initial={
#             "cant_compra": total_cantidad,
#             "valor_neto": valor_neto,
#             "iva": iva,
#             "valor_total": valor_total,
#         }
#     )

#     context = {"form": form}

#     return render(request, "ordencompra.html", context)


def confirmar_compra(request):
    # Obtener datos del carrito desde la sesión
    carrito = request.session.get("carrito", {})

    # Calcular los valores para la orden de compra
    total_cantidad = sum(item["cantidad"] for item in carrito.values())
    valor_neto = sum(item["acumulado"] / Decimal("1.19") for item in carrito.values())
    valor_neto = round(valor_neto, 2)

    # Calcular el IVA y redondear a 2 decimales
    iva = Decimal("0.19") * valor_neto
    iva = round(iva, 2)
    valor_total = valor_neto + iva
    valor_total = str(valor_total) if valor_total % 1 > 0 else str(int(valor_total))

    # Obtener el ID del cliente desde la sesión
    id_cliente = request.user.cliente_set.first().id_cliente

    # Obtener el ID del proveedor del primer producto en el carrito
    primer_producto_id = next(iter(carrito), None)
    id_proveedor = None

    if primer_producto_id:
        try:
            primer_producto = Producto.objects.get(id_producto=int(primer_producto_id))
            if primer_producto.id_proveedor:
                id_proveedor = primer_producto.id_proveedor.id_proveedor
        except Producto.DoesNotExist:
            pass

    # Obtener la fecha actual
    fecha_actual = date.today()

    if request.method == "POST":
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            nueva_orden = form.save(commit=False)
            nueva_orden.cant_compra = total_cantidad
            nueva_orden.valor_neto = valor_neto
            nueva_orden.iva = iva
            nueva_orden.valor_total = valor_total
            nueva_orden.id_cliente = id_cliente
            nueva_orden.id_proveedor = id_proveedor
            nueva_orden.fecha_compra = fecha_actual
            nueva_orden.save()

            # Redirigir al usuario a la pasarela de pago de Transbank
            return redirect(
                "https://webpay3gint.transbank.cl/"
            )  # Redirige al host de Transbank
    else:
        form = OrdenCompraForm(
            initial={
                "cant_compra": total_cantidad,
                "valor_neto": valor_neto,
                "iva": iva,
                "valor_total": valor_total,
                "id_cliente": id_cliente,
                "id_proveedor": id_proveedor,
                "fecha_compra": fecha_actual,
            }
        )

    context = {"form": form}
    return render(request, "ordencompra.html", context)
