# Generated by Django 5.0.6 on 2024-06-10 03:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('valor_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('maneja_iva', models.BooleanField(default=False)),
                ('porcentaje_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutivo', models.IntegerField(unique=True)),
                ('fecha', models.DateField()),
                ('total_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_app.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('iva_calculado', models.DecimalField(decimal_places=2, max_digits=5)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_app.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_app.venta')),
            ],
        ),
    ]
