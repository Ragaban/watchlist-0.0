#classes

class Movie:
    def __init__(self, title, id, description, image, watched_date = ''):
        self.title = title 
        self.id = id 
        self.description = description
        self.image = image
        self.watch_status =  False
        if watched_date == '':  
            pass
        else: 
            self.watched_date = watched_date
    
    def watched_it(self):
        self.watch_status = True
    
    

