import requests
from time import time
from utils import helper

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


def get_all():
    offset = 0
    searchConditions = {
        "targetId": 7,
        "url": 'https://*.nz/',
    }

    filter_condition = {
        "filter": searchConditions,
        "page": 0,
        "limit": 10
    }

    token = get_token()
    if token is None:
        print("Failed to authenticate")
        return None

    start_time = time()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    ret = requests.get(
        url=SERVER_URL + '/wct/api/v1/permissions',
        headers=headers,
        json=filter_condition
    )

    end_time = time()

    time_used = end_time - start_time

    if not ret.ok:
        print(f"Error:  {ret.status_code} {ret.text}")
        return
    helper.print_json(ret.json())
    print(f"time_used: {time_used}")


def get_by_id(oid: int):
    token = get_token()
    if token is None:
        print("Failed to authenticate")
        return None

    start_time = time()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    ret = requests.get(
        url=SERVER_URL + f'/wct/api/v1/permissions/{oid}',
        headers=headers,
    )

    end_time = time()

    time_used = end_time - start_time

    if not ret.ok:
        print(f"Error:  {ret.status_code} {ret.text}")
        return
    print(ret.text)
    print(f"time_used: {time_used}")


def main():
    get_all()

    get_by_id(171)


if __name__ == '__main__':
    main()
