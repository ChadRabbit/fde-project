import sqlite3
import pandas as pd


def run_sql(query):
    conn = sqlite3.connect("data.db")
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return str(e)
