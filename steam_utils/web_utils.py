from typing import Optional

import requests
import logging

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
DEFAULT_COOKIES = {
    'birthtime': '568022401',
    'mature_content': '1',
    'lastagecheckage': '1-January-1990'
}
DEFAULT_HEADERS = {
    'User-Agent': DEFAULT_USER_AGENT,
    'Referer': 'https://www.google.com/',
    'Host': 'store.steampowered.com'
}

def fetch_steam_store_html(url: str, lang: str = 'english', headers=None, cookies=None) -> Optional[str]:
    """
    Fetches the HTML content of a Steam store page with appropriate headers.

    Args:
        url: The URL of the Steam store page.
        lang: The language for the request.

    Returns:
        The HTML content as a string if successful, None otherwise.
        :param cookies: Cookies to use for the request.
        :param url: The URL of the Steam store page.
        :param lang: The language for the request.
        :param headers: Headers to use for the request.
    """
    if cookies is None:
        cookies = DEFAULT_COOKIES
    if headers is None:
        headers = DEFAULT_HEADERS
    params = {'l': lang}

    logger.info(f"Fetching HTML from: {url}")
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None