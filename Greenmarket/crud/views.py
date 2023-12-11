from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from venv import logger
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
    CambiarEstadoForm,
    ClienteForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
    OrdenCompraForm,
    ProductoForm,
    ProveedorForm,
    TruequeForm,
    # RegistroForm,
)

from django.shortcuts import redirect
from .models import (
    Comuna,
    CustomUser,
    Envio,
    EstadoCivil,
    EstadoSolicitud,
    OrdenCompra,
    OrdenTrueque,
    Pago,
    Producto,
    Sexo,
    Cliente,
    Proveedor,
    TruequeProveedor,
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


# def blog(request):
#     return render(request,"blog.html")


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
    usuario_actual = request.user

    # Obtener el proveedor asociado al usuario actual
    # Obtener el usuario actual
    usuario_actual = request.user

    # Obtener el proveedor asociado al usuario actual
    proveedor_usuario = get_object_or_404(Proveedor, id_usuario=usuario_actual)

    # Obtener los productos asociados al proveedor del usuario actual
    productos = Producto.objects.filter(id_proveedor=proveedor_usuario)

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


# MOSTRAR PRODUCTOS EN LA TIENDA PARA PROVEEDORES
def mostrar_productosP(request):
    usuario_actual = request.user
    proveedor_usuario_actual = get_object_or_404(
        Proveedor, id_usuario=usuario_actual
    )  # Suponiendo que esto devuelve el proveedor del usuario actual

    # Obtener todos los proveedores con productos excepto el proveedor del usuario actual
    proveedores_con_productos = (
        Proveedor.objects.exclude(id_proveedor=proveedor_usuario_actual.id_proveedor)
        .filter(producto__isnull=False)
        .distinct()
    )

    return render(request, "tiendaP.html", {"proveedores": proveedores_con_productos})


# <!-- {% url 'solicitud_trueque' producto.id_producto %} agregar al html cuando funcione el boton


# detalle producto como cliente
def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id_producto=producto_id)
    return render(request, "detalleproducto.html", {"producto": producto})


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


# obtener datos
def obtener_direccion_proveedor_actual(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el proveedor correspondiente al usuario actual
        try:
            proveedor_actual = Proveedor.objects.get(id_usuario=request.user)
            return proveedor_actual.direccion
        except Proveedor.DoesNotExist:
            # Manejar el caso en el que no se encuentre el proveedor
            return None
    else:
        # Manejar el caso en el que el usuario no está autenticado
        return None


def obtener_id_usuario_actual(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el ID del usuario actual
        usuario_actual_id = request.user.id_usuario
        return usuario_actual_id
    return None  # Retornar None si el usuario no está autenticado


def obtener_proveedor_actual(request):
    if request.user.is_authenticated:
        proveedor_actual = get_object_or_404(
            Proveedor, id_usuario=request.user.id_usuario
        )
        return proveedor_actual
    return None  # Retornar None si el usuario no está autenticado


# trueque
def trueque(request, proveedor_id, producto_id):
    proveedor_actual = obtener_proveedor_actual(request)
    if proveedor_actual:
        proveedor_actual_id = proveedor_actual.id_proveedor
        proveedor_seleccionado = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
        producto_seleccionado = get_object_or_404(Producto, id_producto=producto_id)
        direccion_proveedor_destino = producto_seleccionado.id_proveedor.direccion
        direccion_proveedor_actual = obtener_direccion_proveedor_actual(request)
        fecha_actual = date.today()

        opciones_prod_enviado = Producto.objects.filter(
            id_proveedor=proveedor_actual_id
        )
        opciones_prod_recibido = Producto.objects.filter(
            id_proveedor=proveedor_seleccionado.id_proveedor
        )

        if request.method == "POST":
            form = TruequeForm(request.POST)
            if form.is_valid():
                orden_trueque = form.save(commit=False)
                orden_trueque.origen = direccion_proveedor_actual
                orden_trueque.destino = direccion_proveedor_destino
                orden_trueque.itrueque = proveedor_actual_id
                orden_trueque.dtrueque = proveedor_seleccionado.id_proveedor
                orden_trueque.fecha_trueque = fecha_actual
                orden_trueque.save()
                return redirect("home")
            else:
                print(form.errors)
        else:
            form = TruequeForm(
                initial={
                    "origen": direccion_proveedor_actual,
                    "destino": direccion_proveedor_destino,
                    "itrueque": proveedor_actual_id,
                    "dtrueque": proveedor_seleccionado.id_proveedor,
                    "fecha_trueque": fecha_actual,
                }
            )
            form.fields["prod_enviado"].queryset = opciones_prod_enviado
            form.fields["prod_recibido"].queryset = opciones_prod_recibido
    else:
        form = TruequeForm()

    return render(request, "trueque.html", {"form": form})


# solicitudes
def mis_solicitudes(request):
    proveedor_actual = obtener_proveedor_actual(request)

    if proveedor_actual:
        solicitudes = OrdenTrueque.objects.filter(
            itrueque=proveedor_actual.id_proveedor
        )
        proveedores_solicitud = {}

        for solicitud in solicitudes:
            try:
                proveedor_solicitud = Proveedor.objects.get(
                    id_proveedor=solicitud.dtrueque
                )
                proveedores_solicitud[solicitud.id_otrueque] = proveedor_solicitud
            except Proveedor.DoesNotExist:
                # Manejar el caso en el que no se encuentra un proveedor para la solicitud
                # Puedes omitir esta solicitud o manejarlo de acuerdo a tu lógica
                pass

        return render(
            request,
            "mis_solicitudes.html",
            {
                "solicitudes": solicitudes,
                "proveedores_solicitud": proveedores_solicitud,
            },
        )
    else:
        # Manejar el caso en el que no hay un proveedor actual
        # Puedes redirigir al usuario a otra página o mostrar un mensaje de error
        return render(request, "registro.html")


def solicitudes_recibidas(request):
    proveedor_actual = obtener_proveedor_actual(request)

    if proveedor_actual:
        solicitudes_recibidas = OrdenTrueque.objects.filter(
            dtrueque=proveedor_actual.id_proveedor
        )
        proveedores_solicitud = {}

        for solicitud in solicitudes_recibidas:
            proveedor_solicitud = Proveedor.objects.get(id_proveedor=solicitud.itrueque)
            proveedores_solicitud[solicitud.id_otrueque] = proveedor_solicitud

        return render(
            request,
            "solicitudes_recibidas.html",
            {
                "solicitudes_recibidas": solicitudes_recibidas,
                "proveedores_solicitud": proveedores_solicitud,
            },
        )


from django.http import JsonResponse


def cambiar_estado_solicitud(request, solicitud_id):
    if request.method == "POST" and request.is_ajax():
        solicitud = get_object_or_404(OrdenTrueque, pk=solicitud_id)
        estado_actual = EstadoSolicitud.objects.get(solicitud=solicitud)

        # Cambiar el estado de Pendiente a Aceptado
        if estado_actual.estado == EstadoSolicitud.PENDIENTE:
            estado_actual.estado = EstadoSolicitud.ACEPTADO
            estado_actual.save()

            return JsonResponse({"message": "Estado cambiado a Aceptado correctamente"})

        # Cambiar el estado a Rechazado si no está Aceptado
        elif estado_actual.estado != EstadoSolicitud.ACEPTADO:
            estado_actual.estado = EstadoSolicitud.RECHAZADO
            estado_actual.save()

            return JsonResponse(
                {"message": "Estado cambiado a Rechazado correctamente"}
            )

    return JsonResponse({}, status=400)
