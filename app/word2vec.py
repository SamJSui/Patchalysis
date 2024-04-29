from app.routes.scrape_routes import scrape_patches
from run import app

import spacy
import json

from transformers import pipeline

def main():
    output = {'_id': '14.8', 'release_date': 'April 17th, 2024',
              'champions': [{'champion': 'Akali', 'updates': [{'Stats': 'Base health increased to 600 from 570.'}]},
                            {'champion': 'Azir',
                             'updates': [{'Stats': 'Base health regeneration reduced to 3.5 from 5.'}, {
                                 'Arise!': 'Base damage reduced to 50 / 65 / 80 / 95 / 110 from 50 / 67 / 84 / 101 / 118.'}]},
                            {'champion': 'Brand',
                             'updates': [{'Blaze': 'Bug Fix: Can now once again trigger  Dark Harvest.'}]},
                            {'champion': 'Briar', 'updates': [{'Stats': 'Health growth reduced to 95 from 100.'}, {
                                'Head Rush': 'Cast range increased to 475 units from 450.'}, {
                                                                  'Blood Frenzy': 'Bonus attack speed changed to 55 / 65 / 75 / 85 / 95% from 54 / 68 / 82 / 96 / 110%. Bug Fix: Now properly reveals the nearest target while the effects of nearsight.'}]},
                            {'champion': 'Draven', 'updates': [{
                                                                   'Spinning Axe': 'Base damage increased to 45 / 50 / 55 / 60 / 65 from 40 / 45 / 50 / 55 / 60.'}]}]}

    # Convert to array of dictionaries keyed on champion name and value all the patch notes.
    data = []
    for champion in output['champions']:
        champ_data = {}
        champ_data[champion['champion']] = []
        for update in champion['updates']:
            # champ_data[champion['champion']] += next(iter(update.values())) + " "
            champ_data[champion['champion']].append(next(iter(update.values())))
        data.append(champ_data)
    print(data)

    print('Initializing sentiment pipeline...')
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print('Sentiment pipeline initialized...')
    for champion in data:
        updates = next(iter(champion.values()))
        print(next(iter(champion.keys())))
        print(updates)
        print(sentiment_pipeline(updates))

if __name__ == '__main__':
    main()

# HuggingFace Sentiment Analysis

# nlp = spacy.load("en_core_web_md")
# tokens = nlp(output['champions'][0]['updates'][0]['Stats'])
#
# # Features would be champion names.
# # Value would be the patch notes vectorized.
# # Output would be the win rates of each champion?
#
# for token in tokens:
#     print(token.vector)
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)