from django.db import models
from django.contrib.auth.models import AbstractUser


#as far as i understand, this class 'Usuario' is meant to be the one who looks after the user and password in our database
#I have to insist, AS FAR AS I UNDERSTAND
#Not an expert tho
#uwu
class Usuario(AbstractUser):
    class Meta:
        db_table = 'USUARIO'   #Lit USUARIO es el nombre de la tabla, huele a fuga de informacion si me lo preguntas.
        managed = False