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
    ['Move1', 'Details1', '---', 'Remove']]

right_click_menu_2 = ['rc_menu2',
    ['Move2', 'Details2']]


# vars containers
watchlist : list[Movie] = []
watched_list : list[Movie]= []

table_con_watchlist = []  # structure [[], [], []] 2d array 
table_con_watched_list = []
# NOTE: watchlist, watched_list AND table_con_watchlist, table_con_watched_list need to have the same index or else... DOOM

table_con_search_matches = []


# headings_watched = ['watched']   not needed only one heading is used maybe in the future
# headings_not_watched = ['not watched']


# funcs
def create_window(title, used_layout, details_text='') -> sg.Window:
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
            sg.Input(key= '-MAIN-INPUT-'),
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

    display_matches = [
        [
            sg.Table(
            values= table_con_search_matches,
            headings= ['matches'],
            text_color= 'Black',
            def_col_width= 30,
            row_height= 20, 
            num_rows= 20,
            background_color= 'grey',
            display_row_numbers= True,
            auto_size_columns= False,
            justification= 'right',
            key='-DISPLAY_MATCHES-')
        ],
        [sg.Button('Cancel'), sg.Push(), sg.Button('Submit')]
    ]
        
    popup_details = [
        [sg.Text(details_text)],
        [sg.Button('Exit')]
    ]

    layouts = {
        'main': main_layout,
        'popup': input_popup,
        'display': display_matches,
        'details' : popup_details
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

    return movie_Obj

# funcs open new windows
def show_details(window : sg.Window) -> None:
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            window.close()
            return
    

# imdb search and shit
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

def display_matches(window : sg.Window) -> int:
    """ Displays the fetched data from IMDB and returns the index of the chosen item"""
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return
        if event == 'Submit':
            if values['-DISPLAY_MATCHES-'] == []:
                continue
            break
        print(event, values)
    index = values['-DISPLAY_MATCHES-'][0]
    window.close()
    return index
     
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
    search_matches = responseObj.json()
    return search_matches['results']

def move_movie(remove_from, put_in, index) -> None:
    """ always use update_tables() after this one """
    m = remove_from.pop(index)
    put_in.insert(0, m)

def update_tables(table_con_watchlist, table_con_watched_list, window):
    table_con_watchlist = [[movie.title] for movie in watchlist]
    table_con_watched_list = [[movie.title] for movie in watched_list]
    window['-WATCHLIST_TABLE-'].update(table_con_watchlist)
    window['-WATCHED_LIST_TABLE-'].update(table_con_watched_list)
    window.refresh()

# MAIN
def main() -> None:
    """Main Function where all the logic is"""
    global table_con_watchlist, table_con_watched_list , table_con_search_matches 

    # Create Movie() instances from db.
    database = load_json() 
    for movie in database['watchlist']:
        movie_object = create_movie_object(movie)
        watchlist.append(movie_object)
    # list comprehension form -> [watchlist.append(create_movie_object(movie)) for movie in database['watchlist']]
    for movie in database['watched_list']:
        movie_object = create_movie_object(movie)
        watched_list.append(movie_object)
    # list comprehension form -> [watched_list.append(create_movie_object(movie)) for movie in database['watchlist']]

    # filling tables with 
    table_con_watchlist = [[movie.title] for movie in watchlist]
    table_con_watched_list = [[movie.title] for movie in watched_list]

    window = create_window('Movie Organizer', 'main')

    while True:
        # main window loop
        event, values = window.read()
        # closing guard
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        
        # Add opens another window to take the title and type of the movie
        if event == 'Add':
            search_parameters = get_input(create_window('Search', 'popup'))
            if search_parameters == None:
                continue
            search_type, search_title = search_parameters
            imdb_data = fetch_imdb_data(search_type, search_title) 
            table_con_search_matches = [[x['title'] + ', ' + x['description']] for x in imdb_data]
            select_items_idx = display_matches(create_window('Results', 'display'))
            if select_items_idx == None:
                continue
            else:
                index = select_items_idx
            
            added_movie = create_movie_object(imdb_data[index])
            watchlist.insert(0, added_movie)
                
            table_con_watchlist = [[movie.title] for movie in watchlist]
            table_con_watched_list = [[movie.title] for movie in watched_list]

            window['-WATCHLIST_TABLE-'].update(table_con_watchlist)
            window['-WATCHED_LIST_TABLE-'].update(table_con_watched_list)
            window.refresh()
                

        if event == 'Move1':
            if values['-WATCHLIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move1'
                continue
            print(values['-WATCHLIST_TABLE-'][0]) # debugging

            index = values['-WATCHLIST_TABLE-'][0] # clicked item 
            if values['-MAIN-INPUT-'] == '':
                pass
            else: 
                watchlist[index].watched_date = values['-MAIN-INPUT-']

            move_movie(watchlist, watched_list, index) 
            update_tables(table_con_watchlist, table_con_watched_list, window)

        if event == 'Move2':
            if values['-WATCHED_LIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move2'
                continue
            index = values['-WATCHED_LIST_TABLE-'][0]
            if hasattr(watched_list[index], 'watched_date'):
                watched_list[index].__delattr__('watched_date')
            
            move_movie(watched_list, watchlist, index)
            update_tables(table_con_watchlist, table_con_watched_list, window)

        if event == 'Remove':
            pass
        
        if event == 'Details1':
            index : int= values['-WATCHLIST-'][0]
            all_attributes = watchlist[index].__dict__.values() # all_attributes is a 'dict_values' class
            show_details(create_window('Details', 'details', list(all_attributes)))
        {3:1}.val
        print(event, values)

    window.close()


if __name__ == '__main__':
    main()
