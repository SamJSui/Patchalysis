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
import re

# Third-party libraries
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BeautifulSoupService:
    def __init__(self):
        self.mongo_service = MongoService()
        self.patches_url = 'https://leagueoflegends.fandom.com/wiki/Patch_(League_of_Legends)'
        self.stats_url = 'https://gol.gg/champion/list/season-ALL/split-ALL/tournament-ALL/'
        # Old stats_url? - 'https://gol.gg/tournament/list/region-ALL/league-1/'

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
        logger.info('Scraping stats')

        # Note: Requires User-Agent header to prevent 403 error.
        # Reference: https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed
        r = requests.post(self.stats_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, "html.parser")

        # Get links to each season.
        links = soup.find_all('a', href=re.compile(r'./list/season-'))
        season_links = []
        for link in links:
            if link.has_attr('href'):
                if 'split-ALL' in link['href']:
                    season_links.append(link['href'])
        # Double counting last season, so remove last item.
        season_links = season_links[:-1]

        # For each season, scrape each patch version's stats.
        results = {}
        for season_link in season_links:
            print('Scraping {}...'.format(season_link))  # Simply to track runtime progress.

            url = "https://gol.gg/champion" + season_link[1:]  # Note: removing '.' before the season link.
            r = requests.post(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, "html.parser")

            # Get list of patch versions.
            patch_versions = []
            patches = soup.find('select', id='patch').find_all('option', value=lambda x: x != 'ALL')
            for patch in patches:
                patch_versions.append(patch['value'])

            # Scrape data for each season and patch version.
            for patch in patch_versions:
                print('     Scraping Patch {}...'.format(patch))  # Simply to track runtime progress.

                post_data = {'patch': patch}
                url = "https://gol.gg/champion" + season_link[1:]
                r = requests.post(url, data=post_data, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.text, "html.parser")

                # Get the table of champion stats.
                tables = soup.find_all('table')
                table = None
                for tab in tables:
                    if tab.has_attr('class'):
                        if tab['class'][0] == 'table_list':
                            table = tab

                # Create list of dictionaries with each champion and their win rate.
                data = []
                rows = table.find_all('tr')
                for row in rows:
                    row_data = {}
                    # Only retrieve the champion name and win rate columns.
                    columns = row.find_all('td')
                    for i, col in enumerate(columns):
                        if i == 0:
                            # Get champion name.
                            a_tag = col.find('a')
                            row_data['champion'] = a_tag['title'][:-6]
                        elif i == 6:
                            # Get win rate.
                            # Note: Might be "None" if champion was not played during the patch.
                            row_data['win-rate'] = col.string
                            break

                    # First row will be the header (i.e., no champion data), so skip.
                    if row_data != {}:
                        data.append(row_data)

                results[patch[:-1]] = data

        print('Completed scraping stats...')
