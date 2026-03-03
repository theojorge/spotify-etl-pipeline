import logging

from airflow.decorators import task
from airflow.exceptions import AirflowException
from scripts.utils.tokens.token import get_access_token


@task
def authorize_user() -> str:
    """
    Returns access token using refresh token.
    No longer uses Selenium.
    """
    try:
        logging.info("Getting access token via refresh token...")
        access_token = get_access_token()
        logging.info("Access token retrieved successfully")
        return access_token
    except Exception as e:
        logging.error(f"Error getting access token: {e}")
        raise AirflowException(f"Error getting access token: {e}")