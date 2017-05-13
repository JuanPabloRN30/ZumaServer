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
        fields = ('username','password','email','first_name','intereses','valoracion','cantidad_votos')#, 'photo', 'factura', 'cedula','valoracion','cantidad_votos')

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField( source='user.username', required = False )
    password = serializers.CharField( source='user.password',required = False )
    email = serializers.CharField( source='user.email',required = False )
    first_name = serializers.CharField( source='user.first_name',required = False )
    intereses = InteresSerializer(many = True)
    class Meta:
        model = Cliente
        fields = ('username','password','email','first_name','intereses')#, 'photo')

class SolicitudSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha = serializers.DateTimeField()
    direccion = serializers.CharField(max_length = 200)
    descripcion = serializers.CharField(max_length = 500)
    estado = serializers.CharField(max_length = 200)
    cliente = ClienteSerializer()
    trabajador = TrabajadorSerializer()
    interes = InteresSerializer()

class SolicitudDTOSerializer(serializers.Serializer):
#    fecha = serializers.DateTimeField()
    direccion = serializers.CharField(max_length = 200)
#    descripcion = serializers.CharField(max_length = 500)
    id = serializers.IntegerField( required = False )
    estado = serializers.CharField(max_length = 200, required = False)
    trabajadorusername = serializers.CharField(max_length = 500)
    interesnombre = serializers.CharField(max_length = 500)
