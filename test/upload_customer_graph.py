import json
import time

import pandas as pd

from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

import pandas as pd

df = pd.read_csv('./customer.csv')

def nebula_test():
    client = None
    try:
        config = Config()
        config.max_connection_pool_size = 2
        # init connection pool
        connection_pool = ConnectionPool()
        assert connection_pool.init([("127.0.0.1", 9669)], config)

        # get session from the pool
        client = connection_pool.get_session("root", "nebula")
        assert client is not None

        client.execute('USE cdp_customer_identity;')

        for row in df.iterrows():
            customer_vertex = 'INSERT VERTEX `customer` (`name`, `gender`, `age`) VALUES "{}":("{}","{}", {});'.format(row[1][0], row[1][1], row[1][2], row[1][3])
            print(customer_vertex)
            resp = client.execute(customer_vertex)
            print(resp)
            phone_vertex = 'INSERT VERTEX `phone` () VALUES "{}":();'.format(row[1][7])
            resp = client.execute(phone_vertex)
            print(resp)
            has_phone_edge = 'INSERT EDGE `has_phone` () VALUES "{}"->"{}":();'.format(row[1][0], row[1][7])
            resp = client.execute(has_phone_edge)
            print(resp)

    except Exception:
        import traceback

        print(traceback.format_exc())
        if client is not None:
            client.release()
        exit(1)

if __name__ == "__main__":
    nebula_test()