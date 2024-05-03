from rest_framework import serializers
from TiendaAPP.models import RegistroTienda


class RegistroTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroTienda
        fields = (
            'RegistroTiendaId',
            'id_vendedor',
            'id_comprador',
            'titulo_producto',
            'precio_producto',
            'imagen_producto',
            'detalle_producto',
            'estado_envio',
            'estado_recibido',
            'estado_pago_shopken',
            'RegistroTokenId'
        )
