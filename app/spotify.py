import os

import requests
import base64
import math

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

host = "https://accounts.spotify.com"


EPISODES_LIMIT = 50
PODECAST_LIMIT = 50


def get_token():

    try:
        path = "/api/token"

        client_id = os.environ["SPOTIFY_CLIENT_ID"]
        client_secret = os.environ["SPOTIFY_CLIENTE_SECRET"]

        message = f"{client_id}:{client_secret}"
        messageBytes = message.encode("ascii")
        base64Bytes = base64.b64encode(messageBytes)
        base64Message = base64Bytes.decode("ascii")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64Message}",
        }

        data = {"grant_type": "client_credentials"}

        url = f"{host}{path}"

        response = requests.post(url, data=data, headers=headers)
        token = response.json()["access_token"]
        return token
    except Exception as e:
        print("Error on get_token", e)
        return None


TOKEN_SPOTIFY = get_token()


def extract_episodes(show_id, episodes):

    try:
        episodes_list = []
        for episode in episodes:
            episodes_list.append(
                {
                    "id": episode["id"],
                    "podcast_id": show_id,
                    "name": episode["name"],
                    "description": episode["description"],
                    "release_date": episode["release_date"],
                    "duration_ms": episode["duration_ms"],
                    "language": episode["language"],
                    "explicit": episode["explicit"],
                    "type": episode["type"],
                }
            )
        return episodes_list
    except Exception as e:
        print("Error on extract_episodes", e)
        return None


def get_podcasts():
    try:
        query = "data hackers"
        host = "https://api.spotify.com"
        path = "/v1/search"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + TOKEN_SPOTIFY,
        }

        params = {
            "q": query,
            "type": "show",
            "limit": PODECAST_LIMIT,
            "market": "BR",
        }  # noqa E501
        url = f"{host}{path}"
        response = requests.get(url, params=params, headers=headers)
        items = response.json()["shows"]["items"]
        podcasts = []
        for item in items:
            podcasts.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "description": item["description"],
                    "total_episodes": item["total_episodes"],
                }
            )
        return podcasts

    except Exception as e:
        print("Error on get_podcasts", e)
        return None


def extract_gb_episodes(episodes):
    try:
        return [
            episode
            for episode in episodes
            if "boticário" in episode["description"].lower()
        ]
    except Exception as e:
        print("Error on extract_gb_episodes", e)
        return None


def get_episodes(show_id, offset):
    try:
        host = "https://api.spotify.com"
        path = f"/v1/shows/{show_id}/episodes"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + TOKEN_SPOTIFY,
        }

        params = {"limit": EPISODES_LIMIT, "offset": offset, "market": "BR"}
        url = f"{host}{path}"
        response = requests.get(url, params=params, headers=headers)
        items = response.json()["items"]

        offset = response.json()["offset"]

        """
        total = response.json()["total"]
        next = response.json()["next"]
        print({
            "total": total,
            "offset": offset,
            "items": len(items),
            "next": next
            }) #noqa E501
        """

        return items

    except Exception as e:
        print("Error on get_episodes", e)
        return []


def get_offsets(total_episodes):
    offsets = [0]
    limit_page = total_episodes / EPISODES_LIMIT
    for n in range(0, math.ceil(limit_page), EPISODES_LIMIT):  # noqa E501
        offsets.append(n + EPISODES_LIMIT)

    return offsets


def get_all_episodes(show_id, total_episodes):
    offsets = get_offsets(total_episodes)
    all_episodes = []
    try:

        func = partial(get_episodes, show_id)
        with ThreadPoolExecutor() as executor:

            futures = [executor.submit(func, n) for n in offsets]

            for future in as_completed(futures):
                episodes = future.result()
                all_episodes = all_episodes + extract_episodes(
                    show_id, episodes
                )  # noqa E501

        return show_id, all_episodes
    except Exception as e:
        print("Error on get_all_episodes", e)
        return show_id, []
