import os
import logging
import reddit_api
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    text = (
        'Welcome to NyaBot paradise!\n'
        'To get more information about bot\'s\n commands send command /info')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def info(update, context):
    list_of_subreddits = ''
    for key, value in reddit_api.SUBREDDITS.items():
        list_of_subreddits += f'/get_{key} - {value}\n'
    text = ('I can send anime pictures from reddit.\n\n'
            '/random - send random picture from any subredit\n\n'
            'List of subreddits:\n'
            f'{list_of_subreddits}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get(update, context):
    plus_command = update.message.text.split('_')
    subreddit = plus_command[1]
    if subreddit not in reddit_api.SUBREDDITS.keys():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'There is no subredit "{subreddit}".\n'
                                 'or I don\' send pictures from there.\n'
                                 'You can find list of subreddits in /info')
    submission = reddit_api.get_random_submission(subreddit)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=reddit_api.make_text_answer(submission),
                             disable_web_page_preview=True)
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=submission.url)


def random(update, context):
    sub_list = list(reddit_api.SUBREDDITS.keys())
    print(sub_list)
    random_sub = choice(sub_list)
    submission = reddit_api.get_random_submission(random_sub)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=reddit_api.make_text_answer(submission),
                             disable_web_page_preview=True)
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=submission.url)


def text_answer(update, context):
    text = ('I don\'t react to text messages.\n'
            'You can check correct commands here /info')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main():
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
