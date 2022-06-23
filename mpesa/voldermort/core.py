import requests
from requests.auth import HTTPDigestAuth
import base64
from datetime import datetime
import json
from .exceptions import MpesaInvalidParameterException, MpesaConnectionError
from .utils import encrypt_security_credential, mpesa_access_token, format_phone_number, api_base_url, mpesa_config, mpesa_response
from decouple import config

from rest_framework.response import Response as RestResponse
from rest_framework import status

class MpesaClient:
	"""
	This is the core MPESA client. 
	The Mpesa Client will access all interactions with the MPESA Daraja API.
	"""

	auth_token = ''

	def __init__(self):
		"""
		The constructor for MpesaClient class
		"""

	def access_token(self):
		"""
		Generate an OAuth access token.
		Returns:
			bool: A string containing a valid OAuth access token
		"""
		
		return mpesa_access_token()

	def parse_stk_result(self, result):
		"""
		Parse the result of Lipa na MPESA Online Payment (STK Push)
		Returns:
			The result data as an array
		"""
		
		payload = json.loads(result)
		data = {}
		callback = payload['Body']['stkCallback']
		data['ResultCode'] = callback['ResultCode']
		data['ResultDesc'] = callback['ResultDesc']
		data['MerchantRequestID'] = callback['MerchantRequestID']
		data['CheckoutRequestID'] = callback['CheckoutRequestID']
		metadata = callback.get('CallbackMetadata')
		if metadata:
			metadata_items = metadata.get('Item')
			for item in metadata_items:
				data[item['Name']] = item.get('Value')
		
		return data

	def stk_push(self, business_short_code, phone_number, amount, account_reference, transaction_desc, transaction_type, callback_url):
		"""
		Attempt to send an STK prompt to customer phone
		Args:
			phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
			amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
			account_reference (str) -- This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type. Along with the business name, this value is also displayed to the customer in the STK Pin Prompt message. Maximum of 12 characters.
			transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
			call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response
		
		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
		"""

		if str(account_reference).strip() == '':
			error = {"detail": ["Account reference cannot be blank"]}
			return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			# raise MpesaInvalidParameterException('Account reference cannot be blank')
		if str(transaction_desc).strip() == '':
			error = {"detail": ["Transaction description cannot be blank"]}
			return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			# raise MpesaInvalidParameterException('Transaction description cannot be blank')
		if not isinstance(amount, int):
			error = {"detail": ["Amount must be an integer"]}
			# return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			raise MpesaInvalidParameterException('Amount must be an integer')


		phone_number = format_phone_number(phone_number)
		url = api_base_url() + 'mpesa/stkpush/v1/processrequest'
		passkey = mpesa_config('MPESA_PASSKEY')
		
		# mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')
		# if mpesa_environment == 'sandbox':
		# 	business_short_code = mpesa_config('MPESA_EXPRESS_SHORTCODE')
		# else:
		# 	business_short_code = mpesa_config('MPESA_SHORTCODE')

		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		password = base64.b64encode((str(business_short_code) + passkey + timestamp).encode('ascii')).decode('utf-8') 

		party_a = phone_number
		party_b = business_short_code

		data = {
			'BusinessShortCode': business_short_code,
			'Password': password,
			'Timestamp': timestamp,
			'TransactionType': transaction_type,
			'Amount': amount,
			'PartyA': party_a,
			'PartyB': party_b,
			'PhoneNumber': phone_number,
			'CallBackURL': callback_url,
			'AccountReference': account_reference,
			'TransactionDesc': transaction_desc
		}

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))

	def b2c_payment(self, phone_number, amount, transaction_desc, callback_url, occassion, command_id):
		"""
		Attempt to perform a business payment transaction
		Args:
			phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
			amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
			transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
			call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
			occassion (str) -- Any additional information to be associated with the transaction.
		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response
		
		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
		"""

		if str(transaction_desc).strip() == '':
			raise MpesaInvalidParameterException('Transaction description cannot be blank')
		if not isinstance(amount, int):
			raise MpesaInvalidParameterException('Amount must be an integer')

		phone_number = format_phone_number(phone_number)
		url = api_base_url() + 'mpesa/b2c/v1/paymentrequest'

		business_short_code = mpesa_config('MPESA_SHORTCODE')

		party_a = business_short_code
		party_b = phone_number
		initiator_username = mpesa_config('MPESA_INITIATOR_USERNAME')
		initiator_security_credential = encrypt_security_credential(mpesa_config('MPESA_INITIATOR_SECURITY_CREDENTIAL'))

		data = {
			'InitiatorName': initiator_username,
			'SecurityCredential': initiator_security_credential,
			'CommandID': command_id,
			'Amount': amount,
			'PartyA': party_a,
			'PartyB': party_b,
			'Remarks': transaction_desc,
			'QueueTimeOutURL': callback_url,
			'ResultURL': callback_url,
			'Occassion':  occassion
		}

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))

	def business_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'BusinessPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)

	def salary_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'SalaryPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)

	def promotion_payment (self, phone_number, amount, transaction_desc, callback_url, occassion):
		command_id = 'PromotionPayment'
		return self.b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id)



	def c2b_register_url(self, ShortCode, ResponseType, ConfirmationURL, ValidationURL):

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		data = {
			"ShortCode": ShortCode,
			"ResponseType": ResponseType,
			"ConfirmationURL": ConfirmationURL,
			"ValidationURL": ValidationURL
		}

		url = api_base_url() + 'mpesa/c2b/v1/registerurl'

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))


	def c2b(self, phone_number, business_short_code, account_number, amount, transaction_type):
		"""
		Attempt to send an STK prompt to customer phone
		Args:
			command_id (String) -- This is a unique identifier of the transaction type:
								   There are two types of these Identifiers:
								   CustomerPayBillOnline:
								   This is used for Pay Bills shortcodes.
								   CustomerBuyGoodsOnline: 
								   This is used for Buy Goods shortcodes.

			phone_number (str): -- This is the phone number initiating the C2B transaction
			amount (int) -- This is the amount being transacted. The parameter expected is a numeric value.
			BillRefNumber (str) -- This is used on CustomerPayBillOnline option only. 
								   This is where a customer is expected to enter a unique bill identifier, e.g an Account Number. 
			ShortCode (str) -- 	This is the Short Code receiving the amount being transacted. 6 characters
			
		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response
		
		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
		"""

		if str(transaction_type).strip() == '':
			error = {"detail": ["Transaction type cannot be blank"]}
			return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			# raise MpesaInvalidParameterException('Account reference cannot be blank')
		# if str(transaction_desc).strip() == '':
		# 	error = {"detail": ["Transaction description cannot be blank"]}
		# 	return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			# raise MpesaInvalidParameterException('Transaction description cannot be blank')
		if not isinstance(amount, int):
			error = {"detail": ["Amount must be an integer"]}
			# return RestResponse(error, status=status.HTTP_400_BAD_REQUEST)
			raise MpesaInvalidParameterException('Amount must be an integer')


		phone_number = format_phone_number(phone_number)
		url = api_base_url() + 'mpesa/c2b/v1/simulate'
		command_id = transaction_type

		data = {
			'CommandID': command_id,
			'Amount': amount,
			'Msisdn': phone_number,
			'BillRefNumber': account_number,
			'ShortCode': business_short_code
		}

		headers = {
			'Authorization': 'Bearer ' + mpesa_access_token(),
			'Content-type': 'application/json'
		}

		try:
			r = requests.post(url, json=data, headers=headers)
			response = mpesa_response(r)
			return response
		except requests.exceptions.ConnectionError:
			raise MpesaConnectionError('Connection failed')
		except Exception as ex:
			raise MpesaConnectionError(str(ex))