from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Proveedor, Categoria, Producto, Detalle_Compra, Detalle_Venta, Compra, Venta
from .forms import ProductoForm, ClienteForm, ProveedorForm, CompraForm, VentaForm, UsuarioForm
from django.http import HttpResponse
from django_select2.views import AutoResponseView
from .db_connection import Database #conexión directa
import json
from decimal import Decimal

#from .forms import ProductoForm
from django.contrib import messages

#shit for test, do not fokin delit

import os
import django
import escpos
import PIL.Image
from django.utils import timezone
from accounts.models import Detalle_Venta, Venta





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
    query = request.GET.get('q', '')
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id', None)
        if producto_id:  # Si hay un ID, estamos actualizando un producto existente
            producto = get_object_or_404(Producto, id_producto=producto_id)
            form = ProductoForm(request.POST, instance=producto)
        else:  # Si no hay ID, estamos creando un nuevo producto
            form = ProductoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado exitosamente.")
            return redirect('producto')
        else:
            messages.error(request, "Hubo un error al registrar el producto.")
    else:
        form = ProductoForm()
    
    productos = Producto.objects.all()
    if query:
        productos_filtrados = productos.filter(id_producto=query)
    else:
        productos_filtrados = productos
    
    return render(request, 'registro_inventario.html', {
        'form': form,
        'productos': productos,
        'productos_filtrados': productos_filtrados,
        'query': query
    })


def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('producto')



def registrar_categoria(request):
    if request.method == 'POST':
        nueva_categoria = Categoria()
        nueva_categoria.descripcion = request.POST.get('descripcion')
        nueva_categoria.save()
        return redirect('producto')
        
    return render(request, 'registro_categoria.html')


def registrar_compra(request):
    productos = Producto.objects.all()
    if request.method == 'POST': 
        form = CompraForm(request.POST)
        if form.is_valid() or not form.has_changed():
            try:
                fecha_compra = request.POST.get('fecha_compra')
                total_compra = Decimal(request.POST.get('total_compra'))
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
                    cantidad = int(item['cantidad'])
                    costo = Decimal(item['costo'])

                    #calculazion de utilidad
                    porcentaje_utilidad = Decimal(producto.porcentaje_utilidad)
                    utilidad = costo * (porcentaje_utilidad/100)
                    precio_venta = costo + utilidad

                    #actualizar producto
                    #actualizar el precio de venta
                    producto.costo_venta = precio_venta
                    
                    #actualizar el costo de venta del producto
                    producto.costo_compra = costo

                    if isinstance(producto.stock,int) :
                        producto.stock += int(cantidad)
                    else :
                        producto.stock = int(cantidad)
                    producto.save()

                    detalle_compra = Detalle_Compra(
                        id_compra=nueva_compra,
                        id_proveedor=proveedor,
                        id_producto=producto,
                        cantidad=cantidad,
                        costo=costo 
                    )
                    detalle_compra.save()
                    #actualización del stock
                return redirect('compra')
            except Exception as e:
                print(f"Error al guardar la compra: {e}")

        else:
            print("El formulario no es válido")
    else:
        form=CompraForm()
    context = {
        'form': form,
        'productos': productos
    }
    return render(request, 'registro_compra.html', context)  



def registro_ventas(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid() or not form.has_changed():
            try:

                fecha_venta = request.POST.get('fecha_venta')       
                total_venta = request.POST.get('total_venta')
                cliente_id = request.POST.get('cliente_id')
                resumen_data = json.loads(request.POST.get('resumen_data', '[]'))
                    
                nueva_venta = Venta(fecha=fecha_venta, total=total_venta)
                nueva_venta.save()

                cliente = Cliente.objects.get(id_cliente=cliente_id)

                for item in resumen_data:
                    #id_cliente = Cliente.objects.get(id_cliente=item['id_cliente'])
                    cantidad = int(item.get('cantidad'))
                    producto_id = Producto.objects.get(id_producto=item['producto_id'])
                    precio_total = float(item.get('precio_total'))
                    precio_base = precio_total / 1.16
                    iva = precio_total - precio_base

                    #descontar stock
                    producto_id.stock -= int(cantidad)
                    producto_id.save()

                    detalle_venta = Detalle_Venta(
                        id_venta1=nueva_venta,  # Aquí el campo en la tabla es 'id_venta1'
                        id_producto=producto_id,  # Obtener instancia del producto
                        cantidad=cantidad,
                        precio_total=precio_base,
                        id_cliente=cliente,  # Obtener instancia del cliente
                        iva=iva,
                        
                    )
                    detalle_venta.save()

                return redirect('venta')
            except Exception as e:
                print(f"Error sabrá Dios dónde: {e}")
        else:
            print("El formulario no es válido")
    else:
        form = VentaForm()
    context = {
        'form': form,
        'productos': productos
    }
    return render(request, 'registro_venta.html', context)

def ticket_generator(request):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../estadias1/settings')
    django.setup()
    printer = escpos.printer.SerialPrinter(port='/dev/ttyUSB0', baudrate=9600)
    #The fokin config of the printer MUST be defined in the previous line.
    #test's haven't been, you know, tested xd
    printer.write('**Electronic Store UTSJR or something**')
    now = timezone.now()
    printer.write(f'Fecha: {now.strftime("%Y-%m-%d")}')
    printer.write(f'Hora: {now.strftime("%H:%M:%S")}')
    detalles = Detalle_Venta.objects.all()
    

    #get the last Detalle_Venta
    ultimo_detalle = Detalle_Venta.objects.latest('id_detalleventa')

    #get the last detalle_venta1 to use it as a reference
    id_venta1 = ultimo_detalle.id_venta1_id 

    #Get the things inside detalle_ventas, not VENTAS, DETALLE you filthy fucker
    detalles = Detalle_Venta.objects.filter(id_venta1=id_venta1).order_by('-id_detalleventa')

    #get the VENTA, not de DETALLE,the VENTA, based on the asociated VENTA1 id in detalle
    #kinda confusing but not so bad my dude
    venta = Venta.objects.get(id_venta=id_venta1)

    #header of tha shi
    printer.write('**Electronic Store UTSJR or whatever**\n')
    now = timezone.now()
    printer.write(f'Date: {now.strftime("%Y-%m-%d")}\n')
    printer.write(f'Time: {now.strftime("%H:%M:%S")}\n')

    #Sell data
    printer.write(f"Sell number: {ultimo_detalle.id_detalleventa}\n")
    #printer.write(f"Cliente: {ultimo_detalle.id_cliente}")
    #printer.write(f"Fecha de Venta: {venta.fecha}")
    #printer.write("Products:")
    printer.write("Cantidad     |Costo         |Total\n")

    #pradacts
    for detalle in detalles:
        cantidad = detalle.cantidad
        individualPrice = detalle.precio_total
        total_articulo = cantidad * precio_total
        printer.write(f"{detalle.id_producto}\n")
        printer.write(f"{detalle.cantidad}    ")
        printer.write(f"{detalle.precio_total}    ")
        printer.write(f"{individualPrice}\n")        
        #printer.write(f"IVA: {detalle.iva}")
        printer.write('---------------------\n')
    #Total
    printer.write(f"Total de la Venta: {venta.total}")


    printer.cut()
# Further tests haven't been applied because, you know, we need a printer
# if this doesn't work you have below this message the original generator
# it generates ugly tickets in PDF but at least that fucking works
# That's it for today, i have an urgent call to buy an hamburguer cs i'm hungry as fuck
# -fakeCirc3



'''
def ticket_generator(request):
    # Generar la respuesta HTTP con el contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="detalle_venta.pdf"'

    # Crear un objeto canvas de ReportLab
    p = canvas.Canvas(response)

    # Obtener el último detalle de venta según id_detalleventa
    ultimo_detalle = Detalle_Venta.objects.latest('id_detalleventa')

    # Obtener el id_venta1 del último detalle de venta
    id_venta1 = ultimo_detalle.id_venta1_id  # Acceder al id de la venta

    # Obtener todos los detalles de venta para el id_venta1 obtenido, manteniendo el último id_detalleventa
    detalles = Detalle_Venta.objects.filter(id_venta1=id_venta1).order_by('-id_detalleventa')

    # Obtener la venta asociada al id_venta1
    venta = Venta.objects.get(id_venta=id_venta1)

    # Inicializar posición de escritura
    y = 800

    # Escribir los datos del último detalle de venta y productos asociados en el PDF
    p.drawString(100, y, f"ID Venta: {ultimo_detalle.id_detalleventa}")
    p.drawString(100, y - 20, f"Cliente: {ultimo_detalle.id_cliente}")
    p.drawString(100, y - 40, f"Fecha de Venta: {venta.fecha}")
    p.drawString(100, y - 60, "Productos:")

    # Listar todos los productos asociados al id_venta1 y último id_detalleventa
    for detalle in detalles:
        p.drawString(120, y - 80, f"Producto: {detalle.id_producto}, Cantidad: {detalle.cantidad}, Costo: {detalle.precio_total}, IVA: {detalle.iva}")
        y -= 40  # Mover hacia abajo para el siguiente detalle

    # Mostrar el total de la venta
    p.drawString(100, y - 100, f"Total de la Venta: {venta.total}")

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response
'''

def historico_compras(request):
    db = Database()
    try:
        #datos del filtro
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        #consulta con filtros
        query = """
        SELECT c.id_compra, c.fecha, pr.razon_social, c.total
        FROM compra c
        JOIN detalle_compra dc ON c.id_compra = dc.id_compra 
        JOIN proveedor pr ON pr.id_proveedor = dc.id_proveedor
        WHERE 1=1
        
        """

        #añadir filtros a la consulta
        params = []
        if fecha_inicio:
            query += " AND c.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND c.fecha <= %s"
            params.append(fecha_fin)

        query += """
        group by c.id_compra,pr.razon_social
        order by c.id_compra desc
        """
        historial_compras = db.fetch_all(query, params)
        total = sum(compra[3] for compra in historial_compras)

        context = {
            'historial_compras': historial_compras,
            'total' : total
        }
    finally:
        db.close()
    return render(request, 'historico_compras.html', context)


def detalle_compra(request): #EXTENSION DEL HISTORICO DE COMPRA PARA VER EL DETALLE DE LA COMPRA SJSJ
    compra_id = request.GET.get('compra_id')
    db = Database()
    try:
        query = """
        SELECT dc.id_detallecompra, p.nombre, dc.cantidad, dc.costo, (dc.cantidad * dc.costo) as total
        FROM detalle_compra dc
        JOIN producto p ON p.id_producto = dc.id_producto
        WHERE dc.id_compra = %s
        """
        detalles_compra = db.fetch_all(query, [compra_id])

        total = sum(detalle[4] for detalle in detalles_compra)

        context = {
            'detalles_compra':detalles_compra,
            'total':total
        }
    finally:
        db.close()

    return render(request, 'detalle_compra.html', context)



def historico_ventas(request):
    db = Database()
    try:
        #datos del filtro
        producto_id = request.GET.get('producto')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        #consulta con filtros
        query = """
        SELECT dv.id_detalleventa, dv.id_venta1, v.fecha, cl.razon_social, p.nombre, dv.cantidad, dv.precio_total, dv.iva
        FROM detalle_venta dv
        JOIN venta v ON dv.id_venta1 = v.id_venta 
        JOIN producto p ON p.id_producto = dv.id_producto
        JOIN cliente cl ON cl.id_cliente = dv.id_cliente
        WHERE 1=1
        """

        #añadir filtros a la consulta
        params = []
        if producto_id:
            query += " AND p.id_producto = %s"
            params.append(producto_id)
        if fecha_inicio:
            query += " AND v.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND v.fecha <= %s"
            params.append(fecha_fin)

        query += " ORDER BY dv.id_detalleventa ASC"
        historial_ventas = db.fetch_all(query, params)

        #calculando el total
        total = sum(venta[5] * (venta[6] + venta[7]) for venta in historial_ventas)

        #obtener la lista de productos para el filtro de productos
        productos_query = "SELECT id_producto, nombre FROM producto"
        productos = db.fetch_all(productos_query, [])

        productos_dict = [{'id_producto': producto[0], 'nombre': producto[1]} for producto in productos]

        context = {
            'historial_ventas': historial_ventas,
            'total': total,
            'productos': productos_dict
        }
    finally:
        db.close()
    return render(request, 'historico_ventas.html', context)







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