from loader import bot
from telebot import types
from tg_API.states import MyStates
from tg_API.button import menu_check, menu_set_filter_rating, menu_header_text_rating
from site_API.data_api import api_request
from logs.log import logger
from database.db import History
from datetime import datetime


rating_menu = {'kp': 'КиноПоиск', 'imdb': 'IMDb'}

type_menu = {'1': 'фильм', '2': 'сериал', '3': 'мультфильм', '4': 'аниме',
             '5': 'мультсериал', '6': 'TV-шоу', '!null': 'не важно'}

countries_menu = {'Россия': 'Россия', 'СССР': 'СССР', 'Индия': 'Индия',
                  'США': 'США', 'Китай': 'Китай', 'Гонконг': 'Гонконг',
                  'Франция': 'Франция', 'Италия': 'Италия', '!null': 'любая'}
year_menu = {'2023': '2023г.', '2022': '2022г.', '2021': '2021г.', '2020': '2020г.', '2010-2019': '2010-2019',
             '2000-2009': '2000-2009', '1992-1999': '1992-1999', '1890 - 1991': 'до 1991', '!null': 'не важно'}

start_parameters = {'rating_type': 'kp', 'rating': '!null', 'typeNumber': '!null',
                    'countries': '!null', 'year': '!null',
                    'm_rating_type': 'КиноПоиск', 'm_rating': 'в диапазоне: 0-10', 'm_type': 'любой',
                    'm_countries': 'любая', 'm_year': 'любой'}


def get_parameters_name(my_user_id: int) -> str:
    """
    возвращает имя словаря с параметрами фильтра пользователя в соответствии с его статусом (пунктом меню)
    """
    parameters = 'parameters_' + bot.get_state(my_user_id)[9:12]
    return parameters


def create_filter_rating(my_user_id: int, sort_type: str, sort: str):
    """
    создает словарь с параметрами фильтра для пользователя из шаблона start_parameters
    в соответствии со статусом (пунктом меню)
    """
    parameters = get_parameters_name(my_user_id)
    with bot.retrieve_data(my_user_id) as data:
        if data.get(parameters):
            return
        data[parameters] = {}
        data[parameters]['sortType'] = sort_type
        data[parameters].update(start_parameters)
        data[parameters]['m_sort'] = sort

        return


def get_parameters(my_user_id: int) -> dict:
    """
    возвращает параметры фильтра для пользователя в соответствии со статусом (пунктом меню)
    """
    name_dict = get_parameters_name(my_user_id)
    with bot.retrieve_data(my_user_id) as data:
        return data[name_dict]


def set_parameters(my_user_id: int, my_key: str, my_value: str) -> None:
    """
    устанавливает значение my_value ключу my_key в словаре с параметрами фильтра пользователя my_user_id
    в соответствии со статусом (пунктом меню)
    :param my_user_id: id пользователя
    :param my_key: ключ
    :param my_value: значение
    :return: None
    """
    name_dict = get_parameters_name(my_user_id)
    logger.info(f'пользователь {my_user_id} в словаре {name_dict} установил {my_key}={my_value}')
    with bot.retrieve_data(my_user_id) as data:
        data[name_dict][my_key] = my_value
    return


def save_history(user_id: int) -> None:
    """
    запись текущих параметров фильтра пользователя в базу данных
    """
    my_parameters = get_parameters(user_id)
    state = bot.get_state(user_id)[9:]
    History.create(user_id=user_id, state=state, **my_parameters)


def text_query_rating(user_id: int) -> dict:
    """
    возвращает параметры для дальнейшей передачи в запросе на сайт КиноПоиска
    """
    my_parameters = get_parameters(user_id)
    save_history(user_id)
    field_rating = my_parameters['rating_type']
    query = {'selectFields': 'id | rating.{} | name | typeNumber | year | countries.name | movieLength'
                             ''.format(field_rating),
             'sortField': 'rating.{}'.format(field_rating),
             'sortType': '{}'.format(my_parameters['sortType']),
             'page': '1',
             'limit': '5',
             'name': '!null',
             'rating.{}'.format(field_rating): '{}'.format(my_parameters['rating']),
             'typeNumber': '{}'.format(my_parameters['typeNumber']),
             'countries.name': '{}'.format(my_parameters['countries']),
             'year': '{}'.format(my_parameters['year'])}
    logger.info(f'пользователь {user_id} сформировал запрос {query}')
    return query


def print_movies(call: types.CallbackQuery, my_movies: list) -> None:
    """
    Выводит на экран пользователя информацию о фильмах
    """
    for elem in my_movies:
        logger.info(f'получено: {elem}')
        countries_list = ''
        for countries_name in elem['countries']:
            if countries_list:
                countries_list += ', '
            countries_list += countries_name['name']
        message = '📈 {}  <b>"{}"</b>\n{},  {}\n{}   {}г.'. \
            format(elem['rating'][get_parameters(call.from_user.id)['rating_type']],
                   elem['name'],
                   type_menu[str(elem['typeNumber'])],
                   str(elem['movieLength']) + ' мин' if elem['movieLength'] is not None else '',
                   countries_list,
                   elem['year'])
        bot.send_message(call.from_user.id, text=message, parse_mode='HTML')


def message_check(call: types.CallbackQuery, my_text: str, my_markup: types.InlineKeyboardMarkup) -> None:
    """
    выводит пользователю меню с текстом и кнопки с вариантами для  выбора значений конкретного фильтра
    """
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="<b>" + my_text + "</b>",
                          reply_markup=my_markup,
                          parse_mode='HTML')
    return


def menu_button_rating(call: types.CallbackQuery) -> None:
    """
    выводит пользователю меню с текстом и кнопки с вариантами выбора фильтра
    """
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=menu_header_text_rating(get_parameters(user_id), bot.get_state(user_id)[9:12]),
                          reply_markup=menu_set_filter_rating(bot.get_state(user_id)[9:12]),
                          parse_mode='HTML')
    return


def menu_low(user_id: int, chat_id: int) -> None:
    """
    устанавливает статус пользователю MyStates.low
    выводит меню соответствующее команде /low
    """
    bot.set_state(user_id, MyStates.low, chat_id)
    create_filter_rating(user_id, '1', 'низким')
    logger.info(f'пользователь {user_id} запустил меню LOW. state=low')
    bot.send_message(chat_id,
                     text=menu_header_text_rating(get_parameters(user_id)),
                     reply_markup=menu_set_filter_rating(),
                     parse_mode='HTML')


def menu_high(user_id: int, chat_id: int) -> None:
    """
    устанавливает статус пользователю MyStates.high
    выводит меню соответствующее команде /high
    """
    bot.set_state(user_id, MyStates.high, chat_id)
    create_filter_rating(user_id, '-1', 'высоким')
    logger.info(f'пользователь {user_id} запустил меню HIGH. state=high')
    bot.send_message(chat_id,
                     text=menu_header_text_rating(get_parameters(user_id)),
                     reply_markup=menu_set_filter_rating(),
                     parse_mode='HTML')


@bot.message_handler(commands=['low'])
def cmd_low_message(message) -> None:
    """
    обрабатывает команду /low -  вызывает соответствующее меню
    """
    menu_low(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'bt_low')
def bt_low_message(call: types.CallbackQuery) -> None:
    """
    обрабатывает нажатие кнопки 'фильмы с низким рейтингом' (аналог команды /low)
    вызывает соответствующее меню
    """
    bot.answer_callback_query(call.id)
    menu_low(call.from_user.id, call.message.chat.id)


@bot.message_handler(commands=['high'])
def cmd_high_message(message) -> None:
    """
    обрабатывает команду /high  -  вызывает соответствующее меню
    """
    menu_high(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'bt_high')
def bt_high_message(call: types.CallbackQuery) -> None:
    """
    обрабатывает нажатие кнопки 'фильмы с высоким рейтингом' (аналог команды /high)
    вызывает соответствующее меню
    """
    bot.answer_callback_query(call.id)
    menu_high(call.from_user.id, call.message.chat.id)


def menu_custom(user_id: int, chat_id: int) -> None:
    """
    устанавливает статус пользователю MyStates.custom
    выводит меню соответствующее команде /custom
    """
    bot.set_state(user_id, MyStates.custom, chat_id)
    create_filter_rating(user_id, '-1', 'заданным')
    logger.info(f'пользователь {user_id} запустил меню CUSTOM. state=custom')
    bot.send_message(chat_id,
                     text=menu_header_text_rating(get_parameters(user_id), state_user='cus'),
                     reply_markup=menu_set_filter_rating(state_user='cus'),
                     parse_mode='HTML')


@bot.message_handler(commands=['custom'])
def cmd_low_message(message) -> None:
    """
    обрабатывает команду /custom
    """
    menu_custom(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'bt_custom')
def bt_low_message(call: types.CallbackQuery) -> None:
    """
    обрабатывает нажатие кнопки 'инфо о фильмах по Вашим настройкам' (аналог команды /custom)
    вызывает соответствующее меню
    """
    bot.answer_callback_query(call.id)
    menu_custom(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'bt_ok_rating')
def process_callback_button_ok(call: types.CallbackQuery) -> None:
    """
    обрабатывает нажатие кнопки 'ОК выбор сделан' в меню выбора значений конкретного фильтра
    вызывает соответствующее меню
    """
    menu_button_rating(call)


@bot.callback_query_handler(func=lambda c: c.data.startswith('rating_type'))
def process_callback_type(call: types.CallbackQuery) -> None:
    """
    установка типа рейтинга фильмов
    """
    user_id = call.from_user.id
    number_bt = call.data[11:]
    if number_bt:
        set_parameters(user_id, 'rating_type', number_bt)
        set_parameters(user_id, 'm_rating_type', rating_menu[number_bt])
    markup_type = menu_check(rating_menu, get_parameters(user_id)['rating_type'], 'rating_type')
    message_check(call, "Выберете версию рейтинга:", markup_type)


@bot.callback_query_handler(func=lambda c: c.data == 'rating')
def process_callback_rating(call: types.CallbackQuery) -> None:
    """
    настройка фильтра рейтинг фильмов
    """
    user_id = call.from_user.id
    bot.set_state(user_id, MyStates.custom_rating_low, call.message.chat.id)
    logger.info(f'пользователь {user_id} задает диапазон рейтинга. state=custom_rating_low')
    bot.send_message(call.from_user.id, '📈 Задайте начальное значение рейтинга (от 0 до 10):')


@bot.callback_query_handler(func=lambda c: c.data.startswith('type'))
def process_callback_type(call: types.CallbackQuery) -> None:
    """
    настройка фильтра тип фильмов
    """
    user_id = call.from_user.id
    number = call.data[4:]
    if number:
        set_parameters(user_id, 'typeNumber', number)
        set_parameters(user_id, 'm_type', type_menu[number])
    markup_type = menu_check(type_menu, get_parameters(user_id)['typeNumber'], 'type')
    message_check(call, "Выберете тип фильма:", markup_type)


@bot.callback_query_handler(func=lambda c: c.data.startswith('countries'))
def process_callback_countries(call: types.CallbackQuery) -> None:
    """
    настройка фильтра страна фильма
    """
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    if bot.get_state(user_id) == MyStates.custom.name:
        bot.set_state(user_id, MyStates.custom_countries, call.message.chat.id)
        logger.info(f'пользователь {user_id} выбирает страну. state=custom_countries')
        bot.send_message(user_id, '🌐 Введите название страны')
        bot.send_message(user_id, 'Что бы снять фильтр введите любые символы')
    else:
        number = call.data[9:]
        if number:
            set_parameters(user_id, 'countries', number)
            set_parameters(user_id, 'm_countries', countries_menu[number])
        markup = menu_check(countries_menu, get_parameters(user_id)['countries'], 'countries')
        message_check(call, "Выберете страну:", markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith('year'))
def process_callback_year(call: types.CallbackQuery) -> None:
    """
    настройка фильтра год (годы) выхода фильмов
    """
    user_id = call.from_user.id
    if bot.get_state(user_id) == MyStates.custom.name:
        bot.set_state(user_id, MyStates.custom_year_low, call.message.chat.id)
        logger.info(f'пользователь {user_id} задает диапазон years. state=custom_year_low')
        text = '📆 Задайте начальный год (от 1890 до {}):'.format(datetime.now().year)
        bot.send_message(user_id, text)
    else:
        number = call.data[4:]
        if number:
            set_parameters(user_id, 'year', number)
            set_parameters(user_id, 'm_year', year_menu[number])
        markup = menu_check(year_menu, get_parameters(user_id)['year'], 'year')
        message_check(call, "Выберете год:", markup)


@bot.callback_query_handler(func=lambda c: c.data == 'bt_get')
def process_callback_get(call: types.CallbackQuery) -> None:
    """
    обработка нажатия кнопки 'Получить список фильмов'
    вызывает процедуру получения данных с API сайта
    и обрабатывает ответ
    """
    user_id = call.from_user.id
    result, movies_response = api_request(text_query_rating(user_id), url_address='v1.3/movie?')
    bot.answer_callback_query(call.id)
    if result:
        movies = movies_response['docs']
        if len(movies) == 0:
            logger.warning(f'пользователь {user_id}  на запрос вернулся пустой список-')
            bot.send_message(user_id, 'Список пуст!.\n Попробуйте изменить условия поиска')
        else:
            print_movies(call, movies)
    else:
        logger.error(f'пользователь {user_id} ошибка обработки запроса')
        bot.send_message(user_id, 'Что-то пошло не так.\n Попробуйте ещё раз позже')
    # rating = True if bot.get_state(user_id) == MyStates.custom.name else False
    bot.send_message(call.message.chat.id,
                     text=menu_header_text_rating(get_parameters(user_id), bot.get_state(user_id)[9:12]),
                     reply_markup=menu_set_filter_rating(bot.get_state(user_id)[9:12]),
                     parse_mode='HTML')
