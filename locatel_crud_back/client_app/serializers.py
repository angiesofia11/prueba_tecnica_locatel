# client_app/serializers.py
from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
 

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        extra_kwargs = {
            'venta': {'required': False}  # Permitir omitir 'venta' al crear un detalle
        }

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = '__all__'
        extra_kwargs = {
            'consecutivo': {'required': False},
            'total_venta': {'required': False}
        }

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        
        # Calcular el próximo consecutivo
        ultimo_consecutivo = Venta.objects.all().order_by('consecutivo').last()
        if ultimo_consecutivo:
            consecutivo = ultimo_consecutivo.consecutivo + 1
        else:
            consecutivo = 1
        validated_data['consecutivo'] = consecutivo
        
        # Crear la venta
        venta = Venta.objects.create(**validated_data)
        
        # Calcular total_venta
        total_venta = 0
        for detalle_data in detalles_data:
            detalle_data['venta'] = venta
            total_venta += detalle_data['valor_producto'] + detalle_data['iva_calculado']
            DetalleVenta.objects.create(**detalle_data)
        
        # Actualizar el total_venta en la venta creada
        venta.total_venta = total_venta
        venta.save()
        
        return venta

    def to_representation(self, instance):
        """Customize the returned data to include detalles"""
        representation = super().to_representation(instance)
        detalles = DetalleVentaSerializer(instance.detalleventa_set.all(), many=True).data
        representation['detalles'] = detalles
        return representation
