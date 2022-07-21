"""
 _   _             ____        _   
| \ | |           |  _ \      | |  
|  \| |_   _  __ _| |_) | ___ | |_ 
| . ` | | | |/ _` |  _ < / _ \| __|
| |\  | |_| | (_| | |_) | (_) | |_ 
|_| \_|\__, |\__,_|____/ \___/ \__|
        __/ |                      
       |___/                       

Telegram bot sending random anime girls pictures.
Written on python. API reddit.
GitHub: https://github.com/AkuLinker/NyaBot-Python
Telegram: @NyaPicturesBot

author: AkuLinker
"""

import os
from random import choice

import praw
from dotenv import load_dotenv

from NyaBot_logging import log

load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USERAGENT'),
)


def get_random_submission(subreddit_name):
    log.debug(f'Function "get_random_submission" called for {subreddit_name}.')
    submission = reddit.subreddit(subreddit_name).random()
    if submission is None:
        log.debug(f'Method "random" don\'t work in subreddit {subreddit_name}')
        submissions = [
            one_submission
            for one_submission in reddit.subreddit(subreddit_name).hot(
                limit=50)
        ]
        random_number = choice(list(range(0, 50)))
        log.debug(f'Hot of subreddit {subreddit_name} number {random_number}.')
        submission = submissions[random_number]
    while not (submission.url[-3:] == 'png' or submission.url[-3:] == 'jpg'):
        log.debug(f'Post {random_number} has inappropriate capture.')
        submissions = [
            one_submission
            for one_submission in reddit.subreddit(subreddit_name).hot(
                limit=50)
        ]
        random_number = choice(list(range(0, 50)))
        submission = submissions[random_number]
        if submission.url[-3:] == 'png' or submission.url[-3:] == 'jpg':
            log.debug(f'Hot of subreddit {subreddit_name} '
                        f'number {random_number}.')
            is_capture = True
    return submission


def make_text_answer(submission):
    log.debug('Function "make_text_answer" called.')
    if submission.over_18:
        nsfw = 'Yes'
    else:
        nsfw = 'No'
    text = (f'Here is your picture from r/{submission.subreddit}\n\n'
            f'Title: {submission.title}\n'
            f'Author of post: {submission.author}\n'
            f'Post url: https://www.reddit.com{submission.permalink}\n'
            f'Origin url: {submission.url}\n'
            f'NSFW: {nsfw}\n')
    return text
