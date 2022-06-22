# from pyexpat import model
# from rest_framework import serializers

# from mpesa.voldermort.core import MpesaClient


# class StkPushRequestSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ""

#     def create(self, validated_data):
#         mpesa_client = MpesaClient()
#         stk_push_callback_url = 'https://darajambili.herokuapp.com/express-payment'

#         phone_number=validated_data.get("phone_number")
#         amount=validated_data.get("amount")
#         account_reference=validated_data.get("account_reference")
#         transaction_desc=validated_data.get("transaction_desc")
#         callback_url=stk_push_callback_url

#         return mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)