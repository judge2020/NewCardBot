import praw
import asyncio
import threading
import os
from webhooks import webhook
from webhooks.senders import targeted

thewebhook = os.environ.get('WEBHOOK')
_clientid = os.environ.get('CLIENT_ID')
_clientsecret = os.environ.get('CLIENT_SECRET')

reddit = praw.Reddit(client_id=_clientid,
                     client_secret=_clientsecret,
                     user_agent='Judge2020/New Card bot hearthstone')

sub = reddit.subreddit('hearthstone')

cache = []

@webhook(sender_callable=targeted.sender)
def basic(url, redditurl):
    return {"content": redditurl}

def mainLoop():
    threading.Timer(30, mainLoop).start()
    new = sub.new(limit=15)
    for post in new:
        if post.shortlink in cache:
            continue
        cache.append(post.shortlink)
        if 'new' in post.title.lower() and 'card' in post.title.lower():
            basic(url=thewebhook, redditurl=post.shortlink)


mainLoop()