import pytest
from bs4 import BeautifulSoup
import os
import sys
from unittest.mock import patch
import requests
import json

from steamscraper.steam_utils.utils import is_valid_steam_url
from steamscraper.steam_data.store_html import StoreHtmlDataSource
from steamscraper.steam_data.steam_app_details import SteamAppDetailsDataSource
from steamscraper.steam_data.combined_data import CombinedSteamDataSource

@pytest.fixture(scope="module")
def store_soup_fixture():
    """Provides a parsed BeautifulSoup object from a cached Steam store HTML file."""
    html_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'Cyberpunk_2077-1091500-schinese.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return BeautifulSoup(html_content, 'html.parser')

@pytest.fixture(scope="module")
def cyberpunk_html_content():
    """Provides the raw HTML content for Cyberpunk 2077."""
    html_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'Cyberpunk_2077-1091500-schinese.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture(scope="module")
def elden_ring_api_json():
    """Provides sample JSON content for Elden Ring from the Steam API."""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'appdetails_1091500_english.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Tests for URL Validation (using utils) ---
@pytest.mark.parametrize("url, expected", [
    ("https://store.steampowered.com/app/1091500/Cyberpunk_2077/", True),
    ("https://store.steampowered.com/app/1245620/ELDEN_RING", True),
    ("http://store.steampowered.com/app/1091500/", False), # Must be https
    ("https://store.steampowered.com/app/1091500", True),
    ("https://store.steampowered.com/app/invalid_id/", False), # App ID must be numeric
    ("https://steamcommunity.com/app/1091500", False), # Must be store.steampowered.com
    ("https://google.com", False),
])
def test_is_valid_steam_url(url, expected):
    """Tests the Steam URL validation logic."""
    match = is_valid_steam_url(url)
    assert bool(match) == expected

# --- Tests for StoreHtmlDataSource ---
def test_store_html_data_source_title(store_soup_fixture):
    """Tests that the game title is correctly parsed from store HTML."""
    ds = StoreHtmlDataSource()
    data = ds._parse_game_details(store_soup_fixture) # Call internal method for testing
    assert data['title'] == "赛博朋克 2077"

def test_store_html_data_source_developer(store_soup_fixture):
    """Tests that the developer info is correctly parsed from store HTML."""
    ds = StoreHtmlDataSource()
    data = ds._parse_game_details(store_soup_fixture)
    assert data['developer']['name'] == "CD PROJEKT RED"
    assert "https://store.steampowered.com/developer/CDPR" in data['developer']['link']

def test_store_html_data_source_screenshots(store_soup_fixture):
    """Tests that screenshots are correctly parsed and counted from store HTML."""
    ds = StoreHtmlDataSource()
    data = ds._parse_game_details(store_soup_fixture)
    assert len(data['media']['screenshots']) > 10 
    assert data['media']['screenshots'][0].startswith("https://shared.fastly.steamstatic.com")

def test_store_html_data_source_tags(store_soup_fixture):
    """Tests that tags are correctly parsed from store HTML."""
    ds = StoreHtmlDataSource()
    data = ds._parse_game_details(store_soup_fixture)
    assert "赛博朋克" in data['tags']
    assert "开放世界" in data['tags']

def test_store_html_data_source_sys_req(store_soup_fixture):
    """Tests that system requirements are parsed from store HTML."""
    ds = StoreHtmlDataSource()
    data = ds._parse_game_details(store_soup_fixture)
    assert 'win' in data['system_requirements']
    assert '操作系统' in data['system_requirements']['win']
    assert '16 GB RAM' in data['system_requirements']['win']['内存']

def test_store_html_data_source_by_appid():
    """Tests fetching data using App ID from StoreHtmlDataSource."""
    ds = StoreHtmlDataSource()
    app_id = "1091500"  # Cyberpunk 2077
    data = ds.get_data(app_id, lang="schinese") # Pass language for localized title
    assert data is not None
    assert data['title'] == "赛博朋克 2077"

# New mocked tests for StoreHtmlDataSource
@patch('requests.get')
def test_store_html_data_source_mocked_success(mock_get, cyberpunk_html_content):
    """Tests StoreHtmlDataSource.get_data with a mocked successful HTTP response."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.text = cyberpunk_html_content
    mock_response.raise_for_status.return_value = None # No HTTP error

    ds = StoreHtmlDataSource()
    app_id = "1091500"
    data = ds.get_data(app_id, lang="schinese")

    assert data is not None
    assert data['title'] == "赛博朋克 2077"
    assert data['developer']['name'] == "CD PROJEKT RED"
    assert "赛博朋克" in data['tags']
    requests.get.assert_called_once_with(
        f"https://store.steampowered.com/app/{app_id}/",
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Host': 'store.steampowered.com' # Added Host header as it's now part of DEFAULT_HEADERS
        },
        cookies={
            'birthtime': '568022401',
            'mature_content': '1',
            'lastagecheckage': '1-January-1990'
        },
        params={'l': 'schinese'},
        timeout=10,
        proxies=None # Added proxies=None
    )

@patch('requests.get')
def test_store_html_data_source_mocked_http_error(mock_get):
    """Tests StoreHtmlDataSource.get_data with a mocked HTTP error response."""
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Not Found")

    ds = StoreHtmlDataSource()
    app_id = "999999999" # Non-existent app ID
    data = ds.get_data(app_id)

    assert data is None
    requests.get.assert_called_once() # Ensure requests.get was called

@patch('requests.get')
def test_store_html_data_source_mocked_invalid_url(mock_get):
    """Tests StoreHtmlDataSource.get_data with an invalid URL format."""
    # requests.get should not be called if the URL is invalid

    ds = StoreHtmlDataSource()
    invalid_url = "https://invalid-steam-url.com/app/123"
    data = ds.get_data(invalid_url)

    assert data is None
    mock_get.assert_not_called()

# --- Tests for SteamAppDetailsDataSource ---
def test_steampowered_api_data_source_by_appid():
    """Tests fetching data using App ID from Storefront API."""
    ds = SteamAppDetailsDataSource()
    app_id = "1091500"  # Cyberpunk 2077
    data = ds.get_data(app_id)
    assert data is not None
    assert data['steam_appid'] == int(app_id)
    assert "name" in data
    assert "about_the_game" in data
    assert "header_image" in data

def test_steampowered_api_data_source_by_url():
    """Tests fetching data using URL from Storefront API."""
    ds = SteamAppDetailsDataSource()
    url = "https://store.steampowered.com/app/1091500/Cyberpunk_2077/"
    data = ds.get_data(url)
    assert data is not None
    assert data['steam_appid'] == 1091500
    assert "name" in data
    assert "about_the_game" in data
    assert "header_image" in data

def test_steampowered_api_data_source_invalid_appid():
    """Tests fetching data with an invalid App ID."""
    ds = SteamAppDetailsDataSource()
    app_id = "99999999999"  # Invalid App ID
    data = ds.get_data(app_id)
    assert data is None

def test_steampowered_api_data_source_language_support():
    """Tests fetching data in a specific language."""
    ds = SteamAppDetailsDataSource()
    app_id = "1091500"
    lang = "schinese"
    data = ds.get_data(app_id, lang=lang)
    assert data is not None
    assert data['steam_appid'] == int(app_id)
    assert data['supported_languages'] is not None
    assert "简体中文" in data['supported_languages'] # Check for Chinese language support

# New mocked tests for SteamAppDetailsDataSource
@patch('requests.get')
def test_steampowered_api_data_source_mocked_success(mock_get, elden_ring_api_json):
    """Tests SteamAppDetailsDataSource.get_data with a mocked successful HTTP response."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    app_id = "1091500" # Using Cyberpunk's ID for the Elden Ring JSON
    mock_response.json.return_value = {
        app_id: {
            "success": True,
            "data": json.loads(elden_ring_api_json)
        }
    }
    mock_response.raise_for_status.return_value = None

    ds = SteamAppDetailsDataSource()
    data = ds.get_data(app_id)

    assert data is not None
    assert data['steam_appid'] == 1091500
    assert data['name'] == "Cyberpunk 2077" # This will be from the mocked JSON
    requests.get.assert_called_once_with(
        "https://store.steampowered.com/api/appdetails",
        params={'appids': app_id, 'l': 'english'},
        timeout=10,
        proxies={} # Added proxies={}
    )

@patch('requests.get')
def test_steampowered_api_data_source_mocked_http_error(mock_get):
    """Tests SteamAppDetailsDataSource.get_data with a mocked HTTP error response."""
    mock_response = mock_get.return_value
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Internal Server Error")

    ds = SteamAppDetailsDataSource()
    app_id = "123456"
    data = ds.get_data(app_id)

    assert data is None
    requests.get.assert_called_once()

@patch('requests.get')
def test_steampowered_api_data_source_mocked_json_decode_error(mock_get):
    """Tests SteamAppDetailsDataSource.get_data with a mocked JSON decode error."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", doc="{}", pos=0)
    mock_response.raise_for_status.return_value = None

    ds = SteamAppDetailsDataSource()
    app_id = "123456"
    data = ds.get_data(app_id)

    assert data is None
    requests.get.assert_called_once()

@patch('requests.get')
def test_steampowered_api_data_source_mocked_api_unsuccessful(mock_get):
    """Tests SteamAppDetailsDataSource.get_data when API returns success: false."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"123456": {"success": False}}
    mock_response.raise_for_status.return_value = None

    ds = SteamAppDetailsDataSource()
    app_id = "123456"
    data = ds.get_data(app_id)

    assert data is None
    requests.get.assert_called_once()

# --- Tests for CombinedSteamDataSource ---
@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value={'title': 'HTML Title', 'price': 'HTML Price', 'developer': {'name': 'HTML Dev'}})
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data', return_value={'name': 'API Name', 'price': 'API Price', 'publisher': {'name': 'API Pub'}})
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_prioritizes_html(mock_extract, mock_api, mock_html):
    """Tests that combined data source prioritizes HTML data."""

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data['title'] == 'HTML Title'
    assert data['price'] == 'HTML Price'
    assert data['developer']['name'] == 'HTML Dev'
    assert data['name'] == 'API Name' # API data should still be merged if key doesn't exist in HTML
    assert data['publisher']['name'] == 'API Pub'

@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value=None)
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data', return_value={'name': 'API Name', 'developer': {'name': 'API Dev'}, 'price': 'API Price'})
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_falls_back_to_api(mock_extract, mock_api, mock_html):
    """Tests that combined data source falls back to API data if HTML data is not available."""

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data['name'] == 'API Name'
    assert data['developer']['name'] == 'API Dev'
    assert data['price'] == 'API Price'
    assert 'title' not in data # Ensure HTML-specific fields are not present if HTML data is None

@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value=None)
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data', return_value=None)
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_no_data(mock_extract, mock_api, mock_html):
    """Tests that combined data source returns None if no data is available from either source."""

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data is None

@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value=None)
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data', return_value={'name': 'API Game', 'release_date': '2023-01-01'})
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_html_fails_api_success(mock_extract, mock_api, mock_html):
    """Tests combined data source when HTML fails but API succeeds."""

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data is not None
    assert data['name'] == 'API Game'
    assert data['release_date'] == '2023-01-01'

@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value={'title': 'HTML Game', 'price': 'Free'})
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data', return_value=None)
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_html_success_api_fails(mock_extract, mock_api, mock_html):
    """Tests combined data source when HTML succeeds but API fails."""

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data is not None
    assert data['title'] == 'HTML Game'
    assert data['price'] == 'Free'
    assert 'name' not in data # API-specific field should not be present

@patch('steam_data.store_html.StoreHtmlDataSource.get_data', return_value={'title': 'HTML Title', 'price': 'HTML Price', 'developer': {'name': 'HTML Dev'}, 'tags': ['HTML Tag1', 'HTML Tag2']})
@patch('steam_data.steam_app_details.SteamAppDetailsDataSource.get_data')
@patch('steam_data.combined_data.extract_app_id_from_url', return_value='123')
def test_combined_data_source_merge_logic(mock_extract, mock_api, mock_html):
    """Tests the merging logic of CombinedSteamDataSource."""
    mock_api.return_value = {
        'name': 'API Name',
        'price': 'API Price (should be overridden)',
        'publisher': {'name': 'API Pub'},
        'tags': ['API Tag1', 'API Tag2'],
        'steam_appid': 123
    }

    ds = CombinedSteamDataSource()
    data = ds.get_data("http://example.com/app/123")

    assert data['title'] == 'HTML Title' # HTML should prioritize
    assert data['price'] == 'HTML Price' # HTML should prioritize
    assert data['developer']['name'] == 'HTML Dev'
    assert data['publisher']['name'] == 'API Pub' # API should fill in missing fields
    assert data['steam_appid'] == 123
    assert data['tags'] == ['HTML Tag1', 'HTML Tag2'] # HTML tags should be present, API tags will be ignored if HTML has them.
