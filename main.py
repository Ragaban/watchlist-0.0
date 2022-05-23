# A watchlist organizer in PySimpleGUI
import json
import PySimpleGUI as sg
from matplotlib.pyplot import table
from classes import Movie

def create_window() -> sg.Window:
    """ Layouts are stored locally else an Error message occurs
    when reusing a layout while creating a new window.
    """
    sg.theme('DarkGrey1')
    sg.set_options(font= font) 
    title = 'Watchlist Organizer'

    main_layout = [
        [  # Row 1
            sg.Text(
                'watchlist organizer',
                justification='center',
                expand_x=True,
                key='TEXT',)
        ],
        [  # Row 2
            sg.Table(
                values= table_content_watched,
                headings= headings_watched,
                text_color= 'Black',
                def_col_width= 30,
                row_height= 25,
                num_rows= 25,
                background_color= 'grey',
                auto_size_columns= False,
                justification= 'right',
                key= '-WATCHED_LIST_TABLE-'
                ),
            sg.Table(
                values= table_content_not_watched,
                headings= headings_not_watched,
                text_color= 'Black',
                def_col_width= 30,
                row_height= 25,
                num_rows= 25,
                background_color= 'grey',
                auto_size_columns= False,
                justification= 'right',
                key= '-WATCHLIST_TABLE-'
                ),
        ], 
        [   # Row 3
            sg.Button(
                'move', key='-MOVE-'
                ), 
            sg.Button(
                'edit', key='-EDIT-'
                ),
            sg.Button(
                'remove', key='-REMOVE-'
            ),
            sg.Push(),
            sg.Button(
                'edit', key='-EDIT2-'
            )
        ],
        [   # Row 4
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

def fill_tables() -> None:
    """ call this only after create_movies_objects()"""
    for item in watchlist:
        table_content_watched.append([item.title])
    for item in watched_list:
        table_content_not_watched.append([item.title])

def main() -> None:
    """Main Function where all the logic is"""
    database = load_json()
    create_movie_objects(database)
    fill_tables()
    window = create_window()

    while True:
        # main window loop
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        
        if event == '-EDIT-':
            pass

        if event == '-MOVE-':
            pass
        
        print(event, values)

    window.close()


# variables
font= ('Ariel, 16')

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