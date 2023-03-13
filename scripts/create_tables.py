from sqlalchemy import text

from app.connection import run_stmt
from app.schemas import source_tables, target_tables


def create_tables(tables):
    try:
        for table in tables:
            try:
                create_table = tables[table]
                if run_stmt(text(create_table)):
                    print("Created", table)
            except Exception as e:
                print("Error while create table", e)
                print("table", table)

    except Exception as e:
        print("Error on connection", e)


if __name__ == "__main__":
    create_tables(source_tables)
    create_tables(target_tables)
