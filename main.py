# A watchlist organizer in PySimpleGUI
import json
from typing import Tuple
import PySimpleGUI as sg
from classes import Movie
import imdb_api as imdb

# vars
font= ('Ariel, 12')

menu_def = [['File', ['Add']],
            ['Help', ['right click on item for drop down menu']]]  

right_click_menu_1 = ['rc_menu',
    ['Move', 'Details', '---', 'Remove']]

right_click_menu_2 = ['rc_menu',
    ['Move Back', 'Details']]

watchlist : list[Movie] = []
watched_list : list[Movie]= []

table_con_watchlist = []  # structure [[], [], []] 2d array
table_con_watched_list = []
search_results = ''

# headings_watched = ['watched']   not needed only one heading is used maybe in the future
# headings_not_watched = ['not watched']


# funcs
def create_window(title, used_layout, display_values= '') -> sg.Window:
    """ Layouts are stored locally else an Error message occurs
    when reusing a layout while creating a new window.
    """
    sg.theme('DarkGrey1')
    sg.set_options(font= font) 

    main_layout = [
        [
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
        [   # Row 2
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
        [sg.Table(
            values= display_values,
            headings= ['results']),
        sg.Button('Submit', key='-DISPLAY_SUBMIT-')    
        ]

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
    m = Movie(
        title = movie['title'],
        id = movie['id'],
        description = movie['description'],
        image = movie['image'],
    )
    if 'watched date' in movie:
        m.set_watched_date(movie["watched date"])
        m.set_watch_status_true()
    return m

# funcs open new windows
def show_details():
    # Show different attributes of the movie object
    # TODO
    pass

def get_input(popup: sg.Window) -> Tuple[str, str]:
    """Tuple first value is search type and the second value is search title"""
    while True:
        event, values = popup.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            popup.close()
            return
        if event == 'Submit':
            # check if text is input and radio
            if values['-INPUT-'] == '':
                continue
            if values[0] == False and values[1] == False:
                print('both radio')
                continue
            break
    search_title = values['-INPUT-']
    popup.close()
    if values[0] == True:
        return 'SearchShow', search_title
    else:
        return 'SearchMovie', search_title

def display_results(win: sg.Window):
    # TODO: display the results of the imdb fetch and let the user pick one of the list
    while True:
        event, values = win.read()
        if event == sg.WINDOW_CLOSED:
            win.close()
            return

# 
def fetch_imdb_data(search_type, search_title) -> list:
    responseObj = imdb.get_respObj(title=search_title, search_type=search_type)
    search_results = responseObj.json()
    return search_results['results']

def move_movie(remove_from, put_in, indx) -> None:
    m = remove_from.pop(indx)
    put_in.append(m)


# MAIN
def main() -> None:
    """Main Function where all the logic is"""
    global table_con_watchlist, table_con_watched_list # 

    # some "initializiaton" required before window can be created
    database = load_json() 
    _ = database['watchlist'] + database['watched_list']
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
            search_ipt = get_input(create_window('Search', 'popup'))
            if search_ipt == None:
                continue
            search_results = fetch_imdb_data(search_ipt[0], search_ipt[1])
            display_win = create_window('Results', 'display', [search_results]) # TODO: look def display_win

        if event == 'Move':
            if values['-WATCHLIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move' and other opt
                continue
            print(values['-WATCHLIST_TABLE-'][0])
            move_movie(watchlist, watched_list, values['-WATCHLIST_TABLE-'][0]) #TODO Move Back does not work and crashed app when clicked again
            
            # window['-WATCHLIST_TABLE-'].update(watchlist)
            # window['-WATCHED_LIST_TABLE-'].update(watched_list)

        if event == 'Move Back':
            if values['-WATCHED_LIST_TABLE-'] == []:
                # checks if item on list is clicked else it ignores 'Move Back' and other opt
                continue

            # move_movie(watched_list, watchlist, values['-WATCHED_LIST_TABLE-'][0])
            # window['-WATCHLIST_TABLE-'].update(watchlist)
            # window['-WATCHED_LIST_TABLE-'].update(watched_list)

        if event == 'Remove':
            pass
        
        if event == 'Details':
            show_details()

        print(event, values)

    window.close()


if __name__ == '__main__':
    main()
