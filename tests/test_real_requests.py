
import pytest
import os
import sys

from steamscraper.steam_data.store_html import StoreHtmlDataSource
from steamscraper.steam_data.steam_app_details import SteamAppDetailsDataSource
from steamscraper.steam_data.combined_data import CombinedSteamDataSource

# --- Real Request Tests ---
# These tests make actual network requests to Steam's servers.
# They are marked with 'real_request' to be run selectively.

APP_ID_ELDEN_RING = "1245620"
APP_NAME_ELDEN_RING = "ELDEN RING"
LANG = "english"

@pytest.mark.real_request
def test_store_html_real_request():
    """
    Tests StoreHtmlDataSource by fetching and parsing real data from the Steam store page.
    """
    ds = StoreHtmlDataSource()
    data = ds.get_data(APP_ID_ELDEN_RING, lang=LANG)

    assert data is not None, "Failed to fetch data from Steam Store HTML."
    assert data['title'] == APP_NAME_ELDEN_RING
    assert 'developer' in data and 'name' in data['developer']
    assert 'media' in data and 'screenshots' in data['media']
    assert len(data['media']['screenshots']) > 0
    assert 'tags' in data and len(data['tags']) > 0
    assert 'system_requirements' in data

@pytest.mark.real_request
def test_steampowered_api_real_request():
    """
    Tests SteamAppDetailsDataSource by fetching real data from the Steam API.
    """
    ds = SteamAppDetailsDataSource()
    data = ds.get_data(APP_ID_ELDEN_RING, lang=LANG)

    assert data is not None, "Failed to fetch data from Steam API."
    assert data['steam_appid'] == int(APP_ID_ELDEN_RING)
    assert data['name'] == APP_NAME_ELDEN_RING
    assert 'supported_languages' in data
    assert 'release_date' in data
    assert 'pc_requirements' in data and 'minimum' in data['pc_requirements']

@pytest.mark.real_request
def test_combined_data_source_real_request():
    """
    Tests CombinedSteamDataSource by fetching real data from both sources and merging it.
    """
    ds = CombinedSteamDataSource()
    data = ds.get_data(APP_ID_ELDEN_RING, lang=LANG)

    assert data is not None, "Failed to fetch combined data."

    # --- Check for data from both sources ---
    # From StoreHtmlDataSource (prioritized)
    assert data['title'] == APP_NAME_ELDEN_RING
    assert 'developer' in data and data['developer']['name'] == "FromSoftware, Inc."

    # From SteamAppDetailsDataSource (fills in the gaps)
    assert data['steam_appid'] == int(APP_ID_ELDEN_RING)
    assert 'release_date' in data and data['release_date']['date'] is not None

    # --- Check for merged data ---
    # 'title' from HTML should be present, 'name' from API should also be present.
    assert 'title' in data
    assert 'name' in data
    assert data['title'] == data['name']

    # System requirements should be merged
    assert 'system_requirements' in data
    assert 'pc_requirements' in data
    assert 'win' in data['system_requirements']
    assert 'minimum' in data['pc_requirements']
