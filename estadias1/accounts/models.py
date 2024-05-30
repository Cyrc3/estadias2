from django.db import models
from django.contrib.auth.models import AbstractUser


#Commented bcs this isn't working
class Usuario(AbstractUser):
    class Meta:
        db_table = 'USUARIO'  
        managed = False


#class Usuario(models.Model):
#    db_table = 'USUARIO' 
#    id_usuario = models.AutoField(primary_key=True)
#    nombre = models.CharField(max_length=255)
#    privilegio = models.CharField(max_length=255)
#    password = models.CharField(max_length=255)
#    managed = False


#MÉTODOS DEL CLIENTE "-------------UWU------------------"
class Cliente(models.Model):
    rfc = models.CharField(max_length=13)
    razon_social = models.CharField(max_length=255)
    uso_factura = models.CharField(max_length=255)
    regimen_fiscal = models.CharField(max_length=255)
    codigo_postal = models.IntegerField()

    class Meta:
        db_table = "cliente"
        managed = False


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    numero_telefono = models.CharField(max_length=255)
    rfc = models.CharField(max_length=12)

    class Meta:
        db_table = 'proveedor'
        managed = False 
    def __str__(self):
        return self.razon_social


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    class Meta : 
        db_table = 'categoria_producto'
        managed = False
    def __str__(self):
        return self.descripcion
    

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    stock = models.IntegerField()
    nombre = models.CharField(max_length=255)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,db_column='id_categoria')
    costo_venta = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta :
        db_table = 'producto'
        managed = False
    def __str__(self):
        return self.nombre


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    fecha = models.DateField()

    class Meta : 
        db_table = 'compra'
        managed = False



class Detalle_Compra(models.Model):
    id_detallecompra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, db_column='id_compra',null=True)
    id_proveedor = models.ForeignKey(Proveedor,on_delete=models.SET_NULL, db_column='id_proveedor',null=True)
    id_producto = models.ForeignKey(Producto,on_delete=models.SET_NULL, db_column='id_producto',null=True)
    cantidad = models.IntegerField()
    costo = models.FloatField()

    class Meta:
        db_table = 'detalle_compra'
        managed = False



class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'venta'
        managed = False

        
class Detalle_Venta(models.Model):
    id_detalleventa = models.AutoField(primary_key=True)
    id_venta1 = models.ForeignKey(Venta, on_delete=models.SET_NULL, db_column='id_venta', null=True)
    id_producto = models.ForeignKey(Producto,on_delete=models.SET_NULL, db_column='id_producto',null=True)
    cantidad = models.IntegerField()
    precio_total = models.FloatField()
    iva = models.FloatField()
    class Meta:
        db_table = 'detalle_venta'
        managed = False

