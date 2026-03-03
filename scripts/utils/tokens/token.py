import base64
import logging

import requests

from airflow.exceptions import AirflowException
from config.appconfig import app_config


def get_access_token():
    """Generates access token using refresh token"""

    CLIENT_ID = app_config.get_spotify_client_id()
    CLIENT_SECRET = app_config.get_spotify_client_secret()

    refresh_token = app_config.get_spotify_refresh_token()
    if not refresh_token:
        raise AirflowException("SPOTIFY_REFRESH_TOKEN not set in .env")

    credentials = "%s:%s" % (CLIENT_ID, CLIENT_SECRET)
    base64_encoded = base64.b64encode(credentials.encode()).decode()

    logging.info("Refreshing access token...")
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        headers={"Authorization": "Basic " + base64_encoded},
    )

    response_json = response.json()
    access_token = response_json.get("access_token")

    if not access_token:
        raise AirflowException(f"Failed to get access token: {response_json}")

    logging.info("Access token retrieved successfully")
    return access_token