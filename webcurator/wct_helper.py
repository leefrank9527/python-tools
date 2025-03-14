import requests

SERVER_URL = "http://localhost:8080"


def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    ret = requests.post(url=SERVER_URL + '/wct/auth/v1/token', headers=headers, data='username=lql&password=1qaz@WSX')
    if ret.ok:
        return ret.text
    else:
        return None
