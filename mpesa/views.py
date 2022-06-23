from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

from mpesa.voldermort.core import MpesaClient

# from voldermort.core import MpesaClient

mpesa_client = MpesaClient()
stk_push_callback_url = 'https://darajambili.herokuapp.com/express-payment'

@api_view(['GET'])
def get_auth_token(request):
    token = mpesa_client.access_token()
    access_token = {"token": token}
    return Response(access_token, status=status.HTTP_200_OK)


# {
#     "phone_number": 254740129131,
#     "amount": 1,
#     "account_reference": "GITHAIGA",
#     "transaction_desc": "Payment for Rent",
# }


@api_view(['POST'])
def lipaNaMpesaOnlineStkPush(request):
    data = request.data
    r = mpesa_client.stk_push(
        phone_number=data["phone_number"],
        amount=data["amount"],
        account_reference=data["account_reference"],
        transaction_desc=data["transaction_desc"],
        callback_url=stk_push_callback_url,
    )
    return Response(r, status=status.HTTP_200_OK)
    


































# class LNMOnlineStkPush(generics.GenericAPIView):
#     serializer_class = StkPushRequestSerializer

#     def post(self, request):
#         data = request.data
#         serializer = self.serializer_class(
#             data=data, context={'request': request})
#         if serializer.is_valid():
#             return Response(serializer.data, status.HTTP_200_OK)
            
#         error = {'detail': serializer.errors}
#         return Response(error, status.HTTP_400_BAD_REQUEST)