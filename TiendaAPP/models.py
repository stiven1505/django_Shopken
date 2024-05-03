# Create your models here.
from django.db import models



class RegistroTienda(models.Model):
    RegistroTiendaId = models.AutoField(primary_key=True)
    id_vendedor = models.CharField(max_length=24)
    id_comprador = models.CharField(max_length=24)
    
    titulo_producto = models.CharField(max_length=24)
    precio_producto = models.CharField(max_length=24)
    imagen_producto = models.CharField(max_length=24)
    detalle_producto  = models.CharField(max_length=24)

    estado_envio = models.BooleanField(default=False)
    estado_recibido = models.BooleanField(default=False)
    estado_pago_shopken = models.BooleanField(default=False)
    RegistroTokenId = models.CharField(max_length=24, null=True, blank=True)
