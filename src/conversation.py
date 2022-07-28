from telegram import (
    Update,InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    CommandHandler, ContextTypes,
    ConversationHandler, CallbackQueryHandler
)

from loger import log
import constants
from db import AsyncSessionLocal
from db_control import (
    check_language, change_language_db, change_nsfw_db, get_user
)

# States
SETTINGS_STATE = 'SETTINGS_STATE'

# Callback data
CALLBACK_CHANGE_LANGUAGE_COMMAND = 'CALLBACK_CHANGE_LANGUAGE_COMMAND'
CALLBACK_CHANGE_NSFW_COMMAND = 'CALLBACK_CHANGE_NSFW_COMMAND'
CALLBACK_EXIT_COMMAND = 'CALLBACK_EXIT_COMMAND'

CALLBACK_ENGLISH_COMMAND = 'CALLBACK_ENGLISH_COMMAND'
CALLBACK_RUSSIAN_COMMAND = 'CALLBACK_RUSSIAN_COMMAND'

CALLBACK_NSFW_ON_COMMAND = 'CALLBACK_NSFW_ON_COMMAND'
CALLBACK_NSFW_OFF_COMMAND = 'CALLBACK_NSFW_OFF_COMMAND'

CALLBACK_BACK_COMMAND = 'CALLBACK_BACK_COMMAND'


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Sends to user settings inline buttons"""
    log.debug('Function "settings" called.')
    user_id = update.effective_user.id
    users_language = await check_language(user_id)
    settings_name = constants.SETTINGS[users_language]
    keyboard = [
        [
            InlineKeyboardButton(
                constants.CHANGE_LANGUAGE_BUTTON[users_language],
                callback_data=CALLBACK_CHANGE_LANGUAGE_COMMAND
            ),
            InlineKeyboardButton(
                constants.CHANGE_NSFW_BUTTON[users_language],
                callback_data=CALLBACK_CHANGE_NSFW_COMMAND
            ),
        ],
        [
            InlineKeyboardButton(
                constants.CLOSE_SETTINGS_BUTTON[users_language],
                callback_data=CALLBACK_EXIT_COMMAND
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    if query is not None:
        await query.edit_message_text(
            f'\n{settings_name}\n', reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            text=f'\n{settings_name}\n',
            reply_markup=reply_markup,
            chat_id=update.effective_chat.id,
        )
    return SETTINGS_STATE


async def change_language(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Sends to user inline buttons for changing language"""
    log.debug('Function "change_language" called.')
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    users_language = await check_language(user_id)
    settings_name = constants.CHANGE_LANGUAGE_SETTINGS[users_language]
    keyboard = [
        [
            InlineKeyboardButton(
                constants.CHOOSE_ENGLISH_LANGUAGE[users_language],
                callback_data=CALLBACK_ENGLISH_COMMAND
            ),
            InlineKeyboardButton(
                constants.CHOOSE_RUSSIAN_LANGUAGE[users_language],
                callback_data=CALLBACK_RUSSIAN_COMMAND
            ),
        ],
        [
            InlineKeyboardButton(
                constants.BACK_BUTTON[users_language],
                callback_data=CALLBACK_BACK_COMMAND
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f'\n{settings_name}\n', reply_markup=reply_markup
    )
    return SETTINGS_STATE


async def change_language_reaction(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Function for reaction on change language button"""
    log.debug('Function "change_language_reaction" called.')
    user_id = update.effective_user.id
    users_language = await check_language(user_id)
    query = update.callback_query
    chosen_language = constants.WICH_LANGUAGE[query.data]
    if users_language == chosen_language:
        answer = constants.NOT_CHANGED_LANGUAGE_NOTIFIVATION[users_language]
        await query.answer(text=answer)
        return SETTINGS_STATE
    await change_language_db(user_id, chosen_language)
    users_language = await check_language(user_id)
    answer = constants.CHANGED_LANGUAGE_NOTIFIVATION[users_language]
    await query.answer(text=answer)
    await change_language(update, context)
    return SETTINGS_STATE


async def change_nsfw(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Sends to user inline buttons for changing nsfw preferences"""
    log.debug('Function "change_nsfw" called.')
    user_id = update.effective_user.id
    users_language = await check_language(user_id)
    settings_name = constants.CHANGE_NSFW_SETTINGS[users_language]
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                constants.CHOOSE_NSFW_ON[users_language],
                callback_data=CALLBACK_NSFW_ON_COMMAND
            ),
            InlineKeyboardButton(
                constants.CHOOSE_NSFW_OFF[users_language],
                callback_data=CALLBACK_NSFW_OFF_COMMAND
            ),
        ],
        [
            InlineKeyboardButton(
                constants.BACK_BUTTON[users_language],
                callback_data=CALLBACK_BACK_COMMAND
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f'\n{settings_name}\n', reply_markup=reply_markup
    )
    return SETTINGS_STATE


async def change_nsfw_reaction(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Function for reaction on change nsfw button"""
    log.debug('Function "change_nsfw_reaction" called.')
    user_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        user = await get_user(user_id, session)
    users_language =  user.language
    query = update.callback_query
    chosen_preference = constants.WICH_NSFW[query.data]
    if not user.nsfw_is_ok == chosen_preference:
        await change_nsfw_db(user_id, chosen_preference)
    answer = constants.CHANGED_NSFW_NOTIFIVATION[users_language]
    await query.answer(text=answer)
    return SETTINGS_STATE


async def close_settings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    log.debug('Function "close_settings" called.')
    query = update.callback_query
    await query.answer(text='settings closed')
    await query.delete_message()


async def back_to_settings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    log.debug('Function "back_to_settings" called.')
    query = update.callback_query
    await query.answer(text='returnd to settings menu')
    await settings(update, context)


conv_handler = ConversationHandler(
    allow_reentry=True,
    conversation_timeout=300,
    entry_points=[CommandHandler('settings', settings)],
    states={
        SETTINGS_STATE: [
            CallbackQueryHandler(
                change_language,
                pattern=CALLBACK_CHANGE_LANGUAGE_COMMAND
            ),
            CallbackQueryHandler(
                change_nsfw,
                pattern=CALLBACK_CHANGE_NSFW_COMMAND
            ),
            CallbackQueryHandler(
                change_language_reaction,
                pattern=CALLBACK_ENGLISH_COMMAND
            ),
            CallbackQueryHandler(
                change_language_reaction,
                pattern=CALLBACK_RUSSIAN_COMMAND
            ),
            CallbackQueryHandler(
                change_nsfw_reaction,
                pattern=CALLBACK_NSFW_ON_COMMAND
            ),
            CallbackQueryHandler(
                change_nsfw_reaction,
                pattern=CALLBACK_NSFW_OFF_COMMAND
            ),
            CallbackQueryHandler(
                back_to_settings,
                pattern=CALLBACK_BACK_COMMAND
            )
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            close_settings,
            pattern=CALLBACK_EXIT_COMMAND
        )
    ],
)
