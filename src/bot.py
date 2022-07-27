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
from telegram import (
    Update, ReplyKeyboardMarkup
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, filters, ContextTypes,
    Defaults, MessageHandler
)

import reddit_api
from loger import log
import constants
from db_control import (
    check_language, user_check, registration, get_user
)
from conversation import conv_handler
from db import AsyncSessionLocal

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to the start command. The entry point to telegram bot.
    """
    log.debug('Function "start" called.')
    user_id = update.effective_user.id
    if not await user_check(user_id):
        await registration(user_id)
    text = await check_language(user_id, constants.START_ANSWER)
    reply_markup = ReplyKeyboardMarkup(
        [['/list', '/random'], ['/about_me', '/settings']],
        resize_keyboard=True
    )
    await send_message_telegram(
        update=update,
        context=context,
        text=text,
        reply_markup=reply_markup
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends information about bot functional"""
    log.debug('Function "info" called.')
    user_id = update.effective_user.id
    text = await check_language(user_id, constants.INFORMATION)
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


async def info_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends list of recommended subreddits"""
    log.debug('Function "info_list" called.')
    list_of_subreddits = ''
    for key, value in constants.SUBREDDITS.items():
        list_of_subreddits += f'/get_{key} - {value}\n'
    text = (
        'LIST OF SUBREDDITS.\n\n'
        '/random - send random picture from any subredit\n\n'
        f'{list_of_subreddits}'
    )
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


async def about_user(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends information about user"""
    log.debug('Function "about_user" called.')
    user_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        user = await get_user(user_id, session)
    text = await check_language(user_id, constants.USER_INFO)
    text += 'ON' if user.nsfw_is_ok == True else 'OFF'
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.debug('Function "get" called.')
    plus_command = update.message.text.split('get_')
    subreddit = plus_command[1]
    if subreddit not in constants.SUBREDDITS.keys():
        text = (
            f'There is no subredit "{subreddit}".\n'
            'or I don\' send pictures from there.\n'
            'You can find list of subreddits in /info'
        )
        send_message_telegram(
            update=update,
            context=context,
            text=text
        )
    else:
        submission = await reddit_api.get_random_submission(subreddit)
        text = await reddit_api.make_text_answer(submission)
        await send_message_telegram(
            update=update,
            context=context,
            text=text,
            photo=submission.url
        )


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.debug('Function "random" called.')
    sub_list = list(constants.SUBREDDITS.keys())
    random_sub = choice(sub_list)
    submission = await reddit_api.get_random_submission(random_sub)
    text = await reddit_api.make_text_answer(submission)
    await send_message_telegram(
        update=update,
        context=context,
        text=text,
        photo=submission.url
    )


async def send_message_telegram(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    photo: str=None,
    reply_markup: ReplyKeyboardMarkup=None
) -> None:
    log.debug('Function "send_message_telegram" called.')
    if photo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
        log.info('send message')
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text
        )
        log.info('send message with picture')


async def text_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    log.debug('Function "text_answer" called.')
    text = (
        'I don\'t react to text messages.\n'
        'You can check correct commands here /info'
    )
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


if __name__ == '__main__':
    log.debug('Start of program.')

    defaults = Defaults(
        parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
    application = ApplicationBuilder().token(TOKEN).defaults(defaults).build()

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('info', info))
    application.add_handler(CommandHandler('list', info_list))
    application.add_handler(CommandHandler('about_me', about_user))
    application.add_handler(CommandHandler('random', random))
    application.add_handler(CommandHandler('get', get))
    application.add_handler(MessageHandler(filters.Regex(r'/get_'), get))
    application.add_handler(MessageHandler(filters.ALL, text_answer))

    application.run_polling()
