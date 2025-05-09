from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Detalle_Compra, Detalle_Venta
from .forms import ProductoForm, ClienteForm, ProveedorForm, CompraForm, VentaForm
from django.http import HttpResponse
from django_select2.views import AutoResponseView


#from .forms import ProductoForm
from django.contrib import messages

def loginFun(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir a la página deseada después del inicio de sesión
                return redirect('../estadias1/views/menu_principal.html')
    else:
        form = AuthenticationForm()
    return render(request, '../estadias1/views/index.html', {'form': form})


def menu_principal(request):
    
    return render(request, 'menu_principal.html')

def index(request):
    return render(request,'index.html')



def registrar_cliente(request):
    if request.method == 'POST' :
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_principal')
        else:
            messages.error(request, "Hubo un error al registrar el cliente.")
    else:
        form = ClienteForm()
    return render(request, 'registro_cliente.html', {'form':form})
    

def registrar_proveedor(request):
    if request.method == 'POST' :
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'menu_principal.html')
        else:
            messages.error(request, "Hubo un error al registrar el proveedor.")
    else:
        form = ProveedorForm()
    return render(request, 'registro_proveedor.html', {'form':form})
    

def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto')
        else:
            messages.error(request, "Hubo un error al registrar el producto.")
    else:
        form = ProductoForm()
    return render(request, 'registro_inventario.html', {'form':form})
    #return render(request, 'registro_venta.html', {'form':form})



def registrar_categoria(request):
    if request.method == 'POST':
        nueva_categoria = Categoria()
        nueva_categoria.id_categoria = request.POST.get('id_categoria')
        nueva_categoria.descripcion = request.POST.get('descripcion')
        nueva_categoria.save()
        return redirect('producto')
        
    return render(request, 'registro_categoria.html')


def registrar_compra(request):
    if request.method == 'POST': 
        form = CompraForm(request.POST)
    else:
        form=CompraForm()
    return render(request, 'registro_compra.html', {'form':form})  
 

def registro_ventas(request):
    if request.method == 'POST':
        nueva_venta = Detalle_Venta()
        nueva_venta.id_detalleventa = request.POST.get('id_detalleventa')
        nueva_venta.id_producto = request.POST.get('id_producto')
        nueva_venta.cantidad = request.POST.get('cantidad')
        nueva_venta.precio_total = request.POST.get('precio_total')
        nueva_venta.id_venta1 = request.POST.get('id_venta1')
        nueva_venta.iva = request.POST.get('iva')
        nueva_venta.rfc = request.POST.get('rfc')
        nueva_venta.save()
        return redirect('venta')
        
    return render(request, 'registro_venta.html')




def historico_compras(request):
    return render(request, 'historico_compras.html')




def historico_ventas(request):
    return render(request, 'historico_ventas.html')


class ProveedorSelect2View(AutoResponseView):
    def get_queryset(self):
        qs = Proveedor.objects.all()
        # Puedes aplicar filtros o cualquier lógica adicional aquí
        return qs
    def get_result_value(self, result):
        # Define cómo se devuelve el valor de cada resultado
        return result.id_proveedor

    def get_result_label(self, result):
        # Define cómo se muestra la etiqueta de cada resultado
        return str(result.razon_social)