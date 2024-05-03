from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #Permite a otros dominio acceder a los metodos
from django.conf import settings
from rest_framework.parsers import JSONParser #Analizar los datos JSON
from django.http.response import JsonResponse #Respuestas de datos JSON
import jwt
from cryptography.fernet import Fernet


#Datos entrantes
from TokenAPP.models import RegistroToken, Token
from TokenAPP.serializers import RegistroTokenSerializer,TokenSerializer

from django.http import HttpResponseRedirect






# Create your views here.

@csrf_exempt
def registroTokenApi(request, id=0):

    if request.session.get('is_authenticated'):
        #devolvera todos los registros en formato JSON
        if request.method=='GET':
            registroToken = RegistroToken.objects.all()
            registroToken_serializer=RegistroTokenSerializer(registroToken,many=True)#Uso de clase serializer para convertirlo a formato JSON
            return JsonResponse(registroToken_serializer.data,safe=False)
        #Insertar registros en la tabla
        elif request.method=='POST':
            #se analiza la solicitud usando el serializador y le convierte en un modelo
            registroToken_data=JSONParser().parse(request)
            registroToken_data['id_vendedor'] = request.session.get('username')
            registroToken_serializer = RegistroTokenSerializer(data=registroToken_data)
            #cuando el modelo sea valido, se guarda
            if registroToken_serializer.is_valid():
                registroToken_serializer.save()
                return JsonResponse("Se agrego t",safe=False)
            return JsonResponse("No se agrego ",safe=False)
        #Actualizar registro de la tabla
        elif request.method=="PUT":
            registroToken_data=JSONParser().parse(request)
            #Se captura el registro existente con el Id 
            registroToken=RegistroToken.objects.get(RegistroTokenId=registroToken_data['RegistroTokenId'])
            
            #con la clase serializer se asignan los nuevos valores
            registroToken_serializer=RegistroTokenSerializer(registroToken,data=registroToken_data)
            #se guarda con la validacion
            if registroToken_serializer.is_valid():
                registroToken_serializer.save()
                return JsonResponse("Se Actualizo",safe=False)
            return JsonResponse("No se Actualizo",safe=False)
        #Elimiar registro de la tabla
        elif request.method=="DELETE":
            #Por medio del id se elimina
            registroToken=RegistroToken.objects.get(RegistroTokenId=id)
            registroToken.delete()
            return JsonResponse("Se Elimino",safe=False)
        return JsonResponse("No se Elimino",safe=False)
    else:
        # El usuario no está autenticado, redirige a la página de inicio
        return HttpResponseRedirect('/ruta-vista-en-angular/')  # Cambia la ruta 


@csrf_exempt
def tokenApi(request, id=0):
    if request.session.get('is_authenticated'):
        #devolvera todos los registros en formato JSON
        if request.method=='GET':
            token = Token.objects.all()
            token_serializer=TokenSerializer(token,many=True)#Uso de clase serializer para convertirlo a formato JSON
            return JsonResponse(token_serializer.data,safe=False)
        #Insertar registros en la tabla
        elif request.method == 'POST':
            #configuracion para encriptar cantidad 
            clave_cifrado = Fernet(settings.SECRET_KEY.encode())
            f = Fernet(clave_cifrado)

            id_usuario = request.POST.get('id_usuario')
            cantidad = request.POST.get('cantidad')

            # Cifra la cantidad
            cantidad_cifrada = f.encrypt(cantidad.encode()).decode()
        
            # Generar el token JWT
            payload = {
                'id_usuario': id_usuario,
                'cantidad': cantidad_cifrada,
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            # Crear o actualizar un registro en la tabla Token
            token_obj, created = Token.objects.get_or_create(id_usuario=id_usuario)
            token_obj.id_usuario = id_usuario  # Asignar el valor de id_usuario
            token_obj.cantidad = cantidad_cifrada  # Asignar el valor de cantidad
            token_obj.Tokengenerado = token
            token_obj.save()
            
            return JsonResponse({'token': token})
        #Actualizar registro de la tabla
        elif request.method=="PUT":
            token_data=JSONParser().parse(request)
            #Se captura el registro existente con el Id 
            token=Token.objects.get(TokenId=token_data['TokenId'])
            #con la clase serializer se asignan los nuevos valores
            token_serializer=TokenSerializer(token,data=token_data)
            #se guarda con la validacion
            if token_serializer.is_valid():
                token_serializer.save()
                return JsonResponse("Se Actualizo",safe=False)
            return JsonResponse("No se Actualizo",safe=False)
        #Elimiar registro de la tabla
        elif request.method=="DELETE":
            #Por medio del id se elimina
            token=Token.objects.get(TokenId=id)
            token.delete()
            return JsonResponse("Se Elimino",safe=False)
        return JsonResponse("No se Elimino",safe=False)
    else:
         # El usuario no está autenticado, redirige a la página de inicio
        return HttpResponseRedirect('/ruta-vista-en-angular/')  # Cambia la ruta 
