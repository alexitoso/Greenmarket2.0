# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class Cliente(models.Model):
    id_cliente = models.BigAutoField(primary_key=True)
    id_sexo = models.ForeignKey("Sexo", models.DO_NOTHING, db_column="id_sexo")
    id_estado = models.ForeignKey(
        "EstadoCivil", models.DO_NOTHING, db_column="id_estado"
    )
    id_comuna = models.ForeignKey("Comuna", models.DO_NOTHING, db_column="id_comuna")
    rut_cliente = models.BigIntegerField()
    dv_cliente = models.CharField(max_length=1)
    pnombre = models.CharField(max_length=50)
    snombre = models.CharField(max_length=50, blank=True, null=True)
    apellidom = models.CharField(max_length=50)
    apellidop = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    edad = models.BigIntegerField()
    direccion = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    id_usuario = models.ForeignKey("Usuario", models.DO_NOTHING, db_column="id_usuario")

    class Meta:
        managed = False
        db_table = "cliente"


class Comuna(models.Model):
    id_region = models.ForeignKey("Region", models.DO_NOTHING, db_column="id_region")
    id_comuna = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "comuna"

    def __str__(self):
        return self.descripcion


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class Envio(models.Model):
    id_envio = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    ncomuna = models.CharField(max_length=50)
    nregion = models.CharField(max_length=50)
    enviopagado = models.CharField(max_length=1)
    tipo_envio = models.CharField(max_length=50)
    peso = models.BigIntegerField()
    fecha_envio = models.DateField()

    class Meta:
        managed = False
        db_table = "envio"


class EstadoCivil(models.Model):
    id_estado = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "estado_civil"

    def __str__(self):
        return self.descripcion


class GreenmarketappUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    tipo_perfil = models.CharField(max_length=10, blank=True, null=True)
    rut_cliente = models.BigIntegerField()
    rut_proveedor = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "greenmarketapp_usuario"


class LoginUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "login_user"


class OrdenCompra(models.Model):
    id_compra = models.BigAutoField(primary_key=True)
    id_proveedor = models.BigIntegerField()
    id_envio = models.ForeignKey(Envio, models.DO_NOTHING, db_column="id_envio")
    id_pago = models.ForeignKey("Pago", models.DO_NOTHING, db_column="id_pago")
    id_producto = models.ForeignKey(
        "Producto", models.DO_NOTHING, db_column="id_producto"
    )
    id_cliente = models.BigIntegerField()
    fecha_compra = models.CharField(max_length=50)
    cant_compra = models.BigIntegerField()
    valor_neto = models.BigIntegerField()
    iva = models.BigIntegerField()
    valor_total = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "orden_compra"


class OrdenTrueque(models.Model):
    id_otrueque = models.BigAutoField(primary_key=True)
    origen = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    cant_recibida = models.BigIntegerField()
    cant_enviada = models.BigIntegerField()
    itrueque = models.CharField(max_length=50)
    dtrueque = models.CharField(max_length=50)
    fecha_trueque = models.DateField()
    prod_enviado = models.CharField(max_length=50)
    prod_recibido = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "orden_trueque"


class Pago(models.Model):
    id_pago = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "pago"

    def __str__(self):
        return self.descripcion


class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    tipo_producto = models.CharField(max_length=50)
    precio = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "producto"


class Proveedor(models.Model):
    id_proveedor = models.BigAutoField(primary_key=True)
    rut_proveedor = models.BigIntegerField()
    dv_proveedor = models.CharField(max_length=1)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column="id_comuna")
    edad = models.BigIntegerField()
    nombre_proveedor = models.CharField(max_length=50)
    apellidom = models.CharField(max_length=50)
    apellidop = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    nombre_tienda = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    id_estado = models.ForeignKey(EstadoCivil, models.DO_NOTHING, db_column="id_estado")
    id_sexo = models.ForeignKey("Sexo", models.DO_NOTHING, db_column="id_sexo")
    correo = models.CharField(max_length=50)
    id_usuario = models.ForeignKey("Usuario", models.DO_NOTHING, db_column="id_usuario")

    class Meta:
        managed = False
        db_table = "proveedor"


class Region(models.Model):
    id_region = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "region"

    def __str__(self):
        return self.descripcion


class Reporte(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=50)
    id_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column="id_compra")

    class Meta:
        managed = False
        db_table = "reporte"


class Sexo(models.Model):
    id_sexo = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "sexo"

    def __str__(self):
        return self.descripcion


class TruequeProveedor(models.Model):
    id_trueque_proveedor = models.BigAutoField(primary_key=True)
    id_otrueque = models.ForeignKey(
        OrdenTrueque, models.DO_NOTHING, db_column="id_otrueque"
    )
    id_proveedor = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "trueque_proveedor"


class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    tipo_perfil = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "usuario"

    def __str__(self):
        return f"{self.tipo_perfil} - {self.username}"
