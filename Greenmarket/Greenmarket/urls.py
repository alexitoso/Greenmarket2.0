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
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("iniciosesion/", views.iniciosesion, name="iniciosesion"),
    path("producto", views.producto, name="producto"),
    path("tienda/", views.mostrar_productos, name="tienda"),
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
