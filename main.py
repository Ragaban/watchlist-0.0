# watchlist
import json

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
    """print either watchlist or finished-film-list. chosen_list = 'watchlist'/'watched_list' """
    with open("database.txt", "r") as jsonFile:
        watchlist = json.load(jsonFile)
        for index, item in enumerate(watchlist[chosen_list]):
            print(index, item['title'])

def add_item():
    pass

def remove_item():
    """prints watchlist with an index. Put in index to delete item from list and return it"""
    prt_list("watched_list")
    with open("database.txt", "w") as jsonFile:
        watchlist = json.load(jsonFile)
        


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
        else:
            return
    
if __name__ == "__main__":
    main()