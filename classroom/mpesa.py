import requests
import json
import datetime
import base64
import logging
from classroom.utils import get_access_token

logger = logging.getLogger(__name__)


def stk_push_request(phone_number=254716454678, amount=1, verbose=False):
    access_token = get_access_token()  # Get access token

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    business_shortcode = "174379"  # Use your Paybill/Till number
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

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

    # Send the POST request to the M-Pesa API
    response = requests.post(api_url, json=payload, headers=headers)

    if verbose:
        logger.info("Response Status Code: %s", response.status_code)
        logger.info("Response Content: %s", response.text)

    # Return the response as a JSON object
    return response.json()  # Return API response
