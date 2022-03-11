# watchlist
import json
import imdb_api as imdb

def menu():
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

def prt_list(chosen_list):
    """print either watchlist or finished-film-list. chosen_list = 'watchlist'/'watched_list'
    w/ index and year """
    with open("database.txt", "r") as jsonFile:
        watchlist = json.load(jsonFile)
        for index, item in enumerate(watchlist[chosen_list]):
            print(index, item['title'], item['description'])

def add_item():
    while True:
        user_ipt = input("Film(1) or TV(2)?: ")
        if user_ipt == "1":
            search_type = "SearchMovie"
            title = input("What is the title of the Film?: ")
            break
        elif user_ipt == "2":
            search_type = "SearchSeries"
            title = input("What is the title of the Show?: ")
            break
        else:
            continue

    response_obj = imdb.get_respObj(search_type, title)
    print(imdb.get_jsonObj(response_obj))
    
    
def remove_item():
    """prints watchlist with an index. Put in index to delete item from list and return it"""
    prt_list("watchlist")
    with open("database.txt", "r+") as jsonFile:
        watchlist = json.load(jsonFile)
        type(watchlist)

        

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