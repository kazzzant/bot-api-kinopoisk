from loader import bot
from tg_API.states import MyStates
from tg_API.button import menu_begin
from logs.log import logger


def send_hello(message) -> None:
    """
    выводит на экран строку приветствия
    """
    bot.send_message(message.chat.id,
                     "Привет, {}! Давай посмотрим рейтинги фильмов и передач?".
                     format(message.from_user.first_name))


def start_menu(user_id, chat_id) -> None:
    """
    устанавливает пользователю статус MyStates.start
    выводит на экран стартовое меню
    """
    bot.set_state(user_id, MyStates.start, chat_id)
    logger.info(f'пользователь {user_id} в главном меню. state=start')
    bot.send_message(chat_id, text='<b>Выбирайте:</b>', reply_markup=menu_begin(), parse_mode='HTML')


@bot.message_handler(commands=['hello-world', 'start', 'Start'])
def start_message(message) -> None:
    """
    обрабатывает команды /hello-world, /start
    """
    logger.info(f'пользователь {message.from_user.id} {message.from_user.first_name} запустил главное меню')
    send_hello(message)
    start_menu(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'start')
def first_menu(call) -> None:
    """
    Обрабатывает нажатие кнопки 'В главное меню'
    """
    start_menu(call.from_user.id, call.message.chat.id)


@bot.message_handler(commands=['help'])
def help_message(message) -> None:
    """
    обрабатывает команду /help
    выводит на экран список доступных команд
    """
    logger.info(f'пользователь {message.from_user.id} {message.from_user.first_name} ввёл команду /help')
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                                      '/help - получить справку о работе бота\n'
                                      '/low - получить список фильмов с низким рейтингом\n'
                                      '/high - получить список фильмов с высоким рейтингом\n'
                                      '/custom - получить список фильмов в соответствии с настройками пользователя\n'
                                      '/history — вывод истории запросов пользователей\n'
                                      'но, гораздо удобнее воспользоваться кнопками меню:')
    start_menu(message.from_user.id, message.chat.id)
