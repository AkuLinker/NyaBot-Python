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

import asyncpraw
from dotenv import load_dotenv

from loger import log

LIST_OF_NUMBERS = list(range(0, 50))

load_dotenv()


reddit = asyncpraw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USERAGENT'),
)


async def choose_submission(subreddit):
    log.debug(f'Function "choose_submission" called')
    submissions = [
        one_submission async for one_submission in subreddit.hot(limit=50)
    ]
    random_number = choice(LIST_OF_NUMBERS)
    submission = submissions[random_number]
    log.debug(
        f'Chosen hot of subreddit {subreddit.display_name} '
        f'number {random_number}.'
    )
    return submission


async def get_random_submission(subreddit_name):
    log.debug(f'Function "get_random_submission" called for {subreddit_name}.')
    subreddit = await reddit.subreddit(subreddit_name)
    submission = await subreddit.random()
    if submission is None:
        log.debug(f'Method "random" don\'t work in subreddit {subreddit_name}')
        submission = await choose_submission(subreddit)
    while not submission.url[-3:] in ('png', 'jpg'):
        log.debug(f'Chosen post has inappropriate capture.')
        submission = await choose_submission(subreddit)
    return submission


async def make_text_answer(submission):
    log.debug('Function "make_text_answer" called.')
    nsfw = 'Yes' if submission.over_18 else 'No'
    text = (f'✓ <b>Picture from:</b> r/{submission.subreddit}\n'
            f'✓ <b>Title:</b> {submission.title}\n'
            f'✓ <b>Author of post:</b> {submission.author}\n'
            f'✓ <b>Post url:</b> https://www.reddit.com{submission.permalink}\n'
            f'✓ <b>Origin url:</b> {submission.url}\n'
            f'✓ <b>NSFW:</b> {nsfw}\n')
    return text
