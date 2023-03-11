from app.connection import get_connection, get_cursor
from app.schemas import tables as all_tables

conn = get_connection()
cursor = get_cursor(conn)


def truncate_tables(tables):
    try:

        if cursor:

            for table in tables:
                print("Truncate", table)
                try:
                    cursor.execute(f"truncate {table}")
                    print("Truncated", table)
                except Exception as e:
                    print("Error while truncate table", e)
                    print("table", table)

    except Exception as e:
        print("Error on connection", e)

if __name__ == "__main__":
    truncate_tables(all_tables)