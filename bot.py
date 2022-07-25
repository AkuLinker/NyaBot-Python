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
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, filters,
    Defaults, MessageHandler, ConversationHandler
)

import reddit_api
from NyaBot_logging import log
from subreddits import SUBREDDITS

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

SETTINGS, PROCESS = range(2)


async def send_message_telegram(
    context, chat_id, text, photo=None, button=False
):
    log.debug('Function "send_message_telegram" called.')
    if button is True:
        reply_markup = ReplyKeyboardMarkup(
            [['/info', '/random']],
            resize_keyboard=True
        )
    else:
        reply_markup = None
    if photo is None:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        log.info('send message')
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=text
        )
        log.info('send message with photo')


async def start(update, context):
    """
    Responds to the start command. The entry point to telegram bot.
    """
    log.debug('Function "start" called.')
    text = (
        'Welcome to NyaBot paradise!\n'
        'To get more information about bot\'s\n commands send command /info'
    )
    await send_message_telegram(
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        button=True
    )


async def info(update, context):
    log.debug('Function "info" called.')
    list_of_subreddits = ''
    for key, value in SUBREDDITS.items():
        list_of_subreddits += f'/get_{key} - {value}\n'
    text = (
        'I can send anime pictures from reddit.\n\n'
        '/random - send random picture from any subredit\n\n'
        'List of subreddits:\n'
        f'{list_of_subreddits}'
    )
    await send_message_telegram(
        context=context,
        chat_id=update.effective_chat.id,
        text=text
    )


async def get(update, context):
    log.debug('Function "get" called.')
    plus_command = update.message.text.split('get_')
    subreddit = plus_command[1]
    if subreddit not in SUBREDDITS.keys():
        text = (
            f'There is no subredit "{subreddit}".\n'
            'or I don\' send pictures from there.\n'
            'You can find list of subreddits in /info'
        )
        send_message_telegram(
            context=context,
            chat_id=update.effective_chat.id,
            text=text
        )
    else:
        submission = await reddit_api.get_random_submission(subreddit)
        text = await reddit_api.make_text_answer(submission)
        await send_message_telegram(
            context=context,
            chat_id=update.effective_chat.id,
            text=text,
            photo=submission.url
        )


async def random(update, context):
    log.debug('Function "random" called.')
    sub_list = list(SUBREDDITS.keys())
    random_sub = choice(sub_list)
    submission = await reddit_api.get_random_submission(random_sub)
    text = await reddit_api.make_text_answer(submission)
    await send_message_telegram(
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        photo=submission.url
    )


async def text_answer(update, context):
    log.debug('Function "text_answer" called.')
    text = (
        'I don\'t react to text messages.\n'
        'You can check correct commands here /info'
    )
    await send_message_telegram(
        context=context,
        chat_id=update.effective_chat.id,
        text=text
    )


if __name__ == '__main__':
    log.debug('Start of program.')

    defaults = Defaults(
        parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
    application = ApplicationBuilder().token(TOKEN).defaults(defaults).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('info', info))
    application.add_handler(CommandHandler('random', random))
    application.add_handler(CommandHandler('get', get))
    application.add_handler(MessageHandler(filters.Regex(r'/get_'), get))
    application.add_handler(MessageHandler(filters.ALL, text_answer))

    application.run_polling()
