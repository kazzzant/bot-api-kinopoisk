from telebot import types


def menu_begin() -> types.InlineKeyboardMarkup:
    """
    формирует кнопки стартового меню
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("️🎬  фильмы с низким рейтингом ", callback_data='bt_low'))
    markup.add(types.InlineKeyboardButton("️️🎬  фильмы с высоким рейтингом", callback_data='bt_high'))
    markup.add(types.InlineKeyboardButton("️🎬  инфо о фильмах по Вашим настройкам", callback_data='bt_custom'))
    markup.add(types.InlineKeyboardButton("📜  история запросов", callback_data='bt_history'))

    return markup


def menu_check(my_variants: dict, param: str, field: str) -> types.InlineKeyboardMarkup:
    """
    формирует меню в виде кнопок для выбора значений заданного фильтра
    :param my_variants: dict справочник с вариантами значений фильтра
    :param param: str  текущее значение фильтра
    :param field: str определяет имя параметра фильтра с которым работает пользователь
    :return:
    """
    buttons = []
    markup = types.InlineKeyboardMarkup(row_width=2)
    for key, value in my_variants.items():
        emoji = '✔️ ' if key == param else '🔵 '
        button = types.InlineKeyboardButton(emoji + value, callback_data=field + key)
        buttons.append(button)
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton('<<  🆗, выбор сделан', callback_data='bt_ok_rating'))

    return markup


def menu_header_text_rating(menu_parameters: dict, state_user: str = '') -> str:
    """
    :param menu_parameters: dict параметры фильтра пользователя
    :param state_user: str если режим - /custom, то добавляет строку со значением фильтра рейтинг
    :return: str  возвращает текстовый заголовок с указанием текущих настроек фильтра
    """
    rating_text = ''
    if state_user == 'cus':
        rating_text = f" 🔹️ рейтинг <b>{menu_parameters['m_rating']}</b>\n"
    text = ("<b> Фильмы и передачи с {m_sort} рейтингом </b>\n"            
            " 🔹️ по версии  <b>{m_rating_type}</b>\n {rating_text}"
            " 🔹️ тип фильма:  <b>{m_type}</b>\n"
            " 🔹️ страна:  <b>{m_countries}</b>\n"
            " 🔹️ год:  <b>{m_year}</b>".format(rating_text=rating_text, **menu_parameters))
    return text


def menu_set_filter_rating(state_user: str = '') -> types.InlineKeyboardMarkup:
    """
    возвращает меню в виде кнопок для выбора имени параметра фильтра
    :param state_user: str если режим - /custom, то добавляет строку для выбора фильтра рейтинг
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⚙️ Изменить тип рейтинга", callback_data='rating_type'))
    if state_user == 'cus':
        markup.add(types.InlineKeyboardButton("⚙️ Значение рейтинга", callback_data='rating'))
    markup.add(types.InlineKeyboardButton("⚙️ Выбрать тип фильма", callback_data='type'))
    markup.add(types.InlineKeyboardButton("⚙️  Выбрать страну", callback_data='countries'))
    markup.add(types.InlineKeyboardButton("⚙️  Установить год", callback_data='year'))
    markup.add(types.InlineKeyboardButton("📽️  Получить список фильмов", callback_data='bt_get'))
    markup.add(types.InlineKeyboardButton("↖️  В главное меню", callback_data='start'))

    return markup
