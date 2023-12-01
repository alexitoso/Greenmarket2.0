from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class RegistroForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Password", max_length=100
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm Password", max_length=100
    )
    tipo_perfil = forms.ChoiceField(
        choices=[("proveedor", "Proveedor"), ("cliente", "Cliente")],
        label="Tipo de Perfil",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None or not self.user_cache.is_active:
                raise forms.ValidationError("Credenciales inválidas")
        return self.cleaned_data


# intento 1
from .models import Comuna, EstadoCivil, Proveedor, Cliente, Sexo, Usuario


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
            "id_usuario",
        ]


# class ProveedorForm(forms.ModelForm):
#     class Meta:
#         model = Proveedor
#         fields = "__all__"  # Puedes especificar los campos si no quieres todos


# class ClienteForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = "__all__"  # Puedes especificar los campos si no quieres todos


class ClienteForm(forms.ModelForm):
    # Obtener opciones para los campos de clave foránea
    id_sexo = forms.ModelChoiceField(queryset=Sexo.objects.all())
    id_estado = forms.ModelChoiceField(queryset=EstadoCivil.objects.all())
    id_comuna = forms.ModelChoiceField(queryset=Comuna.objects.all())
    id_usuario = forms.ModelChoiceField(queryset=Usuario.objects.all())

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
            "id_usuario",
        ]
