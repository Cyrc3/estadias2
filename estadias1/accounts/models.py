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
    rfc = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=255)
    uso_factura = models.CharField(max_length=255)
    regimen_fiscal = models.CharField(max_length=10)
    codigo_postal = models.CharField(max_length=10)

    class Meta:
        db_table = "cliente"
        managed = False


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    numero_telefono = models.CharField(max_length=255)
    rfc = models.CharField(max_length=20)

    class Meta:
        db_table = 'proveedor'
        managed = False 

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    class Meta : 
        db_table = 'categoria_producto'
        managed = False

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    stock = models.IntegerField()
    nombre = models.CharField(max_length=255)
    id_categoria = models.IntegerField()
    costo_venta = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta :
        db_table = 'producto'
        managed = False

#faltan cosas aki

    
