"""
Steam Scraper - Steam game data scraper and parser

A Python package for scraping and parsing Steam game data.
"""

__version__ = "0.1.0"

# Import main classes and functions for easy access
from .steam_data.combined_data import *
from .steam_data.steam_app_details import *
from .steam_data.store_html import *
from .steam_utils import *

# Make main classes available at package level
__all__ = [
    'CombinedSteamDataSource',
    'SteamAppDetailsDataSource', 
    'StoreHtmlDataSource',
    'fetch_steam_store_html',
    'SUPPORTED_LANGUAGES',
]
