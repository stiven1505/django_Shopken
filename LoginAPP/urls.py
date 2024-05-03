
from django.urls import path
from . import views

urlpatterns = [
    # Ruta para iniciar sesión
    path('login/', views.iniciar_sesion, name='login'),

    # Ruta para registrar un nuevo usuario
    path('registro/', views.registro, name='registro'),

    # Otras rutas de tu aplicación
]
