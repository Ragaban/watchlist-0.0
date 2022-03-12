# watchlist
import json
import imdb_api as imdb



def int_input(validate=int) -> int:
    """Takes an int as ipt and validates it with the int() function and except ValueError.""" 
    while True:
        ipt = input()
        try:
            ipt = int(ipt)
        except ValueError:
            print('Invalid input! Try again.')
            continue
        return ipt

def menu() -> str:
    """basic menu"""
    print(
        """
        1. print watchlist
        2. add item
        3. remove item
        4. print finished-films-list
        0. exit
    """)
    return  input()    

def prt_list(chosen_list) -> None:
    """print either watchlist or finished-film-list. chosen_list = 'watchlist'/'watched_list'
    w/ index and year """
    with open("database.txt", "r") as jsonFile:
        watchlist = json.load(jsonFile)
        for index, item in enumerate(watchlist[chosen_list]):
            print(index, item['title'], item['description'])

def search_imdb(search_type, title) -> dict:
    """looks up imdb with imdb_api module"""
    response_obj = imdb.get_respObj(search_type, title)
    return imdb.get_jsonObj(response_obj)

def add_item():
    """adds item from imdb to the list"""
    # input stuff
    while True:
        user_ipt = input("Film(1) or TV(2)?: ")
        if user_ipt == "1":
            search_type = "SearchMovie"
            title = input("What is the title of the film?: ")
            break
        elif user_ipt == "2":
            search_type = "SearchSeries"
            title = input("What is the title of the series?: ")
            break
        else:
            continue
    #filtering results
    search_result = search_imdb(search_type, title) 
    for index, item in enumerate(search_result['results']):
        print(f"({index}) - {item['title']}, {item['description']}")
    #input stuff w/ validating
    while True:
        ipt = int_input()
        if -1 <= ipt <= len([search_result['results']])-1: # check if ipt is in range of results:
            break
        else:
            print("Invalid input. Try again.")
            continue
    
    chosen_item = search_result['results'][ipt]
    with open("database.txt", "r+") as jsonDB:
        dictDB = json.load(jsonDB)
        dictDB['watchlist'].append(chosen_item)
        json.dump(dictDB, jsonDB, sort_keys=True, indent=4) # dump with pretty format

def remove_item():
    """prints watchlist with an index. Put in index to delete item from list and return it"""
    prt_list("watchlist")
    with open("database.txt", "r+") as jsonFile:
        watchlist = json.load(jsonFile)
        type(watchlist)
        #TODO: Implement removing item
        
def main():
    running = True
    while running:
        user_ipt = menu()
        if user_ipt == "1":
            prt_list("watchlist")
        elif user_ipt == "2":
            add_item()
        elif user_ipt == "3":
            remove_item()
        elif user_ipt == "4":
            prt_list("watched_list")
        elif user_ipt == "0":
            print("Closing now. Goodbye :)")
            return
        else:
            continue
    
if __name__ == "__main__":
    main()