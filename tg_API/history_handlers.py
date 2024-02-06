from loader import bot
from tg_API.states import MyStates
from logs.log import logger
from database.db import History
from tg_API.button import menu_header_text_rating
from tg_API.hello_handlers import start_menu


def get_history(user_id: int, chat_id: int) -> None:
    """
    устанавливает пользователю статус MyStates.history
    формирует запрос в базу данных по конкретному пользователю
    обрабатывает полученный ответ
    выводит на экран 10 последних запросов пользователя
    """
    bot.set_state(user_id, MyStates.history, chat_id)
    count = History.select().where(History.user_id == user_id).count()
    logger.info(f'пользователь {user_id} смотрит историю. Найдено {count} записей')
    text = f'Количество сохранившихся запросов: {count}.'
    bot.send_message(chat_id, text)
    if count > 0:
        query = History.select().limit(10).where(History.user_id == user_id).order_by(History.date.desc()).dicts()
        for param_dict in query:
            date_writing = param_dict['date']
            text = f'Запись от: {date_writing}'
            bot.send_message(chat_id, text)
            bot.send_message(chat_id,
                             text=menu_header_text_rating(param_dict),
                             parse_mode='HTML')
    start_menu(user_id, chat_id)
    return


@bot.callback_query_handler(func=lambda c: c.data == 'bt_history')
def bt_low_message(call) -> None:
    """
    Обрабатывает нажатие кнопки 'история запросов'
    """
    get_history(call.from_user.id, call.message.chat.id)


@bot.message_handler(commands=['history'])
def cmd_low_message(message) -> None:
    """
    Обрабатывает команду /history
    """
    get_history(message.from_user.id, message.chat.id)
