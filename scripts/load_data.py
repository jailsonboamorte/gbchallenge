import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pprint import pprint

import pandas as pd

from app.connection import get_connection, get_cursor
from app.schemas import tables as all_tables
from app.truncate_tables import truncate_tables

data_path = "gb_inputs/data"


def format_date(str_date):
    return str_date.replace("T", " ").split(".")[0]


def insert(table, df):
    qty = 0
    sql = ""
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        columns = ", ".join(df.columns)
        placeholder = ",".join(["'{}'" for v in df.columns])

        value_list = []
        for i, row in df.iterrows():

            if "created_at" in row:
                row["created_at"] = format_date(row["created_at"])

            if "investment_completed_at_timestamp" in row:
                row["investment_completed_at_timestamp"] = format_date(
                    row["investment_completed_at_timestamp"]
                )

            if "action_timestamp" in row:
                row["action_timestamp"] = format_date(row["action_timestamp"])

            values = ["null" if v == "None" else v for v in row]

            value_list.append(f"({placeholder})".format(*values))
            # print(sql)

        str_values = ",".join(value_list).replace("'null'", "null")
        sql = f"INSERT INTO {table} ({columns}) VALUES {str_values};"

        cursor.execute(sql)
        conn.commit()

        qty = len(value_list)
    except Exception as e:
        err = {"table": table, "detail": e, "query": sql}
        print("Error on insert", err)

    return qty


def process_chunk(table, df):
    try:
        return insert(table, df)
    except Exception as e:
        print("Error on process_file", e)


def process_file(table, file):
    try:        
        path = f"{data_path}/{table}/{file}"
        df = pd.read_excel(path, index_col=False)  # noqa E501
        qty_inserted = process_chunk(table, df)
        return table, qty_inserted

    except Exception as e:
        print("Error on process_file", e)


def process_files(table):
    try:

        path = f"{data_path}/{table}"
        files = os.listdir(path)

        qty_inserted = 0

        func = partial(process_file, table)

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(func, file)
                for file in files
                if file.endswith(".xlsx")  # noqa E501
            ]

            for future in as_completed(futures):
                table, qty = future.result()
                qty_inserted = qty_inserted + qty

        return table, qty_inserted

    except Exception as e:
        print("Error on process_files", e)


def load_data(tables):
    try:
        summary = {}

        with ThreadPoolExecutor() as executor:

            futures = [
                executor.submit(process_files, table) for table in tables
            ]  # noqa E501

            for future in as_completed(futures):
                table, qty_inserted = future.result()

                print(table, qty_inserted)
                if table in summary:
                    summary[table] = summary[table] + qty_inserted
                else:
                    summary[table] = qty_inserted

        pprint(summary)

    except Exception as e:
        print("Error on load_data", e)


truncate_tables(all_tables)
load_data(all_tables)
