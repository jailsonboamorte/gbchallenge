from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pprint import pprint

from app.schemas import spotify_tables
from app.spotify import extract_gb_episodes, get_all_episodes, get_podcasts
from app.truncate_tables import truncate_tables


def process_spotify_data():
    try:

        episodes = []
        gb_episodes = []

        podcasts = get_podcasts()
        summary = {"podcast": {"qty": len(podcasts)}}
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

        summary["gb_episodes"] = {"qty": len(gb_episodes)}

        # print(gb_episodes[:1])
        # print("-----")
        # pprint(episodes[:1])

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
