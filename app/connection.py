import os

from sqlalchemy import create_engine


def get_engine():
    host = os.environ["MYSQL_HOST"]
    user = os.environ["MYSQL_USER"]
    password = os.environ["MYSQL_PASSWORD"]
    database = os.environ["MYSQL_DATABASE"]

    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}", pool_recycle=3600 # noqa E501
    )


def run_stmt(stmt):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result
    except Exception as e:
        err = {"detail": e}
        print("Error on run_stmt", err)
        return None
