from typing import Required
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import (
    Comuna,
    CustomUser,
    Envio,
    EstadoCivil,
    OrdenCompra,
    Pago,
    Producto,
    Proveedor,
    Cliente,
    Sexo,
    Usuario,
)


class CustomUserCreationForm(UserCreationForm):
    tipo_perfil = forms.ChoiceField(
        choices=[("proveedor", "Proveedor"), ("cliente", "Cliente")],
        label="Tipo de Perfil",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "tipo_perfil")


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")


# intento 1


class ProveedorForm(forms.ModelForm):
    id_comuna = forms.ModelChoiceField(queryset=Comuna.objects.all())
    id_estado = forms.ModelChoiceField(queryset=EstadoCivil.objects.all())
    id_sexo = forms.ModelChoiceField(queryset=Sexo.objects.all())

    class Meta:
        model = Proveedor
        fields = [
            "rut_proveedor",
            "dv_proveedor",
            "id_comuna",
            "edad",
            "nombre_proveedor",
            "apellidom",
            "apellidop",
            "direccion",
            "nombre_tienda",
            "descripcion",
            "telefono",
            "id_estado",
            "id_sexo",
            "correo",
        ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "id_sexo",
            "id_estado",
            "id_comuna",
            "rut_cliente",
            "dv_cliente",
            "pnombre",
            "snombre",
            "apellidom",
            "apellidop",
            "telefono",
            "edad",
            "direccion",
            "correo",
        ]
        widgets = {
            "id_sexo": forms.Select(),  # Define el widget Select para id_sexo
            "id_estado": forms.Select(),  # Define el widget Select para id_estado
            "id_comuna": forms.Select(),  # Define el widget Select para id_comuna
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Llena las opciones del widget Select con los valores del queryset correspondiente
        self.fields["id_sexo"].queryset = Sexo.objects.all()
        self.fields["id_estado"].queryset = EstadoCivil.objects.all()
        self.fields["id_comuna"].queryset = Comuna.objects.all()

        # Agregar impresión de los querysets
        print("Queryset para id_sexo:", self.fields["id_sexo"].queryset)
        print("Queryset para id_estado:", self.fields["id_estado"].queryset)
        print("Queryset para id_comuna:", self.fields["id_comuna"].queryset)


# productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "tipo_producto",
            "precio",
            "stock",
            "imagen",
        ]


# orden de compra


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = [
            "cant_compra",
            "valor_neto",
            "iva",
            "valor_total",
            "id_cliente",
            "id_proveedor",
            "fecha_compra",
            "id_envio",
            "id_pago",
        ]
        widgets = {
            "id_proveedor": forms.TextInput(attrs={"readonly": "readonly"}),
            "id_envio": forms.Select(),
            "id_pago": forms.Select(),
            "id_cliente": forms.TextInput(attrs={"readonly": "readonly"}),
            "fecha_compra": forms.DateInput(attrs={"readonly": "readonly"}),
            "cant_compra": forms.TextInput(attrs={"readonly": "readonly"}),
            "valor_total": forms.TextInput(attrs={"readonly": "readonly"}),
            "valor_neto": forms.TextInput(attrs={"readonly": "readonly"}),
            "iva": forms.TextInput(attrs={"readonly": "readonly"}),
        }
