from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Categoria( models.Model ):
    nombre = models.CharField( max_length=100 )

class Interes( models.Model ):
    nombre = models.CharField( max_length=100 )
    categoria = models.ForeignKey( Categoria,related_name='intereses' ,on_delete = models.CASCADE )

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=100, null = True)
    factura = models.CharField(max_length=100, null = True)
    cedula = models.CharField(max_length=100, null = True, unique = True)
    valoracion = models.IntegerField(default=5)
    cantidad_votos = models.IntegerField(default=1)
    estado = models.BooleanField( default = False )
    intereses = models.ManyToManyField( Interes )
    descripcion = models.CharField( max_length=1000, null = True )
    def __str__(self):
        return self.user.username

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=100, null = True)
    intereses = models.ManyToManyField( Interes )
    def __str__(self):
        return self.user.username

class Solicitud( models.Model ):
    fecha = models.DateTimeField( null = False)
    direccion = models.CharField( max_length=200 )
    descripcion = models.CharField( max_length=500 )
    estado = models.CharField( max_length=200, default='Pendiente' )
    cliente = models.ForeignKey( Cliente, on_delete = models.CASCADE )
    trabajador = models.ForeignKey( Trabajador, on_delete = models.CASCADE )
    interes = models.ForeignKey( Interes, on_delete = models.CASCADE )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
