from loader import bot

import tg_API.state_handlers


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
