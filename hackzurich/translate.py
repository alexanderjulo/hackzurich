from flask import current_app
import requests


base_url = "https://www.googleapis.com/language/translate/v2"


def translate(query, source="DE", target="EN"):
    params = {
        'key': current_app.config['GOOGLE_API_KEY'],
        'q': query,
        'source': source,
        'target': target
    }
    r = requests.get(base_url, params=params)
    print r.json()
    return r.json()['data']['translations'][0]['translatedText']
