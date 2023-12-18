"""
URL configuration for Greenmarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from crud import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.blog, name="blog"),
    path("home/", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("home/iniciosesion/", views.iniciosesion, name="iniciosesion"),
    # tienda para proveedores
    path("tiendaP/", views.mostrar_productosP, name="tiendaP"),
    # cerrar sesion
    path("cerrarsesion/", views.signout, name="cerrarsesion"),
    # cliente
    path(
        "iniciosesion/perfilC/",
        views.crear_perfil_cliente,
        name="perfilC",
    ),
    path(
        "iniciosesion/cliente/editarperfil",
        views.editar_perfil_cliente,
        name="Cliente",
    ),
    # proveedor
    path(
        "iniciosesion/perfilP/",
        views.crear_perfil_proveedor,
        name="perfilP",
    ),
    path(
        "iniciosesion/proveedor/editarperfil",
        views.editar_perfil_proveedor,
        name="Proveedor",
    ),
    path(
        "detalleproducto/<int:producto_id>/",
        views.detalle_producto,
        name="detalleproducto",
    ),
    # crud productos
    path("listar-productos/", views.listar_productos, name="listar_productos"),
    path("crear-producto/", views.crear_producto, name="crear_producto"),
    path(
        "editar-producto/<int:producto_id>/",
        views.editar_producto,
        name="editar_producto",
    ),
    path(
        "eliminar-producto/<int:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    # carrito -------------------
    path("carro/", views.mostrar_productos, name="carro"),
    path("agregar/<int:producto_id>/", views.agregar_carro, name="agregar"),
    path("eliminar/<int:producto_id>/", views.eliminar_carro, name="eliminar"),
    path("restar/<int:producto_id>/", views.restar_carro, name="restar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
    # orden de compra
    path("ordencompra", views.confirmar_compra, name="orden"),
    # trueque
    path(
        "trueque/<int:proveedor_id>/<int:producto_id>/", views.trueque, name="trueque"
    ),
    path("mis-solicitudes/", views.mis_solicitudes, name="mis_solicitudes"),
    path(
        "solicitudes-recibidas/",
        views.solicitudes_recibidas,  # type: ignore
        name="solicitudes_recibidas",
    ),  # type: ignore
    # URL para aceptar una solicitud de trueque específica
    path(
        "aceptar-solicitud/<int:solicitud_id>/",
        views.aceptar_solicitud,
        name="aceptar_solicitud",
    ),
    # URL para rechazar una solicitud de trueque específica
    path(
        "rechazar-solicitud/<int:solicitud_id>/",
        views.rechazar_solicitud,
        name="rechazar_solicitud",
    ),
    path("boleta/<int:id_orden>/", views.boleta, name="boleta"),
    path(
        "historial/",
        views.historial,
        name="historial",
    ),
    path("pago/", views.pago, name="pago"),
    # transbank
    # URL para iniciar la transacción
    #     path("iniciar_transaccion/", views.iniciar_transaccion, name="iniciar_transaccion"),
    #     # URL para recibir el resultado de la transacción desde Webpay
    #     path(
    #         "resultado_transaccion/",
    #         views.resultado_transaccion,
    #         name="resultado_transaccion",
    #     ),
    #     # URL para mostrar el comprobante al tarjetahabiente
    #     path("mostrar_comprobante/", views.mostrar_comprobante, name="mostrar_comprobante"),
    #     # URL para mostrar el comprobante o página de éxito al usuario
    #     path("comprobante_exitoso/", views.comprobante_exitoso, name="comprobante_exitoso"),
    #     #     path(
    #     #         "error",
    #     #         views.error_view,
    #     #         name="error",
    #     #     ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
