
from django.urls import re_path

from TiendaAPP import views

urlpatterns=[
    re_path(r'^registroTienda$',views.registroTiendaApi),
    re_path(r'^registroTienda/([0-9]+)$',views.registroTiendaApi),

    # Otras rutas de tu aplicación
]