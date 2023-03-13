from sqlalchemy import text

from app.connection import run_stmt
from app.schemas import source_tables, target_tables


def drop_tables(tables):
    try:

        for table in tables:
            try:
                if run_stmt(text(f"DROP table IF EXISTS {table}")):
                    print("Dropped", table)
            except Exception as e:
                print("Error while drop table", e)
                print("table", table)

    except Exception as e:
        print("Error on connection", e)


if __name__ == "__main__":
    drop_tables(source_tables)
    drop_tables(target_tables)
