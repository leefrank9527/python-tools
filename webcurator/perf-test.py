import requests
from time import time
import orjson

SERVER_URL = "http://localhost:8080"


def hit(limit: int):
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
        "offset": 0,
        "limit": limit,
        "sortBy": 'creationDate,asc'
    }

    start_time = time()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'McDNBhpF2wgOYng3NnZQsC8KPYyrLmOwlMjo9zbl8JD8z92yCfnMQCtAOOklL5KV'
    }

    ret = requests.post(
        url=SERVER_URL + '/wct/api/v1/targets',
        headers=headers,
        json=filter_condition
    )

    end_time = time()

    time_used = end_time - start_time

    if not ret.ok:
        print(f"Error: {limit} {ret.status_code} {ret.text}")
        return
    content = orjson.dumps(ret.json())
    # print(content)
    print(f"Mysql|limit-{limit}|{limit}|{time_used}|{len(content)}")


def main():
    for idx in range(200000):
        if 0 < idx < 100:
            if idx % 10 != 0:
                continue
            else:
                hit(idx)
        elif 100 <= idx < 1000:
            if idx % 100 != 0:
                continue
            else:
                hit(idx)
        elif 1000 <= idx < 10000:
            if idx % 1000 != 0:
                continue
            else:
                hit(idx)
        elif 10000 <= idx < 100000:
            if idx % 10000 != 0:
                continue
            else:
                hit(idx)
        elif 100000 <= idx < 1000000:
            if idx % 100000 != 0:
                continue
            else:
                hit(idx)
        else:
            continue


if __name__ == '__main__':
    main()
