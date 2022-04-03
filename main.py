import os
import datetime
import redditscrapper
import textclean

time = datetime.date.today().strftime("%d-%m-%Y")
filename = f'scrapes/{time}.csv'
os.makedirs(os.path.dirname(filename), exist_ok=True)

#redditscrapper.scrape(filename)
textclean.clean(filename) 
