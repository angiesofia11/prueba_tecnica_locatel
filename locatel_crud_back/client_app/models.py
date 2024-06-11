from django.db import models

# Create your models here.

class Cliente(models.Model):
    cedula = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    valor_venta = models.DecimalField(max_digits=10, decimal_places=2)
    maneja_iva = models.BooleanField(default=False)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre

    
class Venta(models.Model):
    consecutivo = models.IntegerField(unique=True, blank=True, null=True)  # Permitir null y blank
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Permitir null y blank

    def __str__(self):
        return f'Venta {self.consecutivo}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor_producto = models.DecimalField(max_digits=10, decimal_places=2)
    iva_calculado = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} - {self.venta.consecutivo}'