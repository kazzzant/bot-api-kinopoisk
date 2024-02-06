from loader import bot
from telebot import custom_filters
from tg_API.states import MyStates
from tg_API.hello_handlers import start_menu, send_hello  # Убрать
from tg_API.rating_handlers import set_parameters, get_parameters, menu_custom, api_request
from datetime import datetime
from logs.log import logger
import tg_API.hello_handlers
import tg_API.rating_handlers
import tg_API.history_handlers


countries_api = {}


@bot.message_handler(state=MyStates.start)
def state_start(message) -> None:
    """
    обрабатывает ответ пользователя, имеющего статус MyStates.start
    """
    bot.send_message(message.chat.id,
                     text='{}! Используйте меню.\n'.
                     format(message.from_user.first_name))
    tg_API.hello_handlers.start_menu(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.low)
def states_low(message) -> None:
    """
    обрабатывает ответ пользователя, имеющего статус MyStates.low
    """
    bot.send_message(message.chat.id, text='{}! Нажимайте на кнопки меню.\n'.
                     format(message.from_user.first_name))


@bot.message_handler(state=MyStates.high)
def states_high(message) -> None:
    """
    обрабатывает ответ пользователя, имеющего статус MyStates.high
    """
    bot.send_message(message.chat.id, text='{}! Нажимайте на кнопки меню.\n'.
                     format(message.from_user.first_name))


@bot.message_handler(state=MyStates.custom_year_low, is_digit=True)
def states_custom_year_low(message) -> None:
    """
    обрабатывает ответ пользователя (число), имеющего статус MyStates.custom_year_low
    проверяет попадает ли число в нужный диапазон и
    устанавливает нижнюю границу диапазона года выхода фильма
    """
    user_id = message.from_user.id
    year_low = message.text
    if 1890 <= int(year_low) <= datetime.now().year:
        year_str = year_low + ' - ' + str(datetime.now().year)
        set_parameters(user_id, 'year', year_str)
        set_parameters(user_id, 'm_year', 'в диапазоне ' + year_str + 'гг.')
        bot.set_state(user_id, MyStates.custom_year_high, message.chat.id)
        bot.send_message(message.chat.id, '📆 Введите максимальный год диапазона')
    else:
        bot.send_message(message.chat.id, f'значение {year_low} не входит в диапазон')


@bot.message_handler(state=MyStates.custom_year_low, is_digit=False)
def custom_year_low_incorrect(message) -> None:
    """
    обрабатывает ответ пользователя (не число), имеющего статус MyStates.custom_year_low
    """
    bot.send_message(message.chat.id, 'Вводить можно только цифры')
    text = '📆 Задайте начальный год (от 1890 до {}):'.format(datetime.now().year)
    bot.send_message(message.from_user.id, text)


@bot.message_handler(state=MyStates.custom_year_high, is_digit=True)
def states_custom_year_high(message) -> None:
    """
     обрабатывает ответ пользователя (число), имеющего статус MyStates.custom_year_high
     проверяет попадает ли число в нужный диапазон и
     устанавливает верхнюю границу диапазона года выхода фильма
     """
    user_id = message.from_user.id
    year_low = get_parameters(user_id)['year'][:4]
    year_high = message.text
    year_max = datetime.now().year
    range_year = year_low + ' - ' + str(year_max)
    if int(year_low) <= int(year_high) <= year_max:
        year_str = year_low + ' - ' + year_high
        set_parameters(user_id, 'year', year_str)
        set_parameters(user_id, 'm_year', 'в диапазоне ' + year_str + 'гг.')
        menu_custom(user_id, message.chat.id)
    else:
        bot.send_message(message.chat.id, f'значение {year_high} не входит в диапазон {range_year}')
        bot.send_message(message.chat.id, '📆 Введите максимальный год диапазона')


@bot.message_handler(state=MyStates.custom_year_high, is_digit=False)
def custom_year_high_incorrect(message) -> None:
    """
    обрабатывает ответ пользователя (не число), имеющего статус MyStates.custom_year_high
    """
    bot.send_message(message.chat.id, 'Вводить можно только цифры')
    bot.send_message(message.chat.id, '📆 Введите максимальный год диапазона')


@bot.message_handler(state=MyStates.custom_rating_low, is_digit=True)
def states_custom_year_low(message) -> None:
    """
    обрабатывает ответ пользователя (число), имеющего статус MyStates.custom_rating_low
    проверяет попадает ли число в нужный диапазон и
    устанавливает нижнюю границу диапазона рейтинга фильма
    """
    user_id = message.from_user.id
    rating_low = message.text
    if 0 <= int(rating_low) <= 10:
        rating_str = rating_low + ' - ' + '10'
        set_parameters(user_id, 'rating', rating_str)
        set_parameters(user_id, 'm_rating', 'в диапазоне: ' + rating_str)
        bot.set_state(user_id, MyStates.custom_rating_high, message.chat.id)
        bot.send_message(message.chat.id, '📈 Введите максимальный рейтинг диапазона')
    else:
        bot.send_message(message.chat.id, f'значение {rating_low} не входит в диапазон')


@bot.message_handler(state=MyStates.custom_rating_low, is_digit=False)
def custom_year_low_incorrect(message) -> None:
    """
    обрабатывает ответ пользователя (не число), имеющего статус MyStates.custom_rating_low
    """
    bot.send_message(message.chat.id, 'Вводить можно только цифры')
    bot.send_message(message.from_user.id, '📈 Задайте начальное значение рейтинга (от 0 до 10):')


@bot.message_handler(state=MyStates.custom_rating_high, is_digit=True)
def states_custom_year_high(message) -> None:
    """
    обрабатывает ответ пользователя (число), имеющего статус MyStates.custom_rating_high
    проверяет попадает ли число в нужный диапазон и
    устанавливает верхнюю границу диапазона рейтинга фильма
    """
    user_id = message.from_user.id
    rating_low = get_parameters(user_id)['rating'][:2].strip()
    rating_high = message.text
    range_rating = rating_low + ' - ' + '10'
    if int(rating_low) <= int(rating_high) <= 10:
        rating_str = rating_low + ' - ' + rating_high
        set_parameters(user_id, 'rating', rating_str)
        set_parameters(user_id, 'm_rating', 'в диапазоне ' + rating_str)
        menu_custom(user_id, message.chat.id)
    else:
        bot.send_message(message.chat.id, f'значение {rating_high} не входит в диапазон {range_rating}')
        bot.send_message(message.chat.id, '📈 Введите максимальный рейтинг диапазона')


@bot.message_handler(state=MyStates.custom_rating_high, is_digit=False)
def custom_year_high_incorrect(message) -> None:
    """
    обрабатывает ответ пользователя (не число), имеющего статус MyStates.custom_rating_high
    """
    bot.send_message(message.chat.id, 'Вводить можно только цифры')
    bot.send_message(message.chat.id, '📈 Введите максимальный рейтинг диапазона')


def get_countries() -> None:
    """
    загружает список стран в словарь countries_api
    ключ - название страны в нижнем регистре
    значение - название страны загруженное с сайта
    """
    query = {'field': 'countries.name'}
    result, movies = api_request(query, url_address='v1/movie/possible-values-by-field?')
    if result:
        if len(movies) == 0:
            logger.warning('Список стран не загрузился!')
        else:
            countries_api.update({elem['name'].lower(): elem['name'] for elem in movies})
            logger.warning('Сформировали список стран!')
    else:
        logger.error('ошибка загрузки списка стран')


@bot.message_handler(state=MyStates.custom_countries)
def states_custom_year_high(message) -> None:
    """
    обрабатывает ответ пользователя, имеющего статус MyStates.custom_countries
    устанавливает фильтр: страна фильма.
    если значение, введенное пользователем не найдено в словаре, то страна - любая
    """
    user_id = message.from_user.id
    if not countries_api:
        get_countries()
    countries = countries_api.get(message.text.lower(), 'любая')
    countries_parameters = countries
    if countries == 'любая':
        countries_parameters = '!null'
        bot.send_message(message.chat.id, '🌐 Бот не будет учитывать страну')
    set_parameters(user_id, 'countries', countries_parameters)
    set_parameters(user_id, 'm_countries', countries)
    menu_custom(user_id, message.chat.id)


@bot.message_handler(state=None)
def text_messages(message) -> None:
    """
    обрабатывает ответы пользователя, пока статус не установлен
    """
    if message.text.lower() in ('привет', 'старт', 'start'):
        send_hello(message)
    else:
        bot.send_message(message.chat.id, text='{}! Я не умею болтать.\n'
                                               'Могу предоставить инфу по разным фильмам'.
                         format(message.from_user.first_name))
    start_menu(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
