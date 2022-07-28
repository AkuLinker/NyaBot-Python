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
    check_language, user_check, registration, get_user, check_nsfw
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
    users_language = await check_language(user_id)
    text = constants.START_ANSWER[users_language]
    reply_markup = ReplyKeyboardMarkup(
        [['/info', '/list', '/random'], ['/about_me', '/settings']],
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
    users_language = await check_language(user_id)
    text = constants.INFORMATION[users_language]
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


async def info_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends list of supported subreddits"""
    log.debug('Function "info_list" called.')
    user_id = update.effective_user.id
    users_language = await check_language(user_id)
    text = constants.PRE_SUBREDDIT[users_language]
    for key, value in constants.SUBREDDITS.items():
        text += f'/get_{key} - {value[users_language]}\n'
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
    users_language = await check_language(user_id)
    text = constants.USER_INFO[users_language]
    text += 'ON' if user.nsfw_is_ok == True else 'OFF'
    await send_message_telegram(
        update=update,
        context=context,
        text=text
    )


async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.debug('Function "get" called.')
    user_id = update.effective_user.id
    nsfw_is_ok = await check_nsfw(user_id)
    plus_command = update.message.text.split('get_')
    subreddit = plus_command[1]
    if subreddit not in constants.SUBREDDITS.keys():
        text = (
            f'There is no subredit "{subreddit}".\n'
            'or I don\' send pictures from there.\n'
            'You can find list of subreddits in /list'
        )
        await send_message_telegram(
            update=update,
            context=context,
            text=text
        )
    else:
        print(not nsfw_is_ok)
        print(subreddit in constants.NSFW_SUBREDDITS)
        if not nsfw_is_ok and subreddit in constants.NSFW_SUBREDDITS:
            text = 'nsfw content in subreddit'
            await send_message_telegram(
                update=update,
                context=context,
                text=text
            )
            return None
        submission = await reddit_api.get_random_submission(subreddit)
        if not nsfw_is_ok:
            while submission.over_18:
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
    sub_list = list(set(constants.SUBREDDITS.keys()).difference(
        constants.NSFW_SUBREDDITS
    ))
    print(sub_list)
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
        'I don\'t react to text messages or this command.\n'
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
