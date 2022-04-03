import pandas as pd
from unicodedata import name
import praw
import datetime
import os.path

#write csv file
def write(filename, scores, content):
    dataCSV = pd.DataFrame({'score': scores,'content': content})
    dataCSV.to_csv(filename)
        
#capturing Reddit
def scrape(filename):
    reddit = praw.Reddit(
        client_id = 'hV4Kn9_hkI3UhmjqNBhn1g',
        client_secret = '80GsxlWXoQJtvwZTnFJy4garYhy5Vw',
        user_agent = 'hideenuser74'
    )

    # setting and orginizating data
    subreddit = reddit.subreddit('stocks')
    topposts = subreddit.top('day')
    scores = []
    content = []

    #adding scrapes to data array
    for submission in topposts:
        content.append(submission.title + " " + submission.selftext)
        scores.append(submission.score)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            content.append(comment.body)
            scores.append(comment.score)

    #writing data
    write(filename, scores, content)
