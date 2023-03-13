from app.connection import get_connection, get_cursor
from app.schemas import source_tables, target_tables

conn = get_connection()

cursor = get_cursor(conn)

def create_tables(tables):
    try:
        if cursor:
            for table in tables:
                try:
                    create_table = tables[table]
                    cursor.execute(create_table)
                    print("Created", table)
                except Exception as e:
                    print("Error while create table", e)
                    print("table", table)

    except Exception as e:
        print("Error on connection", e)

if __name__ == "__main__":
    create_tables(source_tables)
    create_tables(target_tables)