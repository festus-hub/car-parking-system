import requests

# Function to get access token from Daraja API
def get_access_token():
    consumer_key = "zyf22CG0suhcx2z8mvruUauQ5EsAqTY7DGL91CRjWgrQzBRC"
    consumer_secret = "7SThoERwBcOYmIEnnA5iKBGL5yJ5OspDq2hbEOZaQgkLryX6R91yGPcVt1uLAr7v"
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    return response.json().get("access_token")
