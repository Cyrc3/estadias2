from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Detalle_Compra
from .forms import ProductoForm, ClienteForm, ProveedorForm
from django.http import HttpResponse

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


#def registro_compra(request):
#    if request.method == 'POST':
#        nueva_compra



def index(request):
    return render(request,'index.html')

def registro_ventas(request):
    return render(request,'registro_venta.html')

#def render_cliente(View):
#    return render(request, 'registro_cliente.html')
 
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
            return redirect('menu_principal')
        else:
            messages.error(request, "Hubo un error al registrar el producto.")
    else:
        form = ProductoForm()
    return render(request, 'registro_inventario.html', {'form':form})


def registrar_categoria(request):
    if request.method == 'POST':
        nueva_categoria = Categoria()
        nueva_categoria.id_categoria = request.POST.get('id_categoria')
        nueva_categoria.descripcion = request.POST.get('descripcion')
        nueva_categoria.save()
        return redirect('producto')
        
    return render(request, 'registro_categoria.html')


def registrar_compra(request):
    proveedores = Proveedor.objects.all()    
    productos = Producto.objects.all()
    if request.method == 'POST': 
        nueva_compra = Detalle_Compra()
        #nueva_compra.id_compra = request.POST.get('id_compra')
        nueva_compra.cantidad = request.POST.get('cantidad')
        id_proveedor = int(request.POST.get('id_proveedor'))
        id_producto = int(request.POST.get('id_producto'))
        if id_proveedor and id_proveedor != '0' and id_producto and id_producto != '0':
            proveedor = Proveedor.objects.get(id_proveedor = id_proveedor)
            producto = Producto.objects.get(id_producto = id_producto)
            nueva_compra.id_proveedor = proveedor.id_proveedor
            nueva_compra.id_producto = producto.id_producto
            #nueva_compra.save()

    else:
         return render(request, 'registro_compra.html', {'proveedores': proveedores, 'productos' : productos})   



def historico_compras(request):
    return render(request, 'historico_compras.html')




def historico_ventas(request):
    return render(request, 'historico_ventas.html')

