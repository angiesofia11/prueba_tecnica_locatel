"""
URL configuration for locatel_crud_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from client_app import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'productos', views.ProductoViewSet)
# router.register(r'ventas', views.VentaView)
router.register(r'detalleventas', views.DetalleVentaViewSet)

urlpatterns = [
    
    path('api/ventas/', views.VentaView.as_view(), name='ventas'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]






