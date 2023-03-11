from app.connection import get_connection, get_cursor
from app.schemas import tables as all_tables

conn = get_connection()

cursor = get_cursor(conn)


def drop_tables(tables):
    try:

        if cursor:

            for table in tables:
                try:
                    cursor.execute(f"DROP table IF EXISTS {table}")
                    print("Dropped", table)
                except Exception as e:
                    print("Error while drop table", e)
                    print("table", table)

    except Exception as e:
        print("Error on connection", e)

if __name__ == "__main__":
    drop_tables(all_tables)