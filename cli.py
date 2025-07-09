import argparse
import json
import sys
import logging

from steam_utils.constants import SUPPORTED_LANGUAGES
from steam_data.store_html import StoreHtmlDataSource
from steam_data.steam_app_details import SteamAppDetailsDataSource
from steam_data.combined_data import CombinedSteamDataSource

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Scrape Steam-related data from various sources.')
    parser.add_argument('identifier', help='The identifier for the data (e.g., Steam store URL, App ID).')
    parser.add_argument('-o', '--output', help='Path to the output JSON file.')
    parser.add_argument('--lang', default='english', choices=SUPPORTED_LANGUAGES.keys(), help='Language for the store page (only for store-html source).')
    parser.add_argument('--source', default='store-html', choices=['store-html', 'steampowered-api', 'combined'], help='Data source to use.')
    args = parser.parse_args()

    data_source = None
    if args.source == 'store-html':
        data_source = StoreHtmlDataSource()
        data = data_source.get_data(args.identifier, lang=args.lang)
    elif args.source == 'steampowered-api':
        data_source = SteamAppDetailsDataSource()
        data = data_source.get_data(args.identifier, lang=args.lang) # Pass lang to steampowered-api
    elif args.source == 'combined':
        data_source = CombinedSteamDataSource()
        data = data_source.get_data(args.identifier, lang=args.lang)
    else:
        logger.error(f"Unknown data source '{args.source}'.")
        sys.exit(1)

    if data:
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Data successfully saved to {args.output}")
            except IOError as e:
                logger.error(f"Error writing to file {args.output}: {e}")
                sys.exit(1)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False)) # Keep print for stdout output
    else:
        logger.info("No data retrieved.")

if __name__ == "__main__":
    main()
