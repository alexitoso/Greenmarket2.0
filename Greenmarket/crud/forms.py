from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Comuna, CustomUser, EstadoCivil, Proveedor, Cliente, Sexo, Usuario


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


# # class RegistroForm(forms.ModelForm):
# #     password = forms.CharField(
# #         widget=forms.PasswordInput(), label="Password", max_length=100
# #     )
# #     password_confirmation = forms.CharField(
# #         widget=forms.PasswordInput(), label="Confirm Password", max_length=100
# #     )
# #     tipo_perfil = forms.ChoiceField(
# #         choices=[("proveedor", "Proveedor"), ("cliente", "Cliente")],
# #         label="Tipo de Perfil",
# #     )

# #     class Meta:
# #         model = CustomUser  # Asocia el formulario con el modelo CustomUser
# #         fields = ["username", "password", "password_confirmation", "tipo_perfil"]

# #     def clean(self):
# #         cleaned_data = super().clean()
# #         password = cleaned_data.get("password")
# #         password_confirmation = cleaned_data.get("password_confirmation")

# #         if password != password_confirmation:
# #             raise forms.ValidationError("Las contraseñas no coinciden.")

# #         return cleaned_data


# # class CustomAuthenticationForm(AuthenticationForm):
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Personaliza los campos si es necesario
# #         # Ejemplo: cambiar etiquetas o agregar clases CSS
# #         self.fields["username"].label = "Nombre de usuario"
# #         self.fields["password"].label = "Contraseña"
# #         self.fields["password"].widget.attrs.update({"class": "password-input"})
# #         # Puedes agregar más personalizaciones aquí

# #     def clean(self):
# #         cleaned_data = super().clean()
# #         # Agrega validaciones adicionales si es necesario
# #         # Por ejemplo, verificación de campos, autenticación personalizada, etc.
# #         return cleaned_data


# class LoginForm(forms.Form):
#     username = forms.CharField(label="Usuario", max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get("username")
#         password = cleaned_data.get("password")

#         if username is not None and password:
#             user = authenticate(username=username, password=password)

#             if user is None or not user.is_active:
#                 raise forms.ValidationError(
#                     "Nombre de usuario o contraseña incorrectos."
#                 )

#         return cleaned_data


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
            "id_usuario",
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
