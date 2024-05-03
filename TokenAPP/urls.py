#URLS especificados de los metodos de la API
from django.urls import re_path

from TokenAPP import views

urlpatterns = [
    re_path(r'^registroToken$',views.registroTokenApi),
    re_path(r'^registroToken/([0-9]+)$',views.registroTokenApi),

    re_path(r'^token$',views.tokenApi),
    re_path(r'^token/([0-9]+)$',views.tokenApi),

]
