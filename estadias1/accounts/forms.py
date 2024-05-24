from django import forms
from .models import Categoria, Producto, Cliente, Proveedor

#ESTE ARCHIVO SE UTILIZA PARA LOS FORMULARIOS Y HACER QUE DJANGO HAGA TODO EL TRABAJO AJIJIJI


class ProductoForm(forms.ModelForm):

    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría', to_field_name='descripcion')

    class Meta:
        model = Producto
        fields = ['nombre','id_categoria','costo_venta','stock']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_categoria'].queryset = Categoria.objects.all()


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['rfc','razon_social','uso_factura','regimen_fiscal','codigo_postal']


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor 
        fields = ['id_proveedor','razon_social','direccion','numero_telefono','rfc']