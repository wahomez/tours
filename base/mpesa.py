import requests
from requests.auth import HTTPBasicAuth
import json
import requests

key = "lQKl01i0an6fv6fGVRVqHOZXbxGZs0Um"
secret = "lQKl01i0an6fv6fGVRVqHOZXbxGZs0Um"

def ac_token():
    mpesa_auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        data = (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(key, secret))).json()
    
        return data['access_token']
    except:
        print("Error")