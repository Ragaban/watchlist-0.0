#imdb-api
import requests

def get_respObj(title, search_type= 'SearchMovie', key= ''):
    if key == '':
        with open('imdb_api_key.txt', 'r') as f:
            key = f.read()         
    return requests.get(f'https://imdb-api.com/en/API/{search_type}/{key}/{title}')

get_respObj('title')