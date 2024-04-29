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
import re

# Third-party libraries
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BeautifulSoupService:
    def __init__(self):
        self.patches_url = 'https://leagueoflegends.fandom.com/wiki/Patch_(League_of_Legends)'
        self.stats_url = 'https://gol.gg/champion/list/season-ALL/split-ALL/tournament-ALL/'

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
        results = []
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

                patch_data = {'_id': patch[:-1], }

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

                patch_data['champions'] = data
                results.append(patch_data)

        f = open("stats.txt", "a")
        f.write(str(results))
        f.close()

        print('Completed scraping stats...')

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