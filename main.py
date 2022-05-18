# A watchlist organizer in PySimpleGUI
import json
import PySimpleGUI as sg
from numpy import size


def create_window(layout_name) -> sg.Window:
    """ Layouts are stored locally else an Error message occurs
    when reusing a layout while creating a new window.
    """

    # Layouts
    main_menu_layout = [
        [sg.Text(
            'main menu',
            justification='center',
            expand_x=True,
            key='TEXT')],
        [sg.Button('watchlist', key='BUTTON_WATCHLIST')],
        [sg.Button('watched-list', key= 'BUTTON_WATCHED-LIST')],
        [sg.Button('exit', key= 'BUTTON_EXIT')],
    ]

    watchlist_layout = [
        [sg.Text(
            'watchlist',
            justification='center',
            expand_x=True,
            key='TEXT',)],
        [sg.Table(
            values= table_content,
            headings= [''],
            hide_vertical_scroll= True,
            auto_size_columns= False,
            max_col_width= 50,
            def_col_width= 50,
            num_rows= 35,
            display_row_numbers= True,
            text_color= 'Black',
            background_color= '#F0F0F0',
            alternating_row_color= '#DDDDDD',
            enable_click_events= True,
            right_click_menu= ['', ['Edit', 'Move']], # TODO: maybe make this a var
            key='WATCHLIST_TABLE')],
        [sg.Button('Back', key='BUTTON_BACK')],
    ]
    
    layouts = {
        'main menu': main_menu_layout, 
        'watchlist': watchlist_layout,
    }

    sg.theme('DarkGrey1')
    sg.set_options(font= 'Franklin 14')
    title = 'Watchlist'
    
    return sg.Window(title, layouts[layout_name], finalize=True)

def load_json() -> dict:
    with open('database.json') as f:
        d : dict = json.load(f)
        return d

def save_to_json(data) -> None:
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def main() -> None:
    """Main Function where all the logic is"""
    database = load_json()
    window = create_window('main menu')
    
    while True:
        # main window loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'BUTTON_EXIT':
            break
        
        if event == 'BUTTON_WATCHLIST':
            for item in database['watchlist']:
                film_title, description = item['title'], item['description']
                table_content.append([f' {film_title} | {description} '])
            window.close()
            window = create_window('watchlist')
            
        if event == 'BUTTON_WATCHED-LIST':
            for item in database['watched_list']:
                film_title, description = item['title'], item['description']
                table_content.append([f' {film_title} | {description} ']) # TODO: seperate those and add headers
            window.close()
            window = create_window('watchlist')

        if event == 'BUTTON_BACK':
            window.close()
            window = create_window('main menu')

        print(event, values)

    window.close()


# variables
table_content = []




if __name__ == '__main__':
    main()

# TODO: Wenn man ein item in der Liste klickt soll man es andern konnen 
# auch sollte man ein menu bar einfugen damit man neue items einfugen kann
# 