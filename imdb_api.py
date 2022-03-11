""" imdbp api fetcher
    api key - k_8udy6r0k 
    100 requests.get() per day
    search movies   - https://imdb-api.com/en/API/SearchMovie/k_8udy6r0k/MOVIE_TITLE
    serach series   - https://imdb-api.com/en/API/SearchSeries/k_8udy6r0k/SERIES_TITLE 
"""
import requests

def get_respObj(film_show, title, key='k_8udy6r0k'):
    """Get response obj from imdb api. film_show = "SearchMovie" or "SearchMovie"."""
    response_obj = requests.get(f'https://imdb-api.com/en/API/{film_show}/{key}/{title}')
    return response_obj

def get_jsonObj(response_obj) -> dict: # Name is wrong return dict_obj
    """convert response_obj (200) to dict."""
    dict_obj = response_obj.json()
    return dict_obj 



# r = imdb_api.get_respObj(title=title, film_show=f_or_s)
# json_obj = imdb_api.get_jsonObj(r)
# for i in range(len(json_obj['results'])):
#     print(json_obj['results'][i]['title'] + ' | ' + json_obj['results'][i]['description'])