from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Detalle_Compra, Detalle_Venta, Compra, Venta
from .forms import ProductoForm, ClienteForm, ProveedorForm, CompraForm, VentaForm
from django.http import HttpResponse
from django_select2.views import AutoResponseView
from .db_conection import Database #conexión directa
import json



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
            return redirect('proveedor')
        else:
            messages.error(request, "Hubo un error al registrar el proveedor.")
    else:
        form = ProveedorForm()
    proveedores = Proveedor.objects.all()
    return render(request, 'registro_proveedor.html', {'form':form, 'proveedores':proveedores})
    

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
    productos = Producto.objects.all()
    return render(request, 'registro_inventario.html', {'form':form, 'productos':productos})


def registrar_categoria(request):
    if request.method == 'POST':
        nueva_categoria = Categoria()
        nueva_categoria.descripcion = request.POST.get('descripcion')
        nueva_categoria.save()
        return redirect('producto')
        
    return render(request, 'registro_categoria.html')


def registrar_compra(request):
    if request.method == 'POST': 
        form = CompraForm(request.POST)
        if form.is_valid() or not form.has_changed():
            try:
                fecha_compra = request.POST.get('fecha_compra')
                total_compra = request.POST.get('total_compra')
                resumen_data = json.loads(request.POST.get('resumen_data', '[]'))

                # Crear nueva compra
                nueva_compra = Compra(fecha=fecha_compra, total=total_compra)
                nueva_compra.save()

                #insertar detalles de la compra
                for item in resumen_data:
                    proveedor =  Proveedor.objects.get(id_proveedor=item['proveedor_id'])
                    producto = Producto.objects.get(id_producto=item['producto_id'])
                    cantidad = item['cantidad']
                    costo = item['costo']
                    detalle_compra = Detalle_Compra(
                        id_compra=nueva_compra,
                        id_proveedor=proveedor,
                        id_producto=producto,
                        cantidad=cantidad,
                        costo=costo
                    )
                    detalle_compra.save()
                    #actualización del stock
                    producto.stock += int(cantidad)
                    producto.save()
                    
                return redirect('compra')
            except Exception as e:
                print(f"Error al guardar la compra: {e}")

        else:
            print("El formulario no es válido")
    else:
        form=CompraForm()
    return render(request, 'registro_compra.html', {'form':form})  



def registro_ventas(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        try:
            if form.is_valid():
                fecha_venta = form.cleaned_data['fecha_venta']
                total_venta = form.cleaned_data['total_venta']
                resumen_data = json.loads(request.POST.get('resumen_data', '[]'))
                
                nueva_venta = Venta(fecha=fecha_venta, total=total_venta)
                nueva_venta.save()
                
                for item in resumen_data:
                    cliente = item.get('cliente')
                    cantidad = item.get('cantidad')
                    precio_total = item.get('precio_total')

                    detalle_venta = Detalle_Venta(
                        id_venta=nueva_venta,
                        rfc=cliente,
                        cantidad=cantidad,
                        precio_total=precio_total
                    )
                    detalle_venta.save()
                
                return redirect('venta')
        except Exception as e:
            print(f"Error sabrá Dios dónde: {e}")
            
    else:
        form = VentaForm()
    
    return render(request, 'registro_venta.html', {'form': form})


def historico_compras(request):
    db = Database()
    try:
        query="""
        SELECT dc.id_detallecompra, dc.id_compra, c.fecha, p.nombre, dc.cantidad, dc.costo
        FROM Detalle_Compra dc
        JOIN Compra c ON dc.id_compra = c.id_compra JOIN Producto p ON p.id_producto=dc.id_producto
        """
        historial_compras = db.fetch_all(query)
        
        #calculando el total
        total = sum(compra[4]*compra[5] for compra in historial_compras)
        context = {
            'historial_compras': historial_compras,
            'total': total,
        }
    finally:
        db.close()
    return render(request, 'historico_compras.html',context)



def historico_ventas(request):
    return render(request, 'historico_ventas.html')


#TEST PARA LA CONEXION DIRECTA A LA BD !!--11--1--121-01|0|020|920|93UR84U2RY2U3
'''
def test_db_view(request):
    db = Database()
    try:
        #probando para insertar --se insertara un cliente 
        insert_query = "INSERT INTO cliente (RFC, razon_social, USO_FACTURA, REGIMEN_FISCAL, CODIGO_POSTAL) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(insert_query,('GGGGGGGGGGGGG','CALAMARDO','SEPA','noce',76800))

        #verificando la inserciónn
        select_query = "SELECT * FROM cliente WHERE RFC= %s"
        resultados = db.fetch_all(select_query,('GGGGGGGGGGGGG'))

        resultado_str = "<br>".join([str(fila) for fila in resultados])
        return HttpResponse(f"Inserción exitosa.<br>Resultados obtenidos:<br>{resultado_str}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
    finally:
        db.close()'''