import logging
from typing import Any, Dict, Optional

from steam_data.base import SteamDataSource
from steam_data.store_html import StoreHtmlDataSource
from steam_data.steam_app_details import SteamAppDetailsDataSource
from steam_utils.utils import extract_app_id_from_url

logger = logging.getLogger(__name__)


class CombinedSteamDataSource(SteamDataSource):
    def __init__(self):
        self.store_html_source = StoreHtmlDataSource()
        self.steampowered_api_source = SteamAppDetailsDataSource()

    def get_data(self, identifier, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetches game data by combining results from StoreHtmlDataSource and SteamAppDetailsDataSource.
        Prioritizes data from StoreHtmlDataSource.
        """
        combined_data: Dict[str, Any] = {}
        app_id: Optional[int] = None

        # Determine app_id from identifier up front
        if isinstance(identifier, str):
            if identifier.isdigit():
                app_id = int(identifier)
            else:
                app_id = extract_app_id_from_url(identifier)
                if not app_id:
                    logger.warning(f"Invalid identifier: {identifier}")
                    return None
        elif isinstance(identifier, int):
            app_id = identifier
        else:
            logger.warning(f"Invalid identifier: {identifier}")
            return None

        # 1. Try to get data from StoreHtmlDataSource
        logger.info(f"Attempting to fetch data from StoreHtmlDataSource for {identifier}")
        html_data = self.store_html_source.get_data(identifier, **kwargs)

        if html_data:
            logger.info("Successfully retrieved data from StoreHtmlDataSource.")
            combined_data.update(html_data)
        else:
            logger.warning("StoreHtmlDataSource failed to retrieve data.")

        # 2. Try to get data from SteamAppDetailsDataSource if app_id is available
        if app_id:
            logger.info(f"Attempting to fetch data from SteamAppDetailsDataSource for App ID: {app_id}")
            api_data = self.steampowered_api_source.get_data(app_id, **kwargs)
            if api_data:
                logger.info("Successfully retrieved data from SteamAppDetailsDataSource.")
                # Merge API data, prioritizing existing HTML data
                # This is a simple merge, more sophisticated merging might be needed based on specific fields
                for key, value in api_data.items():
                    if key not in combined_data or \
                            not combined_data.get(key) or \
                            (isinstance(combined_data.get(key), str) and isinstance(value, dict)):
                        combined_data[key] = value
            else:
                logger.warning(f"SteamAppDetailsDataSource failed to retrieve data for App ID: {app_id}.")
        else:
            logger.warning("Could not determine App ID for SteamAppDetailsDataSource.")

        if not combined_data:
            logger.error(f"Failed to retrieve any data for identifier: {identifier}")
            return None

        return combined_data
