from django.shortcuts import redirect
from django.urls import reverse

from .forms import LoginForm


from .models import Usuario  # Reemplaza "tu_app" con el nombre real de tu aplicación


class ProfileRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Verificar si el usuario tiene un perfil de proveedor o cliente
            try:
                perfil = Usuario.objects.get(
                    usuario=request.session
                )  # Obtener el perfil asociado al usuario autenticado
                if perfil.tipo_perfil not in ["proveedor", "cliente"]:
                    # Redirigir al usuario para crear el perfil correspondiente si no es proveedor ni cliente
                    return redirect(reverse("crearperfil"))
            except Usuario.DoesNotExist:
                # Si el perfil no existe, redirigir al usuario para crearlo
                return redirect(reverse("crearperfil"))

        response = self.get_response(request)
        return response
