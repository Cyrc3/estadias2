"""estadias1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='index.html'), name = 'login'),
    path('registro_venta/',views.registro_ventas,name="ventas"),
    path('registrar_clientes/',views.registrar_cliente,name='cliente'),
    path('registrar_proveedor/',views.registrar_proveedor,name='proveedor'),
    path('registrar_inventario/',views.registrar_producto,name='producto'),
    path('menu_principal/', views.menu_principal, name='menu_principal'),
    path('registro_compra/', views.menu_principal, name='compra'),
    path('historico_compras/', views.menu_principal, name='historicoCompras'),
    path('historico_ventas/', views.menu_principal, name='historicoVentas'),
    path('registro_categoria/', views.menu_principal, name='altaCategoria'),

    


]

