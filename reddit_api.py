"""
 _   _             ____        _   
| \ | |           |  _ \      | |  
|  \| |_   _  __ _| |_) | ___ | |_ 
| . ` | | | |/ _` |  _ < / _ \| __|
| |\  | |_| | (_| | |_) | (_) | |_ 
|_| \_|\__, |\__,_|____/ \___/ \__|
        __/ |                      
       |___/                       

Telegram bot sending an anime girls pictures.
API reddit.
written on python.

author: AkuLinker
"""

import os
import random

import praw
from dotenv import load_dotenv

load_dotenv()

SUBREDDITS = {
    'Moescape':
    'ideally a balance between awe and awww~.',
    'MoeStash':
    'more moe girls.',
    'awwnime':
    'all kinds of moe art.',
    'wholesomeyuri':
    'a place for yuri lovers.',
    'AnimeBlush':
    'blushing anime girls.',
    'Smugs':
    'glorious smug anime faces.',
    'Joshi_Kosei':
    'SFW Fanart of 2D Girls in High School.',
    'tsunderes':
    'well, it\'s tsundere girls.',
    'AnimeLounging':
    'pics of people lounging around idly.',
    'animehotbeverages':
    'anime characters enjoy hot beverages.',
    'Animewallpaper':
    'Anime and anime-style wallpapers.',
    'TwoDeeArt':
    '2D and anime related art.',
    '2DArtchive':
    'more 2D arts.',
    'pantsu':
    'fanservicey art from manga, anime, VNs, JRPGs, etc.',
    'Patchuu':
    'a place for anime fanart with abstract.',
    'Usagimimi':
    'bunniegirls.',
    'kitsunemimi':
    'foxgirls.',
    'kemonomimi':
    'more animalgirls but not only fox or bunny.',
    'cutelittlefangs':
    'for fans of characters with fangs.',
    'headpats':
    'anime characters in need of or receiving headpats.',
    'ChurchofBelly':
    'place where appreciate the belly.',
    'animelegs':
    'place where appreciate the legs.',
    'ZettaiRyouiki':
    '("Absolute Territory")',
    'thighdeology':
    'more thighs but NSFW.',
    'twintails':
    'anime girls with twintails.',
    'pouts':
    'pouting girls and sometimes guys.',
    'gao':
    'cute anime girls making scary noises "gao!".',
    'tyingherhairup':
    'anime girls tying their hair up.',
    'animeponytails':
    'for those who have a fetish for ponytails.',
    'silverhair':
    'for all silver-haired waifu needs.',
    'longhairedwaifus':
    'dedicated to anime girls with long hair.',
    'shorthairedwaifus':
    'pictures of anime girls with short hair.',
    'OfficialSenpaiHeat':
    'art of cute girls. freedom of Weebs.',
}

reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USERAGENT'),
)


def get_random_submission(subreddit_name):
    submission = reddit.subreddit(subreddit_name).random()
    if submission is None:
        submissions = [
            one_submission
            for one_submission in reddit.subreddit(subreddit_name).hot(
                limit=20)
        ]
        random_number = random.randint(0, 20)
        submission = submissions[random_number]
    return submission


def make_text_answer(submission):
    if submission.over_18:
        nsfw = 'Yes'
    else:
        nsfw = 'No'
    text = (f'Here is your picture from r/{submission.subreddit}\n\n'
            f'Title: {submission.title}\n'
            f'Author of post: {submission.author}\n'
            f'Post url: https://www.reddit.com{submission.permalink}\n'
            f'Orogin url: {submission.url}\n'
            f'NSFW: {nsfw}\n')
    return text


def main():
    submission = get_random_submission('animeponytails')
    print(make_text_answer(submission))


if __name__ == '__main__':
    main()
