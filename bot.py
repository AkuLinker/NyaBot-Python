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

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import reddit_api
from NyaBot_logging import log

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def send_message_telegram(context, chat_id, text, photo=None, button=False):
    log.debug('Function "send_message_telegram" called.')
    if button is True:
        reply_markup = ReplyKeyboardMarkup([['/info', '/random']],
                                           resize_keyboard=True)
    else:
        reply_markup = None
    if photo is None:
        context.bot.send_message(chat_id=chat_id,
                                 text=text,
                                 disable_web_page_preview=True,
                                 reply_markup=reply_markup)
        log.info(f'send message with text: {text[:37]}...')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=text,
                                 disable_web_page_preview=True)
        context.bot.send_photo(chat_id=chat_id, photo=photo)
        log.info(f'send message with text: {text[:37]}...')


def start(update, context):
    log.debug('Function "start" called.')
    text = (
        'Welcome to NyaBot paradise!\n'
        'To get more information about bot\'s\n commands send command /info')
    button = True
    send_message_telegram(context=context,
                          chat_id=update.effective_chat.id,
                          text=text,
                          button=button)


def info(update, context):
    log.debug('Function "info" called.')
    list_of_subreddits = ''
    for key, value in reddit_api.SUBREDDITS.items():
        list_of_subreddits += f'/get_{key} - {value}\n'
    text = ('I can send anime pictures from reddit.\n\n'
            '/random - send random picture from any subredit\n\n'
            'List of subreddits:\n'
            f'{list_of_subreddits}')
    send_message_telegram(context=context,
                          chat_id=update.effective_chat.id,
                          text=text)


def get(update, context):
    log.debug('Function "get" called.')
    plus_command = update.message.text.split('get_')
    subreddit = plus_command[1]
    if subreddit not in reddit_api.SUBREDDITS.keys():
        text = (f'There is no subredit "{subreddit}".\n'
                'or I don\' send pictures from there.\n'
                'You can find list of subreddits in /info')
        send_message_telegram(context=context,
                              chat_id=update.effective_chat.id,
                              text=text)
    else:
        submission = reddit_api.get_random_submission(subreddit)
        text = reddit_api.make_text_answer(submission)
        send_message_telegram(context=context,
                              chat_id=update.effective_chat.id,
                              text=text,
                              photo=submission.url)


def random(update, context):
    log.debug('Function "random" called.')
    sub_list = list(reddit_api.SUBREDDITS.keys())
    random_sub = choice(sub_list)
    submission = reddit_api.get_random_submission(random_sub)
    text = reddit_api.make_text_answer(submission)
    send_message_telegram(context=context,
                          chat_id=update.effective_chat.id,
                          text=text,
                          photo=submission.url)


def text_answer(update, context):
    log.debug('Function "text_answer" called.')
    text = ('I don\'t react to text messages.\n'
            'You can check correct commands here /info')
    send_message_telegram(context=context,
                          chat_id=update.effective_chat.id,
                          text=text)


def main():
    
    log.debug('Start of program.')
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('random', random))
    dispatcher.add_handler(CommandHandler('get', get))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'/get_'), get))
    dispatcher.add_handler(MessageHandler(Filters.all, text_answer))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
