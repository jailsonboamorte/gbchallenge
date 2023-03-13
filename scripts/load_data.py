import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pprint import pprint

import pandas as pd
from sqlalchemy import column, insert
from sqlalchemy import table as table_sa

from app.connection import run_stmt
from app.schemas import source_tables
from app.truncate_tables import truncate_tables

data_path = "gb_inputs/data"


def insert_data(table, df):

    try:
        columns_list = [column(col) for col in df.columns]
        table_object = table_sa(table, *columns_list)

        values = df.to_dict("records")
        stmt = insert(table_object).values(values)
        result = run_stmt(stmt)
        return result.rowcount

    except Exception as e:
        err = {"table": table, "detail": e}
        print("Error on insert_data", err)


def process_file(table, file):
    try:
        path = f"{data_path}/{table}/{file}"
        df = pd.read_excel(path, index_col=False)  # noqa E501
        qty_inserted = insert_data(table, df)
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
                if table in summary:
                    summary[table] = summary[table] + qty_inserted
                else:
                    summary[table] = qty_inserted

        pprint(summary)

    except Exception as e:
        print("Error on load_data", e)

if __name__ == "__main__":
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'START AT: {now}')
    truncate_tables(source_tables)
    print('---------')
    load_data(source_tables)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'END AT: {now}')
