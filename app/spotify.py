import os

import requests
import base64


host = "https://accounts.spotify.com"


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


def get_podcasts():
    try:
        query = "data hackers"
        host = "https://api.spotify.com/"
        path = "v1/search"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + get_token(),
        }

        params = {"q": query, "type": "show", "limit": 50, "market": "US"}
        url = f"{host}{path}"
        response = requests.get(url, params=params, headers=headers)
        items = response.json()["shows"]["items"]
        podcasts = []
        for item in items:                 
            podcasts.append( {
                "id": item["id"],
                "name": item["name"],
                "description": item["description"],
                "total_episodes":item["total_episodes"]
            })
        return podcasts        

    except Exception as e:
        print("Error on get_podcasts", e)
        return None
