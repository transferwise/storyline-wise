import os
from typing import Optional

import snowflake.connector
import pandas as pd


def conn(schema: Optional[str] = None):
    con_args = {
        "user": os.getenv("SNOWFLAKE_USER"),
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "authenticator": "externalbrowser",
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "autocommit": True,
    }

    if schema:
        con_args["schema"] = schema

    con = snowflake.connector.connect(**con_args)
    cur = con.cursor()
    return cur


def execute_query(query, c, lowercase: bool = False):
    c.execute(query)

    df = pd.DataFrame(c.fetchall())

    cols = []

    for i in range(df.shape[1]):
        cols.append(c.description[i][0])
    print(cols)
    if lowercase:
        cols = [col.lower() for col in cols]
    df.columns = cols

    return df


class Snowflake:
    def __init__(self, schema: Optional[str] = None):
        self.schema = schema
        self._conn = None

    def execute(self, query: str, lowercase: bool = False):
        if self._conn is None:
            # Lazy init
            self._conn = conn(self.schema)
        try:
            return execute_query(query, self._conn, lowercase)
        except:  # if the connection is closed
            self._conn = conn()
            return execute_query(query, self._conn, lowercase)

    def fetch(self, query: str, lowercase: bool = False):
        return self.execute(query, lowercase)
