from django.contrib import admin
from .models import Usuario


# Register your models here.
class Usuarioadmin(admin.ModelAdmin):
    readonly_fields = ("tipo_perfil",)


# Register your models here.

admin.site.register(Usuario, Usuarioadmin)
