''' This module contains the BeautifulSoupService class, which is responsible for scraping data from the web using the BeautifulSoup library.

Classes:
    BeautifulSoupService: A class for scraping data from the web using BeautifulSoup.

Attributes:
    logger: A logger object for logging messages.

Contributors:
    Sam Sui
    Jovi Yoshioka
'''

# Standard library
import logging
import re
import re

# Third-party libraries
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BeautifulSoupService:
    def __init__(self):
        self.patches_url = 'https://leagueoflegends.fandom.com/wiki/Patch_(League_of_Legends)'
        self.stats_url = 'https://gol.gg/champion/list/season-ALL/split-ALL/tournament-ALL/'
        self.patch_versions = None

    @property
    def patches(self):
        ''' Scrapes the patch versions and their URLs from the League of Legends Fandom website.

        Returns:
            dict: A dictionary containing patch versions as keys and their URLs as values.
        '''

        if self.patch_versions is None:
            history_page = requests.get(self.patches_url)
            history_soup = BeautifulSoup(history_page.content, 'html.parser')
            patches = history_soup.find_all('a', {'title': lambda title: all(char.isdigit() or char == '.' or char == 'V' for char in title) if title else False})
            patches = {
                patch['title'].strip().replace('.', '_'): patch['href'] 
                for patch in patches if patch.text.strip() != ''
            }
            self.patch_versions = patches
            return patches
        else:
            return self.patch_versions

    def scrape_patches(self):
        ''' Scrapes the patch data from the League of Legends Fandom website.

        Returns:
            list: A list of dictionaries containing patch version, release date, and champion updates.

        Example:
            [
                {
                    "_id": "11.1",
                    "release_date": "2021-01-06",
                    "champions": [
                        {
                            "champion": "Aatrox",
                            "updates": [
                                {
                                    "Bug Fixes": "Fixed a bug where Aatrox's E - Umbral Dash would not properly cast if the cursor was outside of the ability's range."
                                }
                            ]
                        },
                        ...
                    ]
                },
                ...
            ]
        '''

        all_patch_data = [] # List to store all patch data
        patches = self.patches # Get patch versions and their URLs

        for patch in patches:
            print(f'Processing patch {patch}...')
            patch_url = f'https://leagueoflegends.fandom.com{patches[patch]}'
            patch_page = requests.get(patch_url)
            patch_soup = BeautifulSoup(patch_page.content, 'html.parser')
            release_date = patch_soup.find('td', {'data-source': 'Release'}).text.strip()
            champions_data = self._parse_champion_data(patch, patch_soup)

            patch_data = {
                '_id': patch, 
                'release_date': release_date,
                'champions': champions_data
            }
            all_patch_data.append(patch_data)
            logger.info(f'Patch {patch} data processed and stored.')

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

        # Reverse list so most recent patches are first.
        #   Note: This is to get rid of duplicate patches across seasons (e.g., Season 8 having 9.13).
        season_links.reverse()

        # For each season, scrape each patch version's stats.
        patches_scraped = []
        results = []
        for season_link in season_links:
            print('Scraping {}...'.format(season_link))  # Simply to track runtime progress.

            url = "https://gol.gg/champion" + season_link[1:]  # Note: removing '.' before the season link.
            r = requests.post(url, headers={ 'User-Agent': 'Mozilla/5.0' })
            soup = BeautifulSoup(r.text, "html.parser")

            # Get list of patch versions.
            patch_versions = []
            patches = soup.find('select', id='patch').find_all('option', value=lambda x: x != 'ALL')
            for patch in patches:
                # Avoid duplicate patches within same season.
                if patch['value'] in patch_versions:
                    print('     Skipping Patch {} (Dup Key)...'.format(patch['value'][:-1]))
                    continue
                patch_versions.append(patch['value'])

            # Scrape data for each season and patch version.
            for patch in patch_versions:
                patch = patch.replace('.', '_')  # Replace '.' with '_' to avoid issues with MongoDB.

                # Avoid duplicate patches across seasons (e.g., Season 8 having 9.13).
                if patch in patches_scraped:
                    print('     Skipping Patch {} (Dup Key)...'.format(patch[:-1]))
                    continue

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
                patches_scraped.append(patch)

        f = open("stats.txt", "a")
        f.write(str(results))
        f.close()
        print('Completed scraping stats...')
        return results

    def _parse_champion_data(self, patch: str, soup):
        ''' Parses the champion updates from a BeautifulSoup object of a single patch page.
        
        Args:
            patch (str): The patch version.
            soup (BeautifulSoup): The BeautifulSoup object of the patch page.
            
        Returns:
            list: A list of dictionaries with champion names and their updates.
        '''

        champions_section = soup.find('span', id='Champions') or soup.find('span', id='Champion')
        if not champions_section:
            print(f'No champions section found for patch {patch}.')
            del self.patches[patch] # Remove patch from list of patches to avoid key errors
            return []
        champions_section = champions_section.parent
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

                    category = update.get_text().split('\n')[0].strip().replace('.', '')
                    update_text = " ".join(update.text.split('\n')[1:]).strip()
                    updates_list.append({category: update_text})

            if updates_list:
                champions_data.append({"champion": champion_name, "updates": updates_list})

        return champions_data
    