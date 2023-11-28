from django.shortcuts import redirect
from django.urls import reverse


class ProfileRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.Usuario.is_anonymous:
            # Verificar si el usuario tiene un perfil
            if not hasattr(request.Usuario, "perfil"):
                # Si no tiene perfil, redirigir a la creación de perfil
                return redirect(reverse("crear_perfil"))

        response = self.get_response(request)
        return response
