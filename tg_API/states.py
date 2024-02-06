from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """
    статусы пользователя
    """
    start = State()
    low = State()
    high = State()
    history = State()
    custom = State()
    custom_year_low = State()
    custom_year_high = State()
    custom_rating_low = State()
    custom_rating_high = State()
    custom_countries = State()
