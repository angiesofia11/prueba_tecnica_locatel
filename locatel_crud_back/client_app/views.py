from django.shortcuts import render

# Create your views here.
# client_app/views.py
from rest_framework import viewsets
from .models import Cliente, Producto, Venta, DetalleVenta
from .serializers import ClienteSerializer, ProductoSerializer, VentaSerializer, DetalleVentaSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente
from .serializers import ClienteSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models 
from .models import Venta, DetalleVenta, Cliente, Producto
import json



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Opcionalmente, también puedes personalizar el método list si quieres que se muestren los detalles de venta en la lista de todas las ventas.
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
@method_decorator(csrf_exempt, name='dispatch')
class VentaView(View):

    def get(self, request, *args, **kwargs):
        try:
            ventas = Venta.objects.all()
            ventas_data = [{'id': venta.id, 'fecha': venta.fecha, 'cliente_id': venta.cliente_id, 'total_venta': venta.total_venta, 'consecutivo': venta.consecutivo} for venta in ventas]
            return JsonResponse({'ventas': ventas_data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            cabecero_data = data.get('cabecero', {})
            cliente_id = cabecero_data.get('cliente_id')
            fecha = cabecero_data.get('fecha')
            total_venta = cabecero_data.get('total_venta')
            max_consecutivo = Venta.objects.aggregate(max_consecutivo=models.Max('consecutivo'))['max_consecutivo']
            if max_consecutivo is None:
                max_consecutivo = 0
            consecutivo = max_consecutivo + 1
            venta = Venta.objects.create(
                fecha=fecha,
                cliente_id=cliente_id,
                total_venta=total_venta,
                consecutivo=consecutivo
            )
            detalles_data = data.get('detalles', [])
            for detalle in detalles_data:
                producto_id = detalle.get('producto')
                valor_producto = detalle.get('valor_producto')
                iva_calculado = detalle.get('iva_calculado')
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_id=producto_id,
                    valor_producto=valor_producto,
                    iva_calculado=iva_calculado
                )
            return JsonResponse({"message": "Venta y detalles guardados exitosamente."}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer