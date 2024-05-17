from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Compra
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
        nuevo_cliente = Cliente()
        nuevo_cliente.razon_social = request.POST.get('nombre')
        nuevo_cliente.rfc = request.POST.get('rfc')
        nuevo_cliente.regimen_fiscal = request.POST.get('regimen_fiscal')
        nuevo_cliente.uso_factura = request.POST.get('uso_factura')
        nuevo_cliente.codigo_postal = request.POST.get('codigo_postal')
        nuevo_cliente.save()
        return render(request, 'menu_principal.html')
    else:
        return render(request, 'registro_cliente.html')
    

def registrar_proveedor(request):
    if request.method == 'POST' :
        nuevo_proveedor = Proveedor()
        nuevo_proveedor.razon_social = request.POST.get('razon_social')
        nuevo_proveedor.direccion = request.POST.get('direccion')
        nuevo_proveedor.numero_telefono = request.POST.get('telefono')
        nuevo_proveedor.rfc = request.POST.get('rfc')
        nuevo_proveedor.save()
        return render(request, 'menu_principal.html')
    else:
        return render(request,'registro_proveedor.html') 
    

def registrar_producto(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nuevo_producto = Producto()
        nuevo_producto.nombre = request.POST.get('nombre')
        nuevo_producto.stock = request.POST.get('stock')
        nuevo_producto.costo_venta = request.POST.get('costo_venta')
        id_categoria = int(request.POST.get('id_categoria'))
        if id_categoria and id_categoria != '0': 
            categoria = Categoria.objects.get(id_categoria=id_categoria)
            nuevo_producto.id_categoria = categoria.id_categoria
            nuevo_producto.save()
            return redirect('menu_principal')
    messages.error(request, 'Por favor, selecciona una categoría.')
    return render(request, 'registro_inventario.html', {'categorias': categorias})


def registrar_categoria(request):
    if request.method == 'POST':
        nueva_categoria = Categoria()
        nueva_categoria.descripcion = request.POST.get('id_categoria')
        nueva_categoria.descripcion = request.POST.get('descripcion')
        nueva_categoria.save()
        return redirect('menu_principal')
    return render(request, 'registro_categoria.html')


def registrar_compra(request):
    if request.method == 'POST':
        nueva_compra = Compra()
        nueva_compra.id_compra = request.POST.get('id_compra')
        nueva_compra.cantidad = request.POST.get('cantidad')
        id_proveedor = int(request.POST.get('proveedor'))
        if id_proveedor != '0':
            proveedor = Proveedor.objects.get(id_proveedor = id_proveedor)
            nueva_compra.id_proveedor = proveedor.id_proveedor
        
        id_producto = int(request.POST.get('producto'))
        if id_producto != '0':
            producto = Producto.objects.get(id_producto = id_producto)
            nueva_compra.id_producto = producto.id_producto

            nueva_compra.save()
            return redirect('menu_principal')
        


def historico_compras(request):
    return render(request, 'menu_principal.html')

def historico_ventas(request):
    return render(request, 'menu_principal.html')