from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlalchemy import text

from app.connection import run_stmt
from app.schemas import source_tables as all_tables


def truncate_table(table):
    try:
        if run_stmt(text(f"truncate {table}")):
            print("Truncated", table)
    except Exception as e:
        print("Error on truncate_table", e)


def truncate_tables(tables):
    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(truncate_table, table) for table in tables
            ]  # noqa E501

            for future in as_completed(futures):
                future.result()

    except Exception as e:
        print("Error on truncate_tables", e)


if __name__ == "__main__":
    truncate_tables(all_tables)
