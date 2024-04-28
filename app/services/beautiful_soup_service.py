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
import time

# Third-party libraries
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BeautifulSoupService:
    def __init__(self):
        self.mongo_service = MongoService()
        self.patches_url = 'https://leagueoflegends.fandom.com/wiki/Patch_(League_of_Legends)'
        self.stats_url = 'https://gol.gg/tournament/list/region-ALL/league-1/'

    def scrape_patches(self):
        logger.info('Scraping patches')

        history_page = requests.get(self.patches_url)
        history_soup = BeautifulSoup(history_page.content, 'html.parser')

        patches = history_soup.find_all('a', {'title': lambda title: all(char.isdigit() or char == '.' or char == 'V' for char in title) if title else False})

        for patch in patches[:1]:
            patch_page = requests.get(f"https://leagueoflegends.fandom.com{patch['href']}")
            patch_soup = BeautifulSoup(patch_page.content, 'html.parser')

            champions_section = patch_soup.find('span', id='Champions').parent

            champion_names = champions_section.find_all_next('dl')

            filtered_champions = []
            for champion in champion_names:
                previous_section = champion.find_previous('h3')
                if previous_section and 'Champions' in previous_section.text:
                    filtered_champions.append(champion)
                else:
                    break # Stop processing when we reach the next section

            for champion in filtered_champions:
                champion_name = champion.find_next('dt').text.strip()
                champion_updates = champion.find_next('ul')
                print(champion_name)
                for update in champion_updates:
                    print(update.text)
                print()
            time.sleep(2)

    def scrape_stats(self):
        print('Scraping stats')
        pass