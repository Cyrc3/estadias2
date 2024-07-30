from django import forms
from django.utils import timezone
from .models import Categoria, Producto, Cliente, Proveedor, Detalle_Compra, Detalle_Venta, Usuario, Caja, Cierre_Caja

#ESTE ARCHIVO SE UTILIZA PARA LOS FORMULARIOS Y HACER QUE DJANGO HAGA TODO EL TRABAJO AJIJIJI


class ProductoForm(forms.ModelForm): 
    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría', to_field_name='descripcion')
    punto_reorden = forms.IntegerField(label='Stock Minimo')
    estado = forms.BooleanField(label='¿Activo o Inactivo?', required=False)
    class Meta:
        model = Producto
        fields = ['nombre','id_categoria','stock','costo_venta','costo_compra','porcentaje_utilidad','punto_reorden','estado']
        


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente 
        fields = ['razon_social','codigo_postal']


class UsuarioForm(forms.ModelForm):
    class Meta: 
        model = Usuario
        fields = ['nombre', 'privilegio', 'password']
        widgets = {
            'privilegio': forms.CheckboxInput(),  # Usa un checkbox para valores booleanos
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['privilegio'].label = "¿Es administrador?"




class ProveedorForm(forms.ModelForm):
    
    razon_social = forms.CharField(label='Razón Social')
    direccion = forms.CharField(label='Dirección')
    comunidad = forms.CharField(label='Comunidad')
    estado = forms.CharField(label='Estado')
    municipio = forms.CharField(label='Municipio')
    cp = forms.CharField(label='Código Postal')
    numero_telefono = forms.CharField(label='Número de Teléfono',max_length=13)
    rfc = forms.CharField(label='RFC', max_length=12)
    class Meta:
        model = Proveedor 
        fields = ['id_proveedor','razon_social','direccion','comunidad','estado','municipio','cp','numero_telefono','rfc']



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

class CajaForm(forms.ModelForm):
    id_usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),  # Asegúrate de que esto traiga todos los usuarios.
        label='Usuario',
        required=True,
        to_field_name='id_usuario',  # Esto asegura que el ID se guarde en la base de datos.
    )
    fecha_asignacion = forms.DateField(
        label='Fecha de Asignación',
        required=True,
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Caja
        fields = ['id_usuario', 'mil', 'quinientos', 'doscientos', 'cien', 'cincuenta', 'veinte', 'monedas', 'monto_asignado', 'fecha_asignacion']

    def __init__(self, *args, **kwargs):
        super(CajaForm, self).__init__(*args, **kwargs)
        self.fields['id_usuario'].queryset = Usuario.objects.all()
        self.fields['fecha_asignacion'].initial = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()

        # Obtén los valores de cada denominación
        mil = cleaned_data.get('mil', 0) * 1000
        quinientos = cleaned_data.get('quinientos', 0) * 500
        doscientos = cleaned_data.get('doscientos', 0) * 200
        cien = cleaned_data.get('cien', 0) * 100
        cincuenta = cleaned_data.get('cincuenta', 0) * 50
        veinte = cleaned_data.get('veinte', 0) * 20
        monedas = cleaned_data.get('monedas', 0)  # Suponiendo que este es el total de monedas en valor

        # Calcula la suma total
        total_asignado = mil + quinientos + doscientos + cien + cincuenta + veinte + monedas

        # Asigna el total al campo 'monto_asignado'
        cleaned_data['monto_asignado'] = total_asignado

        return cleaned_data





class CajaForm(forms.ModelForm):
    id_usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),  # Asegúrate de que esto traiga todos los usuarios.
        label='Usuario',
        required=True,
        to_field_name='id_usuario',  # Esto asegura que el ID se guarde en la base de datos.
    )
    fecha_asignacion = forms.DateField(
        label='Fecha de Asignación',
        required=True,
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Caja
        fields = ['id_usuario', 'mil', 'quinientos', 'doscientos', 'cien', 'cincuenta', 'veinte', 'monedas', 'monto_asignado', 'fecha_asignacion']

    def __init__(self, *args, **kwargs):
        super(CajaForm, self).__init__(*args, **kwargs)
        self.fields['id_usuario'].queryset = Usuario.objects.all()
        self.fields['fecha_asignacion'].initial = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()

        # Obtén los valores de cada denominación
        mil = cleaned_data.get('mil', 0) * 1000
        quinientos = cleaned_data.get('quinientos', 0) * 500
        doscientos = cleaned_data.get('doscientos', 0) * 200
        cien = cleaned_data.get('cien', 0) * 100
        cincuenta = cleaned_data.get('cincuenta', 0) * 50
        veinte = cleaned_data.get('veinte', 0) * 20
        monedas = cleaned_data.get('monedas', 0)  # Suponiendo que este es el total de monedas en valor

        # Calcula la suma total
        total_asignado = mil + quinientos + doscientos + cien + cincuenta + veinte + monedas

        # Asigna el total al campo 'monto_asignado'
        cleaned_data['monto_asignado'] = total_asignado

        return cleaned_data



class CierreForm(forms.ModelForm):
    id_caja = forms.ModelChoiceField(
        queryset=Caja.objects.all(),
        label='Caja',
        required=True,
        to_field_name='id_caja',
    )
    fecha_asignacion = forms.DateField(
        label='Fecha de Asignación',
        required=True,
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Cierre_Caja  # Asegúrate de que este sea el modelo correcto
        fields = ['id_caja', 'mil', 'quinientos', 'doscientos', 'cien', 'cincuenta', 'veinte', 'monedas', 'total_suma', 'total_diferencia', 'fecha_asignacion']

    def __init__(self, *args, **kwargs):
        super(CierreForm, self).__init__(*args, **kwargs)
        self.fields['id_caja'].queryset = Caja.objects.all()
        self.fields['fecha_asignacion'].initial = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()

        # Obtén los valores de cada denominación
        mil = cleaned_data.get('mil', 0) * 1000
        quinientos = cleaned_data.get('quinientos', 0) * 500
        doscientos = cleaned_data.get('doscientos', 0) * 200
        cien = cleaned_data.get('cien', 0) * 100
        cincuenta = cleaned_data.get('cincuenta', 0) * 50
        veinte = cleaned_data.get('veinte', 0) * 20
        monedas = cleaned_data.get('monedas', 0)  # Suponiendo que este es el total de monedas en valor

        # Calcula la suma total
        total_suma = mil + quinientos + doscientos + cien + cincuenta + veinte + monedas
        cleaned_data['total_suma'] = total_suma

        # Obtener el valor de la otra tabla
        id_caja_obj = cleaned_data.get('id_caja')
        id_caja = id_caja_obj.id_caja if id_caja_obj else None
        try:
            monto_asignado = Caja.objects.get(id_caja=id_caja).monto_asignado  # Ajusta esto según tu modelo
        except Caja.DoesNotExist:
            raise ValidationError("No se encontró la caja con el ID especificado.")



        # Calcula la diferencia
        total_diferencia = total_suma - monto_asignado
        cleaned_data['total_diferencia'] = total_diferencia

        return cleaned_data
        cleaned_data = super().clean()

        # Obtén los valores de cada denominación
        mil = cleaned_data.get('mil', 0) * 1000
        quinientos = cleaned_data.get('quinientos', 0) * 500
        doscientos = cleaned_data.get('doscientos', 0) * 200
        cien = cleaned_data.get('cien', 0) * 100
        cincuenta = cleaned_data.get('cincuenta', 0) * 50
        veinte = cleaned_data.get('veinte', 0) * 20
        monedas = cleaned_data.get('monedas', 0)  # Suponiendo que este es el total de monedas en valor

        # Calcula la suma total
        total_suma = mil + quinientos + doscientos + cien + cincuenta + veinte + monedas
        cleaned_data['total_suma'] = total_suma

        # Obtener el valor de la otra tabla
        #from .models import Caja 
        id_caja = cleaned_data.get('id_caja')
        try:
            monto_asignado = Caja.objects.get(id_caja=id_caja).valor_numerico  # Ajusta esto según tu modelo
        except Caja.DoesNotExist:
            monto_asignado = 0  # Maneja el caso donde no existe el valor en la otra tabla

        # Calcula la diferencia
        total_diferencia = total_suma - valor_otro
        cleaned_data['total_diferencia'] = total_diferencia

        return cleaned_data