from django import forms
from .models import Categoria, Producto, Cliente, Proveedor, Detalle_Compra, Detalle_Venta

#ESTE ARCHIVO SE UTILIZA PARA LOS FORMULARIOS Y HACER QUE DJANGO HAGA TODO EL TRABAJO AJIJIJI


class ProductoForm(forms.ModelForm):
    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría', to_field_name='descripcion')
    id_proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), label='Proveedor', to_field_name='razon_social')
    class Meta:
        model = Producto
        fields = ['nombre','id_proveedor','id_categoria','costo_venta','stock']
        


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rfc','razon_social','uso_factura','regimen_fiscal','codigo_postal']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor 
        fields = ['id_proveedor','razon_social','direccion','numero_telefono','rfc']



class CompraForm(forms.ModelForm):

    id_proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(),label='Proveedor', to_field_name='razon_social')

    id_producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto',to_field_name='nombre')

    costo = forms.FloatField(label='Costo Individual')
    class Meta:
        model = Detalle_Compra
        fields = ['id_proveedor','id_producto','cantidad','costo']



class VentaForm(forms.ModelForm):
    id_producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto',to_field_name='nombre')
    rfc = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='rfc', to_field_name='rfc')

    class Meta:
        model = Detalle_Venta
        fields = ['id_producto','cantidad','precio_total','rfc']
  