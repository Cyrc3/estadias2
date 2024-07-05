from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Detalle_Compra, Detalle_Venta, Compra, Venta
from .forms import ProductoForm, ClienteForm, ProveedorForm, CompraForm, VentaForm, UsuarioForm
from django.http import HttpResponse
from django_select2.views import AutoResponseView
from .db_conection import Database #conexión directa
import json
#from .forms import ProductoForm
from django.contrib import messages





def menu_principal(request):
    
    return render(request, 'menu_principal.html')


def index(request):
    return render(request,'index.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('usuario')
        else:
            messages.error(request, "Hubo un error al registrar el usuario.")
    else:
        form = UsuarioForm()
    return render(request, 'usuario.html', {'form':form})


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
    query = request.GET.get('q','')
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
    #filtrar productos segun la busqueda
    if query:
        productos_filtrados = productos.filter(id_producto=query)
    else:
        productos_filtrados = productos
    return render(request, 'registro_inventario.html', {'form':form, 'productos':productos,'productos_filtrados':productos_filtrados,'query':query})


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
                proveedor_id = request.POST.get('proveedor_id')
                resumen_data = json.loads(request.POST.get('resumen_data', '[]'))

                # Crear nueva compra
                nueva_compra = Compra(fecha=fecha_compra, total=total_compra)
                nueva_compra.save()
                
                #obtener el proveedor 
                proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)

                #insertar detalles de la compra
                for item in resumen_data:
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
        if form.is_valid() or not form.has_changed():
            try:

                fecha_venta = request.POST.get('fecha_venta')
                total_venta = request.POST.get('total_venta')
                resumen_data = json.loads(request.POST.get('resumen_data', '[]'))
                    
                nueva_venta = Venta(fecha=fecha_venta, total=total_venta)
                nueva_venta.save()

                for item in resumen_data:
                    id_cliente = item.get('id_cliente')
                    cantidad = item.get('cantidad')
                    producto_id = item.get('producto_id')
                    precio_total = float(item.get('precio_total'))
                    precio_base = precio_total / (1 + 0.16)
                    iva = precio_total - precio_base
    

                    detalle_venta = Detalle_Venta(
                        id_venta1=nueva_venta,  # Aquí el campo en la tabla es 'id_venta1'
                        id_producto=Producto.objects.get(id_producto=producto_id),  # Obtener instancia del producto
                        cantidad=cantidad,
                        precio_total=precio_total,
                        id_cliente=Cliente.objects.get(id_cliente=id_cliente),  # Obtener instancia del cliente
                        
                    )
                    detalle_venta.save()

                return redirect('venta')
            except Exception as e:
                print(f"Error sabrá Dios dónde: {e}")
        else:
            print("El formulario no es válido")
    else:
        form = VentaForm()

    return render(request, 'registro_venta.html', {'form': form})


def historico_compras(request):
    db = Database()
    try:
        #datos del filtro
        producto_id = request.GET.get('producto')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        #consulta con filtros
        query = """
        SELECT dc.id_detallecompra, dc.id_compra, c.fecha, pr.razon_social, p.nombre, dc.cantidad, dc.costo
        FROM Detalle_Compra dc
        JOIN Compra c ON dc.id_compra = c.id_compra 
        JOIN Producto p ON p.id_producto = dc.id_producto
        JOIN Proveedor pr ON pr.id_proveedor = dc.id_proveedor
        WHERE 1=1
        """

        #añadir filtros a la consulta
        params = []
        if producto_id:
            query += " AND p.id_producto = %s"
            params.append(producto_id)
        if fecha_inicio:
            query += " AND c.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND c.fecha <= %s"
            params.append(fecha_fin)

        query += " ORDER BY dc.id_detallecompra ASC"
        historial_compras = db.fetch_all(query, params)

        #calculando el total
        total = sum(compra[5] * compra[6] for compra in historial_compras)

        #obtener la lista de productos para el filtro de productos
        productos_query = "SELECT id_producto, nombre FROM Producto"
        productos = db.fetch_all(productos_query, [])

        productos_dict = [{'id_producto': producto[0], 'nombre': producto[1]} for producto in productos]

        context = {
            'historial_compras': historial_compras,
            'total': total,
            'productos': productos_dict
        }
    finally:
        db.close()
    return render(request, 'historico_compras.html', context)



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