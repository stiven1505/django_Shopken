from rest_framework import serializers
from TokenAPP.models import RegistroToken, Token



class RegistroTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroToken
        fields = (
            'RegistroTokenId',
            'id_usuario_vendedor',
            'tipo_transaccion',
            'nombre_banco',
            'tipo_cuenta',
            'numero_cuenta',
            'estado_transaccion',
            'fecha_transaccion',
            'valor_transaccion'
        )


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'TokenId',
            'id_usuario',
            'cantidad',
            'Tokengenerado', 
        )
