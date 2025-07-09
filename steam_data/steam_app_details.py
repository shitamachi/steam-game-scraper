from typing import Optional

import requests
import sys
import os
import json
import logging

from steam_data.base import SteamDataSource
from steam_utils.utils import extract_app_id_from_url

logger = logging.getLogger(__name__)

class SteamAppDetailsDataSource(SteamDataSource):
    BASE_URL = "https://store.steampowered.com/api/appdetails"

    def get_data(self, identifier, **kwargs):
        """
        Fetches game data from Steam Storefront API using the appdetails endpoint.
        Identifier can be an App ID or a Steam store URL.
        """
        app_id: Optional[str] = None
        if isinstance(identifier, int) or identifier.isdigit():
            app_id = str(identifier)
        else:
            app_id = extract_app_id_from_url(identifier)

        if not app_id:
            logger.error("Invalid App ID or Steam store URL provided.")
            return None

        lang = kwargs.get('lang', 'english')
        params = {'appids': app_id, 'l': lang}

        logger.info(f"Fetching from Steam Storefront API for App ID: {app_id}")
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data and app_id in data and data[app_id]['success']:
                game_data = data[app_id]['data']
                return game_data
            else:
                logger.error(f"Could not retrieve data for App ID {app_id} or API call was unsuccessful.")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from Steam Storefront API: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from Steam Storefront API: {e}")
            return None
