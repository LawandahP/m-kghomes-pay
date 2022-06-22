import requests
from requests.auth import HTTPBasicAuth


def generateAccessToken():
    consumer_key = 'yVS3HM45wEfZYftAsptGOr8wkMCypzbd'
    consumer_secret = 'cXjtpeJjA7VaPuGp'
    mpesa_auth_endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        response = requests.get(
            mpesa_auth_endpoint,
            auth=HTTPBasicAuth( consumer_key, consumer_secret),
        )
    except:
        response = requests.get(
            mpesa_auth_endpoint,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            verify=False
        )
    auth_res = response.json()
    my_access_token = auth_res['access_token']

    print("access-token-", my_access_token)
    return my_access_token
# generateAccessToken()














# import requests

# from payments import mpesa_keys
# from payments import generateAccessToken, generatePassword, generateAccessToken, getTimestamp


# def lipaNaMpesaOnline():
#   timeStamp = getTimestamp()
#   access_token = generateAccessToken()
#   password = generatePassword()


#   headers = { 
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer %s' % access_token 
#   }

#   payload = {
#       "BusinessShortCode": mpesa_keys.paybill_no,
#       "Password": password,
#       "Timestamp": timeStamp,
#       "TransactionType": "CustomerPayBillOnline",
#       "Amount": 1,
#       "PartyA": mpesa_keys.phone_number,
#       "PartyB": mpesa_keys.paybill_no,
#       "PhoneNumber": mpesa_keys.phone_number,
#       "CallBackURL": "https://magicalcarpets.herokuapp.com/api/payments/lnm",
#       "AccountReference": "GITHAIGA",
#       "TransactionDesc": "Payment of X" 
#     }

#   stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#   response = requests.post(
#     stk_push_url,
#     headers = headers, json = payload)
#   print(response.text)

# # lipaNaMpesaOnline()
