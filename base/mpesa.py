import requests
from requests.auth import HTTPBasicAuth
import json
import requests

key = "dsxA8QGfXN5MGxSwv5RzdueGodvd3KKc"
secret = "WVjn4GiaSgPFPk5t"

def ac_token():
    mpesa_auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        data = (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(key, secret))).json()
    
        return data['access_token']
    except:
        print("Error")