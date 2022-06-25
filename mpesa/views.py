from datetime import datetime
import pytz

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from mpesa.models import LipaNaMpesaOnline
from mpesa.serializers import LipaNaMpesaOnlineSerializer

from mpesa.voldermort.core import MpesaClient

# from voldermort.core import MpesaClient

mpesa_client = MpesaClient()
stk_push_callback_url = 'https://m-kghomes-pay.herokuapp.com/api/v1/lnm-callback/'


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


class LipaNaMpesaCallbackUrlAPIView(generics.GenericAPIView):
    queryset = LipaNaMpesaOnline.objects.all()
    serializer_class = LipaNaMpesaOnlineSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):     
        data = request.data
        print(data)   
        return Response(data)

    def get(self, request):     
        data = request.data
        print(data)   
        return Response(data)





















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




"""
        # {'Body': 
        #     {'stkCallback': 
        #         {
        #             'MerchantRequestID': '82441-85031621-1', 
        #             'CheckoutRequestID': 'ws_CO_010920211148228797', 
        #             'ResultCode': 0, 
        #             'ResultDesc': 'The service request is processed successfully.',
        #             'CallbackMetadata': 
        #                 {
        #                     'Item': [   
        #                         {'Name': 'Amount', 'Value': 1.0}, 
        #                         {'Name': 'MpesaReceiptNumber', 'Value': 'PI10C6XGTY'}, 
        #                         {'Name': 'Balance'}, 
        #                         {'Name': 'TransactionDate', 'Value': 20210901114837}, 
        #                         {'Name': 'PhoneNumber', 'Value': 254740129131}
        #                     ]
        #             }
        #         }
        #     }
        # }
        
        # """
        # merchant_request_id = request.data['Body']['stkCallback']['MerchantRequestID']
        # checkout_request_id = request.data['Body']['stkCallback']['CheckoutRequestID']
        # result_code = request.data['Body']['stkCallback']['ResultCode']
        # result_description = request.data['Body']['stkCallback']['ResultDesc']

        # amount = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        # mpesa_receipt_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']

        # transaction_date = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        # phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']

        # # convert timestamp to date
        

        # transaction_date_str = str(transaction_date)
        # transaction_datetime = datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")

        # timezone_aware_datetime = pytz.utc.localize(transaction_datetime)
        
        # lipa_na_mpesa_online = LipaNaMpesaOnline.objects.create(
        #     MerchantRequestID = merchant_request_id,
        #     CheckoutRequestID = checkout_request_id,
        #     ResultCode = result_code,
        #     ResultDesc = result_description,
        #     Amount = amount,
        #     MpesaReceiptNumber = mpesa_receipt_number,
        #     TransactionDate = timezone_aware_datetime,
        #     PhoneNumber = phone_number
        # )
        # lipa_na_mpesa_online.save()

        # serializer = LipaNaMpesaOnlineSerializer(lipa_na_mpesa_online, many=False)