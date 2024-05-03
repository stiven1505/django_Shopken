""" from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session

@csrf_exempt
def loginApi(request):
    if request.method == 'POST':
        # Obtener las credenciales del cliente desde los datos JSON
        data = JSONParser().parse(request)
        usern = data.get('UsuarioName')
        pas = data.get('Password')
      # Utiliza 'Password'

        # Verificar las credenciales con la base de datos
        user = authenticate(request, username=usern, password=pas)
        print(user)
        print(pas)
        print(usern)

        if user is not None:
            # Las credenciales son válidas, iniciar sesión
            login(request, user)
            request.session['is_authenticated'] = True
            request.session['username'] = user.UsuarioName  # Utiliza 'UsuarioName' para obtener el nombre de usuario
            return JsonResponse({"message": "Inicio de sesión exitoso"})
        else:
            request.session['is_authenticated'] = False
            # Las credenciales no son válidas, devolver un mensaje de error
            return JsonResponse({"message": "Nombre de usuario o contraseña incorrectos"}, status=401)
 """

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import CustomUser 
@csrf_exempt
def registro(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"message": "Nombre de usuario y contraseña son requeridos."}, status=400)

        # Verifica si el usuario ya existe en el modelo personalizado
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"message": "El nombre de usuario ya existe."}, status=400)

        # Crea un nuevo usuario en el modelo personalizado
        user = CustomUser.objects.create_user(username=username, password=password)

        return JsonResponse({"message": "Registro exitoso"})

    return JsonResponse({"message": "Método no permitido"}, status=405)

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['is_authenticated'] = True
            request.session['username'] = user.UsuarioName
            return JsonResponse({"message": "Inicio de sesión exitoso"})
        else:
            return JsonResponse({"message": "Nombre de usuario o contraseña incorrectos"}, status=401)

    return JsonResponse({"message": "Método no permitido"}, status=405)
