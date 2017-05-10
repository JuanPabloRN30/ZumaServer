from rest_framework import serializers
from zumaInfo.models import Trabajador,Cliente,Interes,Categoria,Solicitud
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    intereses = serializers.SlugRelatedField(
                many=True,
                read_only=True,
                slug_field='nombre'
    )
    class Meta:
        model = Categoria
        fields = ('nombre', 'intereses' )

class InteresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interes
        fields = ('nombre',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name')

class TrabajadorSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField( source='user.username', required = False )
    password = serializers.CharField( source='user.password',required = False )
    email = serializers.CharField( source='user.email',required = False )
    first_name = serializers.CharField( source='user.first_name',required = False )
    intereses = InteresSerializer(many = True)
    class Meta:
        model = Trabajador
        fields = ('username','password','email','first_name','intereses')#, 'photo', 'factura', 'cedula','valoracion','cantidad_votos')

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField( source='user.username', required = False )
    password = serializers.CharField( source='user.password',required = False )
    email = serializers.CharField( source='user.email',required = False )
    first_name = serializers.CharField( source='user.first_name',required = False )
    class Meta:
        model = Cliente
        fields = ('username','password','email','first_name')#, 'photo')

class SolicitudSerializer(serializers.ModelSerializer):
    id_trabajador = serializers.CharField( source='trabajador.id' )
    id_cliente = serializers.CharField( source='cliente.id' )
    nombre_interes = serializers.CharField( source='interes.nombre' )
    class Meta:
        model = Solicitud
        fields = ('fecha', 'direccion', 'descripcion', 'estado', 'id_cliente', 'id_trabajador', 'nombre_interes')
