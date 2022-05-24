# A watchlist organizer in PySimpleGUI
import json
from typing import Tuple
import PySimpleGUI as sg
from classes import Movie
import imdb_api as imdb

def create_window() -> sg.Window:
    """ Layouts are stored locally else an Error message occurs
    when reusing a layout while creating a new window.
    """
    sg.theme('DarkGrey1')
    sg.set_options(font= font) 
    title = 'Watchlist Organizer'

    main_layout = [
        [
            sg.Menu(menu_def)
        ],
        [  # Row 1
            sg.Text(
                'watchlist organizer',
                justification='center',
                expand_x=True,
                key='TEXT',)
        ],
        [  # Row 2 
            sg.Table( # not watched
                values= table_content_not_watched,
                headings= headings_not_watched,
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
            sg.Table( # watched
                values= table_content_watched,
                headings= headings_watched,
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
        [   # Row 3
            sg.Push(),
            sg.Button(
                button_text= 'exit', 
                key= '-EXIT-')
        ],
    ]
    
    return sg.Window(title, main_layout, finalize=True)

def load_json() -> dict[list[dict], list[dict]]:
    with open('database.json') as f:
        return  json.load(f)

def save_to_json(data) -> None:
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def create_movie_objects(database) -> None:
    """fills the 2 lists watchlist/watched_list with Movie Objects respectively"""
    for item in database['watchlist']:
        m = Movie(
            title= item['title'],
            id= item['id'],
            description= item['description'],
            image= item['image'],
        )
        watchlist.append(m)
    for item in database['watched_list']:
        m = Movie(
            title= item['title'],
            id= item['id'],
            description= item['description'],
            image= item['image'],
        )
        if item.get('watched date') != None: # some items in watched_list dont have a 'watched date'
            m.set_watched_date(item['watched date'])
        watched_list.append(m)

def show_details():
    pass

def update_tables() -> None:
    global table_content_not_watched, table_content_watched
    table_content_not_watched = []
    table_content_watched = []
    for movie in watchlist:
        table_content_not_watched.append([movie.title])
    for movie in watched_list:
        table_content_watched.append([movie.title])

def move_movie(remove_from, put_in, indx) -> None:
    m = remove_from.pop(indx)
    put_in.append(m)
    
def get_input() -> Tuple[str, str]:
    """returned Tuple first value shows if show (True) or movie (False) and second val is name"""
    popup = sg.Window('Continue?', [
        [sg.Radio('Show', "RAD1"), sg.Radio('Movie', "RAD1")], 
        [sg.Input(key='-INPUT-')],
        [sg.Button('Cancel'), sg.Push(), sg.Button('Submit')]])
    while True:
        event, values = popup.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            popup.close()
            return
        if event == 'Submit':
            if values['-INPUT-'] == '':
                continue
            if values[0] == False and values[1] == False:
                print('both radio')
                continue
            break
        print(event, values)
    
    popup.close()
    if values[0] == True:
        return 'SearchShow', values['-INPUT-']
    else:
        return 'SearchMovie', values['-INPUT-']

def display_results():
    # TODO
    pass

def main() -> None:
    """Main Function where all the logic is"""
    database = load_json()
    create_movie_objects(database)
    update_tables()
    window = create_window()

    while True:
        # main window loop
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        
        if event == 'Add':
            ipt = get_input()
            if ipt == None:
                continue
            display_results(ipt)
            







        if event == 'Move':
            if values['-WATCHLIST_TABLE-'] == []:
                continue
            move_movie(watchlist, watched_list, values['-WATCHLIST_TABLE-'][0])
            update_tables()
            window['-WATCHLIST_TABLE-'].update(table_content_not_watched)
            window['-WATCHED_LIST_TABLE-'].update(table_content_watched)

        if event == 'Move Back':
            if values['-WATCHED_LIST_TABLE-'] == []:
                continue
            move_movie(watched_list, watchlist, values['-WATCHED_LIST_TABLE-'][0])
            window['-WATCHLIST_TABLE-'].update(table_content_not_watched)
            window['-WATCHED_LIST_TABLE-'].update(table_content_watched)

        if event == 'Remove':
            pass
        
        if event == 'Details':
            show_details()

        print(event, values)

    window.close()


# variables
font= ('Ariel, 12')

menu_def = [['File', ['Add']],
            ['Help', ['right click on item for drop down menu']]
]  
right_click_menu_1 = ['rc_menu',
    ['Move', 'Details', '---', 'Remove']
]
right_click_menu_2 = ['rc_menu',
    ['Move Back', 'Details']
]

table_content_watched = [] # 2d array
table_content_not_watched = [] # 2d array

watchlist : list[Movie] = []
watched_list : list[Movie]= []

headings_watched = ['watched']
headings_not_watched = ['not watched']

if __name__ == '__main__':
    main()

# TODO: Wenn man ein item in der Liste klickt soll man es andern konnen 
# auch sollte man ein menu bar einfugen damit man neue items einfugen kann
# 