import requests
from time import time
import orjson
import pandas as pd

SERVER_URL = "http://localhost:8080"

MAX_ROWS = 200000


def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    ret = requests.post(url=SERVER_URL + '/wct/auth/v1/token', headers=headers, data='username=lql&password=1qaz@WSX')
    if ret.ok:
        return ret.text
    else:
        return None


def _hit(limit: int):
    # offset = int(MAX_ROWS / 2)
    offset = 0
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
    print(f"limit-{limit}|{limit}|{time_used}|{len(content)}")
    return time_used, len(content)


class PerfTest:
    time_usage = {}

    def __init__(self):
        pass

    def hit(self, limit):
        ret = _hit(limit)
        if ret is None:
            return
        label = f'label{limit}'
        time_used, _ = ret

        if label not in self.time_usage:
            self.time_usage[label] = []
        self.time_usage[label].append(time_used)

    def run_one_round(self):
        for idx in range(MAX_ROWS):
            if 0 < idx < 100:
                if idx % 10 != 0:
                    continue
                else:
                    self.hit(idx)
            elif 100 <= idx < 1000:
                if idx % 100 != 0:
                    continue
                else:
                    self.hit(idx)
            elif 1000 <= idx < 10000:
                if idx % 1000 != 0:
                    continue
                else:
                    self.hit(idx)
            elif 10000 <= idx < 100000:
                if idx % 10000 != 0:
                    continue
                else:
                    self.hit(idx)
            elif 100000 <= idx < 1000000:
                if idx % 100000 != 0:
                    continue
                else:
                    self.hit(idx)
            else:
                continue


def main():
    handler = PerfTest()
    max_loop = 5
    for idx in range(max_loop):
        handler.run_one_round()

    df = pd.DataFrame(handler.time_usage)

    mean_per_row = df.mean()
    print(mean_per_row)
    # mean_per_row.to_frame().T.to_csv('postgres-simplified-entities-mean.csv', index=False)
    df.loc[len(df)] = mean_per_row

    print(df)
    df.to_csv('mysql-simplified-entities-offset-middle.csv', index=False)


if __name__ == '__main__':
    main()
