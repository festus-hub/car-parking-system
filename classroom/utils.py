import requests
import base64
from django.conf import settings
from datetime import datetime
from requests.auth import HTTPBasicAuth

def get_mpesa_access_token():
    """ Get M-Pesa API access token """
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    
    return response.json().get("access_token")

def stk_push_request(phone_number, amount, order_id):
    """ Initiate M-Pesa STK Push request """
    access_token = get_mpesa_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # Customer's phone number (format: 2547XXXXXXXX)
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"Order-{order_id}",
        "TransactionDesc": "Parking Payment"
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)

    return response.json()
