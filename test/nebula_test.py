import json
import time

import pandas as pd

from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

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

        client.execute('USE customer_identity;')

        resp = client.execute('MATCH p=(:customer)-[:has_phone]->(phone) WHERE id(phone) == "12121212121" RETURN p;')
        print(resp)

    except Exception:
        import traceback

        print(traceback.format_exc())
        if client is not None:
            client.release()
        exit(1)

if __name__ == "__main__":
    nebula_test()