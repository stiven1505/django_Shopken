from django.db import models
import jwt
from django.conf import settings


class  RegistroToken (models.Model):
    RegistroTokenId = models.AutoField(primary_key=True)
    id_usuario_comprador= models.CharField(max_length=24)
    id_usuario_vendedor= models.CharField(max_length=24)
    tipo_transaccion= models.CharField(max_length=100)
    nombre_banco= models.CharField(max_length=100)
    tipo_cuenta= models.CharField(max_length=100)
    numero_cuenta= models.CharField(max_length=100)
    estado_transaccion= models.BooleanField(default=False)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    valor_transaccion= models.DecimalField(decimal_places=2, default=0.0, max_digits=10)




class Token(models.Model):
    TokenId = models.AutoField(primary_key=True)
    id_usuario = models.CharField(max_length=24)
    cantidad = models.CharField(max_length=24)
    Tokengenerado = models.CharField(max_length=500)



