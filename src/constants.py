# Supported languages
LANGUAGES = [
    'english',
    'russian'
]

# For changing language
WICH_LANGUAGE = {
    'CALLBACK_ENGLISH_COMMAND': 'english',
    'CALLBACK_RUSSIAN_COMMAND': 'russian'
}

# For changing NSFW
WICH_NSFW = {
    'CALLBACK_NSFW_ON_COMMAND': True,
    'CALLBACK_NSFW_OFF_COMMAND': False
}

# Subreddits in supported languages
SUBREDDITS = {
    'Moescape': 'ideally a balance between awe and awww~.',
    'MoeStash': 'more moe girls.',
    'awwnime': 'all kinds of moe art.',
    'wholesomeyuri': 'a place for yuri lovers.',
    'AnimeBlush': 'blushing anime girls.',
    'Smugs': 'glorious smug anime faces.',
    'Joshi_Kosei': 'SFW Fanart of 2D Girls in High School.',
    'tsunderes': 'well, it\'s tsundere girls.',
    'AnimeLounging': 'pics of people lounging around idly.',
    'animehotbeverages': 'anime characters enjoy hot beverages.',
    'Animewallpaper': 'Anime and anime-style wallpapers.',
    'TwoDeeArt': '2D and anime related art.',
    '2DArtchive': 'more 2D arts.',
    'pantsu': 'fanservicey art from manga, anime, VNs, JRPGs, etc.',
    'Patchuu': 'a place for anime fanart with abstract.',
    'Usagimimi': 'bunniegirls.',
    'kitsunemimi': 'foxgirls.',
    'cutelittlefangs': 'for fans of characters with fangs.',
    'headpats': 'anime characters in need of or receiving headpats.',
    'ChurchofBelly': 'place where appreciate the belly.',
    'animelegs': 'place where appreciate the legs.',
    'ZettaiRyouiki': '("Absolute Territory")',
    'thighdeology': 'more thighs but NSFW.',
    'pouts': 'pouting girls and sometimes guys.',
    'gao': 'cute anime girls making scary noises "gao!".',
    'tyingherhairup': 'anime girls tying their hair up.',
    'twintails': 'anime girls with twintails.',
    'animeponytails': 'for those who have a fetish for ponytails.',
    'silverhair': 'for all silver-haired waifu needs.',
    'longhairedwaifus': 'dedicated to anime girls with long hair.',
    'shorthairedwaifus': 'pictures of anime girls with short hair.',
    'OfficialSenpaiHeat': 'art of cute girls. freedom of Weebs.',
}


# Buttons in supported languages
CHANGE_LANGUAGE_BUTTON = {
    'english': 'Change language',
    'russian': 'Изменить язык'
}
CHANGE_NSFW_BUTTON = {
    'english': 'nsfw (18+)',
    'russian': 'nsfw (18+)'
}
CLOSE_SETTINGS_BUTTON = {
    'english': 'Close settings',
    'russian': 'Закрыть настройки'
}

CHOOSE_ENGLISH_LANGUAGE = {
    'english': 'English',
    'russian': 'Английский'
}
CHOOSE_RUSSIAN_LANGUAGE = {
    'english': 'Russian',
    'russian': 'Русский'
}

CHOOSE_NSFW_ON = {
    'english': 'Switch nsfw on',
    'russian': 'Включить nsfw'
}
CHOOSE_NSFW_OFF = {
    'english': 'Switch nsfw off',
    'russian': 'Отключить nsfw'
}

BACK_BUTTON = {
    'english': 'Back',
    'russian': 'Вернуться'
}


# Notifications in conversation
CHANGED_LANGUAGE_NOTIFIVATION = {
    'english': 'language changed',
    'russian': 'Язык изменён'
}
CHANGED_NSFW_NOTIFIVATION = {
    'english': 'nsfw preferences changed',
    'russian': 'Предпочтения в nsfw изменены'
}


# Text answers in supported languages
SETTINGS = {
    'english': 'SETTINGS',
    'russian': 'НАСТРОЙКИ'
}
CHANGE_LANGUAGE_SETTINGS = {
    'english': 'LANGUAGE SETTINGS',
    'russian': 'НАСТРОЙКИ ЯЗЫКА'
}
CHANGE_NSFW_SETTINGS= {
    'english': 'NSFW SETTINGS (18+)',
    'russian': 'НАСТРОЙКИ NSFW (18+)'
}

START_ANSWER = {
    'english': (
        'Helo there!\n'
        'I\'m NyaBot. I can sand pictures of anime girls.\n'
        'For more information send /info\n'
        'For list of possible thems of pictures send me command /list\n'
        'You can change language and nsfw preferences '
        'in settings if you want.\n'
        'For that click on button settings or send me /settings command.'
    ),
    'russian': (
        'Привет!\n'
        'Меня зовут NyaBot. Я могу отправлять картинки с аниме девочками.\n'
        'Чтобы узнать больше пришли ине команду /info\n'
        'Чтобы получить список возможных тем картинок, '
        'пришли мне команду /list\n'
        'Ты можешь изменить язык и nsfw предпочтения '
        'в настройках, если захочешь.\n'
        'Для этого нажми на кнопку настройки или отправь мне команду /settings'
    )
}
INFORMATION = {
    'english': (
        'Pictures are taken from '
        '<a href="https://www.reddit.com/">reddit</a>.\n'
        'Use /get_(subreddit name) command to '
        'get random picture frome there.\n'
        'If you just want a random picture send me /random\n'
        'By default I dont send nsfw content.\n'
        'If you want to change it use /settings'
    ),
    'russian': (
        'Картинки берутся из <a href="https://www.reddit.com/">реддита</a>.\n'
        'Используй  команду /get_(Название сабреддита), '
        'чтобы получить рандомную картинку оттуда.\n'
        'Если тебе нужна просто рандомная картинка, используй команду /random\n'
        'Изначально я не шлю nsfw контент.\n'
        'Если хочешь изменить это, используй настройки /settings'
    )
}
USER_INFO = {
    'english': (
        'ABOUT YOU\n\n'
        'language: English\n'
        'NSFW(18+): '
    ),
    'russian': (
        'ИНФОРМАЦИЯ О ТЕБЕ\n\n'
        'Язык: Русский\n'
        'NSFW(18+): '
    )
}

