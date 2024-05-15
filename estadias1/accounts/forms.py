from django import forms
from .models import Categoria, Producto

#ESTE ARCHIVO POR AHORA SE ESTA UTILIZANDO PARA LOS FORMULARIOS QUE REQUIEREN CONSULTAS
#


class ProductoForm(forms.ModelForm):
    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),to_field_name='id')

    class Meta:
        model = Producto
        fields = ['stock','nombre','costo_venta','id_categoria']