import base64
from datetime import datetime


lipa_na_mpesa_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
paybill_no = 174379

def getTimestamp():
    time = datetime.now()
    time_stamp = time.strftime("%Y%m%d%H%M%S")
    print("timestamp", time_stamp)
    return time_stamp


def generatePassword():
    timeStamp = getTimestamp()
    data_to_encode = str(paybill_no) + lipa_na_mpesa_passkey + timeStamp
    encoded_string = base64.b64encode(data_to_encode.encode())

    password = encoded_string.decode('utf-8')
    print("password -", password)
    return password

# generatePassword()
