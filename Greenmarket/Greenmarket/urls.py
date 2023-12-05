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
from django.contrib import admin
from django.urls import path
from crud import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("iniciosesion/", views.iniciosesion, name="iniciosesion"),
    path("producto", views.producto, name="producto"),
    path("tienda/", views.tienda, name="tienda"),
    path("cerrarsesion/", views.signout, name="cerrarsesion"),
    # cliente
    path(
        "iniciosesion/perfilC/",
        views.crear_perfil_cliente,
        name="perfilC",
    ),
    path("iniciosesion/cliente/", views.obtener_perfil_cliente, name="editarperfilC"),
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
        "iniciosesion/proveedor/", views.obtener_perfil_proveedor, name="editarperfilP"
    ),
    path(
        "iniciosesion/proveedor/editarperfil",
        views.editar_perfil_proveedor,
        name="Proveedor",
    ),
]
