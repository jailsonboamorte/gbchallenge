from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pprint import pprint

from sqlalchemy import column, insert
from sqlalchemy import table as table_sa

from app.connection import run_stmt
from app.schemas import spotify_tables
from app.spotify import extract_gb_episodes, get_all_episodes, get_podcasts
from app.truncate_tables import truncate_tables


def save_data(table, data):

    try:
        columns_list = [column(col) for col in data[0].keys()]
        table_object = table_sa(table, *columns_list)

        stmt = insert(table_object).values(data)
        result = run_stmt(stmt)
        return result.rowcount

    except Exception as e:
        err = {"table": table, "detail": e}
        print("Error on save_data", err)


def process_spotify_data():
    try:

        podcasts = get_podcasts()

        episodes = []
        gb_episodes = []

        summary = {}

        func = partial(get_all_episodes)
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    func, pod_cast["id"], pod_cast["total_episodes"]
                )  # noqa E501
                for pod_cast in podcasts
            ]

            for future in as_completed(futures):
                podcast_id, podcast_episodes = future.result()
                gb_podcast_episodes = extract_gb_episodes(podcast_episodes)

                episodes = episodes + podcast_episodes
                gb_episodes = gb_episodes + gb_podcast_episodes

                summary[podcast_id] = {
                    "episodes": {
                        "qty": len(podcast_episodes),
                        "qty_gb": len(gb_podcast_episodes),
                    }
                }

        summary["source"] = {
            "podcast": {"qty": len(podcasts)},
            "gb_episodes": {"qty": len(gb_episodes)},
            "episodes": {"qty": len(episodes)},
        }

        qty_podcasts = save_data("spotify_podcast", podcasts)
        qty_episodes = save_data("spotify_podcast_episodes", episodes)
        qty_gb_episodes = save_data("spotify_gb_podcast_episodes", gb_episodes)

        summary["saved"] = {
            "podcasts": {"qty": qty_podcasts},
            "episodes": {"qty": qty_episodes},
            "gb_episodes": {"qty": qty_gb_episodes},
        }

    except Exception as e:
        err = {"detail": e}
        print("Error on process_spotify_data", err)

    return summary


if __name__ == "__main__":
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"START AT: {now}")
    truncate_tables(spotify_tables)
    pprint(process_spotify_data())
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"END AT: {now}")
