# Generated by Django 4.2.7 on 2023-12-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crud", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("id_producto", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=50)),
                ("descripcion", models.CharField(max_length=50)),
                ("tipo_producto", models.CharField(max_length=50)),
                ("precio", models.BigIntegerField()),
                ("stock", models.BigIntegerField()),
                (
                    "imagen",
                    models.ImageField(blank=True, null=True, upload_to="productos/"),
                ),
            ],
            options={
                "db_table": "producto",
                "managed": False,
            },
        ),
    ]
