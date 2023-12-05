from django.contrib import admin
from .models import Cliente, Usuario


# Register your models here.
class Usuarioadmin(admin.ModelAdmin):
    readonly_fields = ("tipo_perfil",)

class Clienteadmin(admin.ModelAdmin):
    readonly_fields = ('id_cliente', 'pnombre', 'snombre', 'apellidom', 'apellidop')
# Register your models here.

admin.site.register(Usuario, Usuarioadmin)
admin.site.register(Cliente, Clienteadmin)
