from django import forms
from .models import Categoria, Producto, Cliente, Proveedor, Detalle_Compra, Detalle_Venta, Usuario

#ESTE ARCHIVO SE UTILIZA PARA LOS FORMULARIOS Y HACER QUE DJANGO HAGA TODO EL TRABAJO AJIJIJI


class ProductoForm(forms.ModelForm): 
    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría', to_field_name='descripcion')
    punto_reorden = forms.IntegerField(label='Stock Minimo')
    class Meta:
        model = Producto
        fields = ['nombre','id_categoria','stock','costo_venta','costo_compra','porcentaje_utilidad','punto_reorden']
        


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente 
        fields = ['rfc','razon_social','uso_factura','regimen_fiscal','codigo_postal']


class UsuarioForm(forms.ModelForm):
    class Meta: 
        model = Usuario
        fields = ['nombre','privilegio','password'] 


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor 
        fields = ['id_proveedor','razon_social','direccion','numero_telefono','rfc']



class CompraForm(forms.ModelForm):

    id_proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(),label='Proveedor', required=False)

    id_producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto', required=False)

    cantidad = forms.IntegerField(required=False)

    costo = forms.FloatField(label='Costo Individual', required=False)
    class Meta:
        model = Detalle_Compra
        fields = ['id_proveedor','id_producto','cantidad','costo']

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields['id_proveedor'].queryset = Proveedor.objects.all()
        self.fields['id_producto'].queryset = Producto.objects.all()


class VentaForm(forms.ModelForm):
    id_producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto', required=False)
    id_cantidad = forms.IntegerField(label='Cantidad', required=False)
    #costo = forms.FloatField(label='Costo Individual', required=False)
    precio_total = forms.FloatField(label='Costo Individual', required=False)
    #id_venta1 not defined cs don't get how to link this (detalle_venta) with Venta xd
    #iva = forms.FloatField(label='IVA'
    #fecha_venta = forms.DateField(label='fecha')
    id_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente', required=False)

    class Meta:
        model = Detalle_Venta
        fields = ['id_producto','id_cantidad','id_cliente', 'precio_total']
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['id_producto'].queryset = Producto.objects.all()
        self.fields['id_cliente'].queryset = Cliente.objects.all()


