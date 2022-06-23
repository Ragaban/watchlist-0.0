# A watchlist organizer in PySimpleGUI
import json
import requests
import PySimpleGUI as sg

from requests import Response
from typing import Tuple
from classes import Movie


# vars
font= ('Ariel, 12')

# vars structures
menu_def = [['File', ['Add']],
            ['Help', ['right click on item for drop down menu']]]  

right_click_menu_1 = ['rc_menu1',
    ['Move', 'Details', '---', 'Remove']]

right_click_menu_2 = ['rc_menu2',
    ['Move Back', 'Details']]


# vars containers
watchlist : list[Movie] = []
watched_list : list[Movie]= []

table_con_watchlist = []  # structure [[], [], []] 2d array
table_con_watched_list = []

table_con_search_results = []


# headings_watched = ['watched']   not needed only one heading is used maybe in the future
# headings_not_watched = ['not watched']


# funcs
def create_window(title, used_layout) -> sg.Window:
    """ Layouts are stored locally else an Error message occurs
    when reusing a layout while creating a new window.
    """

    # vars
    sg.theme('DarkGrey1')
    sg.set_options(font= font) 

    main_layout = [
        [  # Menu Bar
            sg.Menu(menu_def)
        ],
        [  # Row 1
            sg.Table( # WATCHLIST
                values= table_con_watchlist,
                headings= ['watchlist'],
                text_color= 'Black',
                def_col_width= 30,
                row_height= 20, 
                num_rows= 20,
                background_color= 'grey',
                display_row_numbers= True,
                auto_size_columns= False,
                right_click_menu= right_click_menu_1,
                justification= 'right',
                key= '-WATCHLIST_TABLE-'
                ),
            sg.Table( # WATCHED-LIST
                values= table_con_watched_list,
                headings= ['watched-list'],
                text_color= 'Black',
                def_col_width= 30,
                row_height= 20,
                num_rows= 20,
                background_color= 'grey',
                display_row_numbers= True,
                auto_size_columns= False,
                right_click_menu= right_click_menu_2,
                justification= 'right',
                key= '-WATCHED_LIST_TABLE-'
                ),
        ], 
        [  # Row 2
            sg.Push(),
            sg.Button(
                button_text= 'exit', 
                key= '-EXIT-')
        ],
    ]
    
    input_popup = [
        [sg.Radio('Show', "RAD1"), sg.Radio('Movie', "RAD1")], 
        [sg.Input(key='-INPUT-')],
        [sg.Button('Cancel'), sg.Push(), sg.Button('Submit')]]

    display_results = [
        [
            sg.Table(
            values= table_con_search_results,
            headings= ['results'],
            text_color= 'Black',
            def_col_width= 30,
            row_height= 20, 
            num_rows= 20,
            background_color= 'grey',
            display_row_numbers= True,
            auto_size_columns= False,
            justification= 'right',
            key='-DISPLAY_RESULTS-')
        ],
        [sg.Button('Cancel'), sg.Push(), sg.Button('Submit')]
    ]
        

    layouts = {
        'main': main_layout,
        'popup': input_popup,
        'display': display_results
        }

    return sg.Window(title, layouts[used_layout], finalize=True)

# funcs before first window is generated

def load_json() -> dict[list[dict], list[dict]]:
    with open('database.json') as f:
        return  json.load(f)

def save_to_json(data) -> None:
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def create_movie_object(movie : dict) -> Movie:
    if 'watched date' in movie:
        watched_date = movie['watched date']
    else:
        watched_date = ''

    movie_Obj = Movie(
        title = movie['title'],
        id = movie['id'],
        description = movie['description'],
        image = movie['image'],
        watched_date= watched_date
    )
    if 'watched date' in movie:
        movie_Obj.watched_it()

    return movie_Obj

# funcs open new windows
def show_details():
    # Show different attributes of the movie object
    # TODO
    pass

# imdb search
def get_input(window : sg.Window) -> Tuple[str, str]:
    """Tuple first value is search type and the second value is search title"""
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return
        if event == 'Submit':
            # check if input and radio are not empty
            if values['-INPUT-'] == '':
                continue
            if values[0] == False and values[1] == False:
                print('both radio')
                continue
            break
    search_title = values['-INPUT-']
    search_type = values[0]
    window.close() 
    if search_type == True: # true Series false Movies
        return 'SearchSeries', search_title
    else:
        return 'SearchMovie', search_title

def display_results(window : sg.Window) -> int:
    # TODO: display the results of the imdb fetch and let the user pick one of the list
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return
        if event == 'Submit':
            if values['-DISPLAY_RESULTS-'] == []:
                continue
            break
        print(event, values)
    index = values['-DISPLAY_RESULTS-'][0]
    window.close()
    return index
     
# imdb shit
def get_respObj(title, search_type, key= '') -> Response:
    """gets input from get_input func"""
    if key == '': # IF KEY NOT GIVEN USES ONE IN FILE imdb_api_key.txt
        with open('imdb_api_key.txt', 'r') as f:
            key = f.read()
    return requests.get(f'https://imdb-api.com/en/API/{search_type}/{key}/{title}')

def fetch_imdb_data(search_type, search_title) -> list:
    responseObj = get_respObj(search_type=search_type, title=search_title)
    if responseObj.status_code == 404:
        return []
    search_results = responseObj.json()
    return search_results['results']

def move_movie(remove_from, put_in, index) -> None:
    m = remove_from.pop(index)
    put_in.append(m)


# MAIN
def main() -> None:
    """Main Function where all the logic is"""
    global table_con_watchlist, table_con_watched_list , table_con_search_results 

    # Create Movie() instances from db.
    database = load_json() 
    _ = database['watchlist'] + database['watched_list'] # OPTIONAL TODO: MAYBE use zip function for this here idk
    for movie in _:
        movObj = create_movie_object(movie)
        if movObj.watch_status: 
            watched_list.append(movObj)    
        else: 
            watchlist.append(movObj)

    table_con_watchlist = [[movie.title] for movie in watchlist]
    table_con_watched_list = [[movie.title] for movie in watched_list]

    window = create_window('Movie Organizer', 'main')

    while True:
        # main window loop
        event, values = window.read()
        # closing guard
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        
        # Add opens another window to take the tile and type of the movie
        if event == 'Add':
            search_output= get_input(create_window('Search', 'popup'))
            if search_output == None:
                continue
            search_type, search_title = search_output
            search_results = fetch_imdb_data(search_type, search_title) 
            table_con_search_results = [[x['title'] + ', ' + x['description']] for x in search_results]
            select_items_idx = display_results(create_window('Results', 'display'))
            if select_items_idx == None:
                continue
            else:
                index = select_items_idx
                print(search_results[index])
                #TODO:

        if event == 'Move':
            if values['-WATCHLIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move'
                continue
            print(values['-WATCHLIST_TABLE-'][0]) # debugging

            index = values['-WATCHLIST_TABLE-'][0]
            move_movie(watchlist, watched_list, index) 

            table_con_watchlist = [[movie.title] for movie in watchlist]
            table_con_watched_list = [[movie.title] for movie in watched_list]

            window['-WATCHLIST_TABLE-'].update(table_con_watchlist)
            window['-WATCHED_LIST_TABLE-'].update(table_con_watched_list)
            
            window.refresh()

        if event == 'Move Back':
            if values['-WATCHED_LIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move Back'
                continue
            
            index = values['-WATCHED_LIST_TABLE-'][0]
            move_movie(watched_list, watchlist, index)

            table_con_watchlist = [[movie.title] for movie in watchlist]
            table_con_watched_list = [[movie.title] for movie in watched_list]

            window['-WATCHLIST_TABLE-'].update(table_con_watchlist)
            window['-WATCHED_LIST_TABLE-'].update(table_con_watched_list)
            
            window.refresh()

        if event == 'Remove':
            pass
        
        if event == 'Details':
            show_details()

        print(event, values)

    window.close()


if __name__ == '__main__':
    main()
