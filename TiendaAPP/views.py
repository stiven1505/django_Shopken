from django.shortcuts import render
# Permite a otros dominio acceder a los metodos
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser  # Analizar los datos JSON
from django.http.response import JsonResponse  # Respuestas de datos JSON


# Datos entrantes
import jwt
from TiendaAPP.models import RegistroTienda
from TokenAPP.models import RegistroToken, Token
from TokenAPP.serializers import RegistroTokenSerializer, TokenSerializer
from TiendaAPP.serializers import RegistroTiendaSerializer
from django.conf import settings
from cryptography.fernet import Fernet
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
import logging


# Create your views here.
@csrf_exempt
def registroTiendaApi(request, id=0):
    # if request.session.get('is_authenticated'):
    # devolvera todos los registros en formato JSON
    if request.method == 'GET':
        registroTienda = RegistroTienda.objects.all()
        # Uso de clase serializer para convertirlo a formato JSON
        registroTienda_serializer = RegistroTiendaSerializer(
            registroTienda, many=True)
        return JsonResponse(registroTienda_serializer.data, safe=False)

    # Insertar registros en la tabla
    elif request.method == 'POST':
        # Agrega mensajes de registro para depuración
        logger = logging.getLogger(__name__)
        logger.info("Received POST request with data: %s", request.body)

        registroTienda_data = JSONParser().parse(request)
        registroTiendaSerializer = RegistroTiendaSerializer(
            data=registroTienda_data)

        if registroTiendaSerializer.is_valid():
            registroTiendaSerializer.save()
            return JsonResponse("Added Successfully", safe=False)
        else:
            logger.error("Validation errors: %s", registroTiendaSerializer.errors)

        return JsonResponse("Failed to Add", safe=False)
    # Actualizar registro de la tabla
    elif request.method == "PUT":
        usuario_iniciado = request.session.get('username')
        registroTienda_data = JSONParser().parse(request)
        registroTienda_id = registroTienda_data['RegistroTiendaId']

        try:
            registroTienda = RegistroTienda.objects.get(
                RegistroTiendaId=registroTienda_id)
        except RegistroTienda.DoesNotExist:
            return JsonResponse("El registro no existe", safe=False, status=404)

        # Verificar si el usuario que realiza la solicitud es el vendedor o si ya hay un registro de comprador
        es_vendedor = registroTienda.id_vendedor == usuario_iniciado or registroTienda.id_comprador != "null"

        # Si el usuario no es el vendedor, actualiza el campo id_comprador
        if not es_vendedor:
            registroTienda_data['id_comprador'] = usuario_iniciado

        registroTienda_serializer = RegistroTiendaSerializer(
            registroTienda, data=registroTienda_data, partial=not es_vendedor)

        if registroTienda_serializer.is_valid():
            # Obtener la cantidad del usuario iniciado en sesión
            token_usuario = Token.objects.filter(
                id_usuario=usuario_iniciado).first()
            cantidad_usuario = token_usuario.cantidad if token_usuario else 0

            precio_producto = registroTienda_data['precio_producto']
            clave_cifrado = Fernet(settings.SECRET_KEY)
            cantidad_desencriptada = clave_cifrado.decrypt(
                cantidad_usuario.encode()).decode()

            if float(cantidad_desencriptada) >= float(precio_producto):

                # Actualizar registroTienda
                registroTienda_serializer.save()

                # Actualizar cantidad de tokens del comprador
                nuevaCantidad = float(
                    cantidad_desencriptada) - float(precio_producto)
                nuevaCantidad_cifrada = clave_cifrado.encrypt(
                    str(nuevaCantidad).encode()).decode()

                token_usuario.cantidad = nuevaCantidad_cifrada
                token_usuario.Tokengenerado = jwt.encode({'id_usuario': usuario_iniciado, 'cantidad': nuevaCantidad_cifrada},
                                                         settings.SECRET_KEY, algorithm='HS256')
                token_usuario.save()

                # Actualizar cantidad de tokens del vendedor
                if not es_vendedor:
                    try:
                        token_vendedor = Token.objects.get(
                            id_usuario=registroTienda.id_vendedor)
                        cantidad_vendedor = token_vendedor.cantidad
                        id_vendedor = token_vendedor.id_usuario
                    except Token.DoesNotExist:
                        cantidad_vendedor = 0

                    nuevaCantidad_vendedor = float(
                        cantidad_vendedor) + float(precio_producto)
                    nuevaCantidad_vendedor_cifrada = clave_cifrado.encrypt(
                        str(nuevaCantidad_vendedor).encode()).decode()

                    # Generar un nuevo token para el vendedor (si es necesario)
                    payload_vendedor = {
                        'id_usuario': id_vendedor,
                        'cantidad': nuevaCantidad_vendedor_cifrada,
                    }

                    token_vendedor = jwt.encode(
                        payload_vendedor, settings.SECRET_KEY, algorithm='HS256')

                    # Actualizar el registro del vendedor en la tabla Token
                    try:
                        token_vendedor = Token.objects.get(
                            id_usuario=registroTienda.id_vendedor)
                        token_vendedor.cantidad = nuevaCantidad_vendedor_cifrada
                        # Actualiza también el token generado (opcional)
                        token_vendedor.Tokengenerado = token_vendedor
                        token_vendedor.save()
                    except Token.DoesNotExist:
                        JsonResponse("Sin token", safe=False)
                        pass

                # Crear registro en RegistroToken
                registro_token_data = {
                    'id_usuario_comprador': registroTienda_data['id_vendedor'],
                    'id_usuario_vendedor': registroTienda_data['id_comprador'],
                    'tipo_transaccion': 'Traspaso',
                    'nombre_banco': 'Banco Ejemplo',
                    'tipo_cuenta': 'Cuenta de Ahorros',
                    'numero_cuenta': '1234567890',
                    'estado_transaccion': True,
                    'valor_transaccion': registroTienda_data['precio_producto'],
                }

                registro_token_serializer = RegistroTokenSerializer(
                    data=registro_token_data)

                if registro_token_serializer.is_valid():
                    registro_token_serializer.save()
                    nuevo_registro_token_id = registro_token_serializer.data['RegistroTokenId']

                    # Actualizar RegistroTokenId en registroTienda
                    registroTienda.RegistroTokenId = nuevo_registro_token_id
                    registroTienda.save()

                    return JsonResponse("Datos guardados correctamente", safe=False)

        return JsonResponse("No se Actualizó RegistroTienda", safe=False)

    # Elimiar registro de la tabla
    elif request.method == "DELETE":
        # Por medio del id se elimina
        registroTienda = RegistroTienda.objects.get(RegistroTiendaId=id)
        registroTienda.delete()
        return JsonResponse("Se Elimino", safe=False)
    return JsonResponse("No se Elimino", safe=False)
   # else:
    # El usuario no está autenticado, redirige a la página de inicio
    # Cambia la ruta
    # return HttpResponseRedirect('/ruta-vista-en-angular/')
   # return JsonResponse("No se Elimino", safe=False)


# para el cambio del estado de envio y recibido se crea nuevas vistas
""" 
# ...

@csrf_exempt
def cambiar_estado_envio(request, id=0):
    # Verifica si el usuario está autenticado
    if request.session.get('is_authenticated'):
        if request.method == 'PUT':
            try:
                registroTienda = RegistroTienda.objects.get(RegistroTiendaId=id)
            except RegistroTienda.DoesNotExist:
                return HttpResponseNotFound("El registro no existe", status=404)

            # Verifica si el usuario que realiza la solicitud es el vendedor
            if registroTienda.id_vendedor == request.session.get('username'):
                # Cambia el estado de envío a True
                registroTienda.estado_envio = True
                registroTienda.save()
                return JsonResponse("Estado de envío cambiado a True", safe=False)
            else:
                return HttpResponseBadRequest("No tiene permiso para cambiar el estado de envío", status=400)
        else:
            return HttpResponseBadRequest("Método no permitido", status=400)
    else:
        return HttpResponseBadRequest("Usuario no autenticado", status=401)

@csrf_exempt
def cambiar_estado_recibido(request, id=0):
    # Verifica si el usuario está autenticado
    if request.session.get('is_authenticated'):
        if request.method == 'PUT':
            try:
                registroTienda = RegistroTienda.objects.get(RegistroTiendaId=id)
            except RegistroTienda.DoesNotExist:
                return HttpResponseNotFound("El registro no existe", status=404)

            # Verifica si el usuario que realiza la solicitud es el comprador
            if registroTienda.id_comprador == request.session.get('username'):
                # Cambia el estado recibido a True
                registroTienda.estado_recibido = True
                registroTienda.save()
                return JsonResponse("Estado recibido cambiado a True", safe=False)
            else:
                return HttpResponseBadRequest("No tiene permiso para cambiar el estado recibido", status=400)
        else:
            return HttpResponseBadRequest("Método no permitido", status=400)
    else:
        return HttpResponseBadRequest("Usuario no autenticado", status=401)
  """
