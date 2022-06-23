from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

from mpesa.voldermort.core import MpesaClient

# from voldermort.core import MpesaClient

mpesa_client = MpesaClient()
stk_push_callback_url = 'https://darajambili.herokuapp.com/express-payment'


@api_view(['GET'])
def index(request):
    urls = {
        "access-token": "oauth-token/",
        "lnm-stk-push": "lnm/stk-push/",
        "c2b": "c2b/"
    }
    return Response(urls, 200)

@api_view(['GET'])
def get_auth_token(request):
    token = mpesa_client.access_token()
    access_token = {"token": token}
    return Response(access_token, status=status.HTTP_200_OK)





@api_view(['POST'])
def lipaNaMpesaOnlineStkPush(request):
    """
    
    {
        "transaction_type": "CustomerPayBillOnline",
        "business_short_code": 174379,
        "phone_number": "0740129131",
        "amount": 1,
        "account_reference": "GITHAIGA",
        "transaction_desc": "Payment for Rent"
    }
    
    """
    data = request.data

    r = mpesa_client.stk_push(
        transaction_type=data["transaction_type"],
        business_short_code=data["business_short_code"],
        phone_number=data["phone_number"],
        amount=data["amount"],
        account_reference=data["account_reference"],
        transaction_desc=data["transaction_desc"],
        callback_url=stk_push_callback_url,
    )
    return Response(r, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def c2bPayment(request):

    """
        {
            "business_short_code": 174379,
            "phone_number": "0740129131",
            "amount": 1,
            "account_number": "0740129131",
            "transaction_type": "CustomerPayBillOnline"
        }
    """

    data = request.data
    r = mpesa_client.c2b(

        business_short_code=data["business_short_code"],
        phone_number=data["phone_number"],
        amount=data["amount"],
        account_number=data["account_number"],
        transaction_type=data["transaction_type"],
    )

    return Response(r, 200)





























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