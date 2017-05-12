from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction

from zumaInfo.models import *
from zumaInfo.serializers import *

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


@csrf_exempt
def categoria_detail(request, nombre):
    try:
        categoria = Categoria.objects.get(nombre=nombre)
    except Categoria.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategoriaSerializer(categoria, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        categoria.delete()
        return HttpResponse(status=204)

@csrf_exempt
def interes_detail(request, nombre):
    try:
        interes = Interes.objects.get(nombre=nombre)
    except Interes.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategoriaSerializer(interes)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategoriaSerializer(interes, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        interes.delete()
        return HttpResponse(status=204)

class TrabajadorList(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format = None):
        logger.info('get all customers endpoint')
        trabajadores = Trabajador.objects.all()
        serializer = TrabajadorSerializer(trabajadores, many = True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format = None):
        serializer = TrabajadorSerializer(data = request.data)
        if serializer.is_valid():
            logger.info('Creating user %s started' % serializer.data['username'])
            print (serializer.data)
            print ("Llegue con la siguiente info: ")
            print (serializer.data[ 'first_name' ])
            print (serializer.data[ 'username' ])
            print (serializer.data[ 'email' ])
            print (serializer.data[ 'password' ])
            print (serializer.data[ 'intereses' ])
            print ("Imprimiendo los intereses")


            user = User(first_name = serializer.data['first_name'], \
                        username = serializer.data['username'],     \
                        email = serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            trabajador = Trabajador(user = user)
            trabajador.save()
            for item in serializer.data[ 'intereses' ]:
                trabajador.intereses.add( Interes.objects.get(nombre=item['nombre']) )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ClienteList(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format = None):
        logger.info('get all customers endpoint')
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many = True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format = None):
        serializer = ClienteSerializer(data = request.data)
        if serializer.is_valid():
            logger.info('Creating user %s started' % serializer.data['username'])
            print ("Llegue con la siguiente info: ")
            print (serializer.data[ 'first_name' ])
            print (serializer.data[ 'username' ])
            print (serializer.data[ 'email' ])
            print (serializer.data[ 'password' ])

            user = User(first_name = serializer.data['first_name'], \
                        username = serializer.data['username'],     \
                        email = serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            cliente = Cliente(user = user)
            cliente.save()
            for item in serializer.data[ 'intereses' ]:
                cliente.intereses.add( Interes.objects.get(nombre=item['nombre']) )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_trabajador_authenticated(request):
    try:
        user = request.user
        trabajador = Trabajador.objects.filter(user__id__exact=user.id).first()
        if trabajador is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Trabajador.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TrabajadorSerializer(trabajador)
    return Response(serializer.data)

@api_view(['GET'])
def get_cliente_authenticated(request):
    try:
        user = request.user
        cliente = Cliente.objects.filter(user__id__exact=user.id).first()
        if cliente is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClienteSerializer(cliente)
    return Response(serializer.data)

@api_view(['GET'])
def solicitud_cliente(request):
    user = request.user
    print (user)
    cliente = Cliente.objects.filter(user__id__exact = user.id).first()
    solicitudes = Solicitud.objects.filter(cliente = cliente).all()
    estado = request.query_params.get('estado',None)
    if estado is not None:
        listaSolicitudes = estado.split(',')
        solicitudes = Solicitud.objects.filter(estado__in = listaSolicitudes).all()
    mis_solicitudes = []
    for solicitud in solicitudes:
        mis_solicitudes.append(solicitud)
    serializer = SolicitudSerializer(mis_solicitudes, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def solicitud_trabajador(request):
    user = request.user
    print (user)
    trabajador = Trabajador.objects.filter(user__id__exact = user.id).first()
    solicitudes = Solicitud.objects.filter(trabajador = trabajador).all()
    estado = request.query_params.get('estado',None)
    if estado is not None:
        listaSolicitudes = estado.split(',')
        solicitudes = Solicitud.objects.filter(estado__in = listaSolicitudes).all()
    mis_solicitudes = []
    for solicitud in solicitudes:
        mis_solicitudes.append(solicitud)
    serializer = SolicitudSerializer(mis_solicitudes, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def solicitud_trabajador_interes(request,nombre):
    interes = Interes.objects.get( nombre = nombre )
    trabajadores = Trabajador.objects.filter(intereses = interes).all()
    mis_trabajadores = []
    for trabajador in trabajadores:
        mis_trabajadores.append(trabajador)
    serializer = TrabajadorSerializer(mis_trabajadores, many = True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def tipo_usuario(request):
    auth_Cliente = False;
    auth_Trabajador = False;
    try:
        usuario = User.objects.get( username = request.data['username'] )
    except User.DoesNotExist:
        return JsonResponse({'tipo':'ninguno'});

    try:
        trabajador = Trabajador.objects.get( user__id = usuario.id )
        auth_Trabajador = True;
    except Trabajador.DoesNotExist:
        print ("No existe")

    try:
        cliente = Cliente.objects.get( user__id = usuario.id )
        auth_Cliente = True;
    except Cliente.DoesNotExist:
        print ("No existe")
    if auth_Trabajador:
        return JsonResponse({'tipo':'trabajador'});
    else:
        return JsonResponse({'tipo':'cliente'});

@api_view(['POST'])
def create_solicitud(request):
    serializer = SolicitudDTOSerializer(data = request.data)
    if request.method == 'GET':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        if serializer.is_valid():
            trabajador_usuario = User.objects.filter(username = serializer.data['trabajadorusername']).first()
            trabajador = Trabajador.objects.filter(user__id__exact = trabajador_usuario.id).first()
            interes = Interes.objects.filter(nombre = serializer.data['interesnombre']).first()
            #fecha = serializer.data['fecha']
            #direccion = serializer.data['direccion']
            #descripcion = serializer.data['descripcion']
            fecha = datetime.now();
            user = request.user
            cliente = Cliente.objects.filter(user__id__exact = user.id).first()
            solicitud = Solicitud(fecha=fecha,cliente = cliente,trabajador = trabajador, interes = interes)
            solicitud.save()
            serializer = SolicitudSerializer(solicitud)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    except Interes.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    except Trabajador.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def edit_solicitud(request):
    serializer = SolicitudDTOSerializer(data = request.data)
    if request.method == 'GET':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        if serializer.is_valid():
            solicitud = Solicitud.objects.get( pk = serializer.data['id'] );
            solicitud.estado = serializer.data['estado'];
            solicitud.save()
            serializer = SolicitudSerializer(solicitud)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    except Solicitud.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
