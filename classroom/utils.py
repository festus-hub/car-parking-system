import requests
from django.conf import settings
import base64

def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers)

    response_data = response.json()
    return response_data.get("access_token", None)
