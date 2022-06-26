#classes

class Movie:
    def __init__(self, title, id, description, image, watched_date):
        self.title = title 
        self.id = id 
        self.description = description
        self.image = image
        if watched_date == '':  
            pass
        else: 
            self.watched_date = watched_date
    
    def __repr__(self):
        return f"Movie: {self.title}, {self.description}"
    
    

