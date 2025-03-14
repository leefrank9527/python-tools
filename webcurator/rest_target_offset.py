import requests
from time import time

from utils import helper
from webcurator import wct_helper


def get_all():
    offset = 1
    limit = 1
    searchConditions = {
        "targetId": None,
        "name": None,
        "seed": None,
        "description": None,
        "groupName": None,
        "nonDisplayOnly": False
    }

    filter_condition = {
        "filter": searchConditions,
        "offset": offset,
        "limit": limit,
        "sortBy": 'creationDate,asc'
    }

    token = wct_helper.get_token()
    if token is None:
        print("Failed to authenticate")
        return None

    start_time = time()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    ret = requests.get(
        url=wct_helper.SERVER_URL + '/wct/api/v1/targets',
        headers=headers,
        json=filter_condition
    )

    end_time = time()

    time_used = end_time - start_time

    if not ret.ok:
        print(f"Error: {limit} {ret.status_code} {ret.text}")
        return
    content = ret.json()
    helper.print_json(content)


def main():
    get_all()


if __name__ == '__main__':
    main()
