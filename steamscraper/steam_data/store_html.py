import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import logging

from .base import SteamDataSource
from ..steam_utils.utils import is_valid_steam_url
from ..steam_utils.constants import SUPPORTED_LANGUAGES
from ..steam_utils.web_utils import fetch_steam_store_html

logger = logging.getLogger(__name__)

class StoreHtmlDataSource(SteamDataSource):
    def get_data(self, identifier, **kwargs):
        """
        Fetches game data from a Steam store URL or App ID.
        """
        url = identifier
        lang = kwargs.get('lang', 'english')
        # If identifier is an App ID, construct the URL
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            app_id = str(identifier)
            url = f"https://store.steampowered.com/app/{app_id}/"
            logger.info(f"Constructed URL from App ID: {url}")

        match = is_valid_steam_url(url)
        if not match:
            logger.error("Invalid Steam store page URL or App ID provided.")
            return None

        app_id = match.group(1)
        game_name = match.group(2) or f"app_{app_id}"
        
        safe_game_name = re.sub(r'[\\/*?"<>|]', "", game_name)

        html_content = fetch_steam_store_html(url, lang=lang)
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return self._parse_game_details(soup)
        except Exception as e:
            logger.error(f"An unexpected error occurred during parsing: {e}")
            return None

    def parse_static_content(self, content: str, **kwargs):
        """
        Processes raw HTML content to extract game details.
        """
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return self._parse_game_details(soup)
        except Exception as e:
            logger.error(f"Error parsing HTML content: {e}")
            return None

    @staticmethod
    def _parse_game_details(soup: BeautifulSoup):
        """
        Parses the BeautifulSoup object to extract comprehensive game details.
        """
        game_data = {}

        # --- Basic Info ---
        title_element = soup.find('div', class_='apphub_AppName')
        game_data['title'] = title_element.get_text(strip=True) if title_element else None

        header_image_element = soup.find('img', class_='game_header_image_full')
        game_data['header_image'] = header_image_element['src'] if header_image_element else None

        description_element = soup.find('div', class_='game_description_snippet')
        game_data['short_description'] = description_element.get_text(strip=True) if description_element else None
        
        full_description_element = soup.find('div', id='game_area_description')
        if full_description_element:
            for element in full_description_element.select('.game_area_description_section_title, .responsive_button'):
                element.decompose()
            full_desc_text = full_description_element.get_text(strip=True)
            reward_cutoff = full_desc_text.find("领取专属道具")
            if reward_cutoff != -1:
                full_desc_text = full_desc_text[:reward_cutoff]
            game_data['full_description'] = full_desc_text.strip()
        else:
            game_data['full_description'] = None

        # --- Developer/Publisher/Date ---
        details_block = soup.find('div', class_='glance_ctn')
        if details_block:
            dev_rows = details_block.find_all('div', class_='dev_row')
            for row in dev_rows:
                subtitle_div = row.find('div', class_='subtitle')
                if not subtitle_div: continue
                subtitle = subtitle_div.get_text(strip=True)
                summary = row.find('div', class_='summary')
                if summary:
                    link = summary.find('a')
                    text = link.get_text(strip=True) if link else summary.get_text(strip=True)
                    url = link['href'] if link else None
                    if 'Developer' in subtitle or '开发者' in subtitle:
                        game_data['developer'] = {'name': text, 'link': url}
                    elif 'Publisher' in subtitle or '发行商' in subtitle:
                        game_data['publisher'] = {'name': text, 'link': url}
            
            release_date_row = details_block.find('div', class_='release_date')
            if release_date_row:
                date_str = release_date_row.find('div', class_='date')
                game_data['release_date'] = date_str.get_text(strip=True) if date_str else None

        # --- Media (Screenshots/Videos)---
        game_data['media'] = {'videos': [], 'screenshots': []}
        video_elements = soup.select('.highlight_player_item.highlight_movie')
        for video in video_elements:
            video_id = video['id'].replace('highlight_movie_', '')
            thumb_element = soup.find('div', id=f'thumb_movie_{video_id}')
            thumbnail = thumb_element.find('img')['src'] if thumb_element and thumb_element.find('img') else None
            game_data['media']['videos'].append({
                'title': video.get('data-video-title', ''),
                'thumbnail': thumbnail,
                'webm_source': video.get('data-webm-source', ''),
                'mp4_source': video.get('data-mp4-source', '')
            })
        
        screenshot_elements = soup.select('a.highlight_screenshot_link')
        for screenshot in screenshot_elements:
            game_data['media']['screenshots'].append(screenshot['href'])

        # --- Pricing ---
        price_block = soup.find('div', class_='game_purchase_action')
        if price_block:
            price_element = price_block.find('div', class_='game_purchase_price')
            if price_element:
                game_data['price'] = price_element.get_text(strip=True)
            else:
                discount_block = price_block.find('div', class_='discount_block')
                if discount_block:
                    final_price = discount_block.find('div', class_='discount_final_price')
                    original_price = discount_block.find('div', class_='discount_original_price')
                    game_data['price'] = {
                        'discount_price': final_price.get_text(strip=True) if final_price else None,
                        'original_price': original_price.get_text(strip=True) if original_price else None,
                    }
                else:
                    game_data['price'] = 'Free to Play'
        else:
            game_data['price'] = 'N/A'

        # --- Tags ---
        tags_elements = soup.select('.glance_tags.popular_tags a.app_tag')
        game_data['tags'] = [tag.get_text(strip=True) for tag in tags_elements]

        # --- Reviews ---
        game_data['reviews'] = {}
        review_summary_rows = soup.select('.user_reviews_summary_row')
        for row in review_summary_rows:
            subtitle_div = row.find('div', class_='subtitle')
            if not subtitle_div: continue
            subtitle = subtitle_div.get_text(strip=True)
            summary_span = row.find('span', class_='game_review_summary')
            tooltip_html = row.get('data-tooltip-html', '')
            
            review_key = 'recent' if 'Recent' in subtitle or '最近' in subtitle else 'all'
            game_data['reviews'][review_key] = {
                'summary': summary_span.get_text(strip=True) if summary_span else None,
                'tooltip': tooltip_html
            }

        # --- System Requirements ---
        game_data['system_requirements'] = {}
        sys_req_content_list = soup.select('.game_area_sys_req')
        for content in sys_req_content_list:
            os_name = content.get('data-os', 'other').lower()
            reqs = {}
            for li in content.select('ul.bb_ul li'):
                strong = li.find('strong')
                if strong:
                    key = strong.get_text(strip=True).lower().replace(':', '')
                    value = li.get_text().replace(strong.get_text(), '').strip()
                    reqs[key] = value
            if reqs:
                game_data['system_requirements'][os_name] = reqs

        # --- Language Support ---
        game_data['language_support'] = []
        lang_table = soup.find('table', class_='game_language_options')
        if lang_table:
            for row in lang_table.find_all('tr')[1:]: # Skip header
                cols = row.find_all('td')
                if len(cols) == 4:
                    lang_name = cols[0].get_text(strip=True)
                    interface = '✔' in cols[1].get_text() or '✓' in cols[1].get_text()
                    full_audio = '✔' in cols[2].get_text() or '✓' in cols[2].get_text()
                    subtitles = '✔' in cols[3].get_text() or '✓' in cols[3].get_text()
                    game_data['language_support'].append({
                        'language': lang_name,
                        'interface': interface,
                        'full_audio': full_audio,
                        'subtitles': subtitles
                    })

        # --- Metacritic ---
        metacritic_block = soup.find('div', id='game_area_metascore')
        if metacritic_block:
            score = metacritic_block.find('div', class_='score')
            link = metacritic_block.find('a')
            game_data['metacritic'] = {
                'score': int(score.get_text(strip=True)) if score else None,
                'url': link['href'] if link else None
            }
        else:
            game_data['metacritic'] = None # Ensure it's always defined

        # --- DLCs ---
        game_data['dlcs'] = []
        dlc_rows = soup.select('.game_area_dlc_row')
        for row in dlc_rows:
            name_element = row.find(class_='game_area_dlc_name')
            price_div = row.find('div', class_='game_purchase_price') or row.find('div', class_='discount_final_price')
            game_data['dlcs'].append({
                'name': name_element.get_text(strip=True) if name_element else None,
                'price': price_div.get_text(strip=True) if price_div else 'N/A'
            })
            
        # --- Game Features ---
        features_list = soup.select('.game_area_details_specs_ctn .label')
        game_data['features'] = [feature.get_text(strip=True) for feature in features_list]

        # --- Content Descriptors ---
        rating_descriptors = soup.find('div', class_='game_rating_descriptors')
        if rating_descriptors:
            game_data['content_descriptors'] = list(rating_descriptors.stripped_strings)
        else:
            game_data['content_descriptors'] = []

        return game_data