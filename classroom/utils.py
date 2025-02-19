import requests

# Function to get access token from Daraja API
def get_access_token():
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    return response.json().get("access_token")
