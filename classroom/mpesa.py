import requests
import json
import datetime
import base64
from classroom.utils import get_access_token

def stk_push_request(phone_number=254716454678, amount=5):
    access_token = get_access_token()  # Get access token

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    business_shortcode = "174379"  # Use your Paybill/Till number
    passkey = "YOUR_PASSKEY"

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{business_shortcode}{passkey}{timestamp}".encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  
        "PartyB": business_shortcode,  
        "PhoneNumber": phone_number,
        "CallBackURL": "https://a013-196-207-175-179.ngrok-free.app/mpesa/callback/",
        "AccountReference": "CarParking",
        "TransactionDesc": "Parking Payment"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()  # Return API response

