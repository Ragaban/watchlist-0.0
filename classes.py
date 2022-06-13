#classes
import json
from dataclasses import dataclass
from re import M

@dataclass
class Movie:
    title : str
    id : str
    description : str
    image : str
    watch_status = False
    
    def set_watch_status(self):
        self.watch_status = True

    def set_watched_date(self, watched_date: str) -> None:
        self.watched_date = watched_date
    