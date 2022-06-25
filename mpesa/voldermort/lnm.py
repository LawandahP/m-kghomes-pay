import time
import requests
from mpesa_password import generatePassword, getTimestamp, paybill_no
from mpesa_token import generateAccessToken


def lipaNaMpesaOnline():
    timeStamp = getTimestamp()
    # access_token = generateAccessToken()
    password = generatePassword()

    headers = { 
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + 'Pq4lVBt6NAy2DpxUpEsHLoRBGa5G' 
    }

    time.sleep(2)
    payload = {
        "BusinessShortCode": paybill_no,
        "Password": password,
        "Timestamp": timeStamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254740129131,
        "PartyB": paybill_no,
        "PhoneNumber": 254740129131,
        "CallBackURL": "https://m-kghomes-pay.herokuapp.com/api/v1/lnm-callback/",
        "AccountReference": "GITHAIGA",
        "TransactionDesc": "Payment of X" 
    }

    stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    response = requests.post(
        stk_push_url,
        headers = headers, json = payload
    )

    print(response.text)
lipaNaMpesaOnline()

# print(generate_access_token())

