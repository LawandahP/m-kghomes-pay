from rest_framework import serializers

from mpesa.models import LipaNaMpesaOnline


class LipaNaMpesaOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipaNaMpesaOnline
        fields = '__all__'
