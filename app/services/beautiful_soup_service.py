''' This module contains the BeautifulSoupService class, which is responsible for scraping data from the web using the BeautifulSoup library.

Classes:
    BeautifulSoupService: A class for scraping data from the web using BeautifulSoup.

Attributes:
    logger: A logger object for logging messages.

Contributors:
    Sam Sui
'''

# Internal imports
from app.services.mongo_service import MongoService

# Standard library
import logging

# Third-party libraries
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BeautifulSoupService:
    def __init__(self):
        self.patches_url = 'https://leagueoflegends.fandom.com/wiki/Patch_(League_of_Legends)'
        self.stats_url = 'https://gol.gg/tournament/list/region-ALL/league-1/'

    def scrape_patches(self):
        """
        Scrapes the patches from the League of Legends patch history page and each patch's detail page.
        """
        logger.info('Scraping patches')
        history_page = requests.get(self.patches_url)
        history_soup = BeautifulSoup(history_page.content, 'html.parser')
        patches = history_soup.find_all('a', {'title': lambda title: all(char.isdigit() or char == '.' or char == 'V' for char in title) if title else False})
        
        all_patch_data = []
        for patch in patches[:1]:  # Limited for demonstration

            patch_url = f'https://leagueoflegends.fandom.com{patch["href"]}'
            patch_page = requests.get(patch_url)
            patch_soup = BeautifulSoup(patch_page.content, 'html.parser')
            release_date = patch_soup.find('td', {'data-source': 'Release'}).text.strip()
            champions_data = self._parse_champion_data(patch_soup)

            patch_version = patch.text.strip()
            patch_data = {
                '_id': patch_version, 
                'release_date': release_date,
                'champions': champions_data
            }
            all_patch_data.append(patch_data)
            print(patch_data)
            logger.info(f'Patch {patch_version} data processed and stored.')

        return all_patch_data

    def scrape_stats(self):
        print('Scraping stats')
        pass

    def _parse_champion_data(self, soup):
        """
        Parses the champion updates from a BeautifulSoup object of a single patch page.
        
        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the patch page.
            
        Returns:
            list: A list of dictionaries with champion names and their updates.
        """
        champions_section = soup.find('span', id='Champions').parent
        champion_names = champions_section.find_all_next('dl')
        champions_data = []

        for champion in champion_names:
            previous_section = champion.find_previous('h3')
            if not previous_section or 'Champions' not in previous_section.text:
                break  # Stop if we are out of the Champions section

            champion_name = champion.find_next('dt').text.strip()
            logger.debug(f"Processing updates for {champion_name}")
            updates_list = []
            updates = champion.find_next('ul')
            if updates:
                for update in updates.find_all('li', recursive=False):
                    if 'skin-icon' in str(update) or 'cosmetics' in str(update).lower():
                        continue  # Ignore cosmetic updates

                    category = update.get_text().split('\n')[0].strip()
                    update_text = " ".join(update.text.split('\n')[1:]).strip()
                    updates_list.append({category: update_text})

            if updates_list:
                champions_data.append({"champion": champion_name, "updates": updates_list})

        return champions_data