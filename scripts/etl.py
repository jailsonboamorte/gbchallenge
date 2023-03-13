from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pprint import pprint

import pandas as pd
from sqlalchemy import column, insert
from sqlalchemy import table as table_sa
from sqlalchemy import text

from app.connection import get_engine, run_stmt
from app.schemas import target_tables
from app.truncate_tables import truncate_tables

query_map = {
    "sales_by_year_month": "queries/sales_by_ano_and_mes.sql",
    "sales_by_brand_category": "queries/sales_by_marca_and_linha.sql",
    "sales_by_brand_year_month": "queries/sales_by_marca_ano_and_mes.sql",
    "sales_by_category_year_month": "queries/sales_by_linha_ano_mes.sql",
}


def process_chunk(table, df):
    try:

        columns_list = [column(col) for col in df.columns]
        table_object = table_sa(table, *columns_list)

        values = df.to_dict("records")
        stmt = insert(table_object).values(values)
        result = run_stmt(stmt)
        return result.rowcount
    except Exception as e:
        print("Error on process_chunk", e)
        return None


def process_query(table):
    try:

        file = query_map[table]
        sql = None

        with open(file, "r") as f:
            sql = text(f.read())

        if sql is not None:
            engine = get_engine()
            conn = engine.connect()

            chunks = pd.read_sql_query(sql, conn, chunksize=10000)

            func = partial(process_chunk, table)
            qty_inserted = 0
            with ThreadPoolExecutor() as executor:

                futures = [executor.submit(func, chunk) for chunk in chunks]
                for future in as_completed(futures):
                    qty_inserted = qty_inserted + future.result()

        return table, qty_inserted
    except Exception as e:
        err = {"table": table, "detail": e, "query": sql}
        print("Error on process_query", err)
        return table, 0


def process_queries():
    with ThreadPoolExecutor() as executor:

        futures = [
            executor.submit(process_query, process)
            for process in query_map.keys()  # noqa E501
        ]

        summary = {}

        for future in as_completed(futures):
            file, qty_inserted = future.result()
            # print(file, qty_inserted)
            summary[file] = qty_inserted

        pprint(summary)


if __name__ == "__main__":
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"START AT: {now}")
    truncate_tables(target_tables)
    print("---------")
    process_queries()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"END AT: {now}")
