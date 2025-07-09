import re

def is_valid_steam_url(url):
    """
    Checks if a given URL is a valid Steam store app page URL.
    Returns a match object if valid, None otherwise.
    """
    # Regex to match Steam store app URLs
    # It captures the app ID and optionally the game name
    pattern = r"https://store\.steampowered\.com/app/(\d+)(?:/([^/]+))?/?.*"
    match = re.match(pattern, url)
    return match

def extract_app_id_from_url(url):
    """
    Extracts the App ID from a valid Steam store URL.
    Returns the App ID as a string, or None if the URL is invalid.
    """
    match = is_valid_steam_url(url)
    if match:
        return match.group(1)
    return None

def clean_filename(filename):
    """
    Cleans a string to be suitable for use as a filename.
    Removes invalid characters and truncates if too long.
    """
    # Remove invalid characters
    cleaned = re.sub(r'[\\/*?:"<>|]', '', filename)
    # Replace spaces with underscores (optional, but good for consistency)
    cleaned = cleaned.replace(' ', '_')
    # Truncate if too long (e.g., for OS compatibility)
    if len(cleaned) > 200:
        cleaned = cleaned[:200]
    return cleaned
