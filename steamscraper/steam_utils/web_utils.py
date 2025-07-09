from typing import Optional

import requests
import logging
import os

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

def get_proxies_from_env() -> dict:
    """
    Reads proxy settings from environment variables HTTP_PROXY and HTTPS_PROXY.
    Returns a dictionary suitable for the 'proxies' argument in requests.
    """
    proxies = {}
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')

    if http_proxy:
        proxies['http'] = http_proxy
    if https_proxy:
        proxies['https'] = https_proxy
    return proxies

def fetch_steam_store_html(url: str, lang: str = 'english', headers: Optional[dict] = None, cookies: Optional[dict] = None, proxies: Optional[dict] = None) -> Optional[str]:
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

    # Get proxies from environment variables
    env_proxies = get_proxies_from_env()
    # Merge with provided proxies, giving precedence to env_proxies
    if env_proxies:
        if proxies:
            proxies.update(env_proxies)
        else:
            proxies = env_proxies

    logger.info(f"Fetching HTML from: {url}")
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10, proxies=proxies)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None