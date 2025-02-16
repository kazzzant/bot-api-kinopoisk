# БОТ показывает рейтинг фильмов с API КиноПоиск

Бот формиует списки фильмов с наибольшим и с наименьшим рейтингами, а также в соответствии с настройками пользователя.
Есть возможжность установить следующие фильтры:
>* 📈 тип рейтинга
>* 🌐 страна фильма
>* ️🎬 тип фильма
>* 📆 год фильма

После запуска бота пользователю предлагается выбрать из кнопочного меню варианты:
>* ️🎬  фильмы с низким рейтингом
>* ️️🎬  фильмы с высоким рейтингом
>* ️🎬  инфо о фильмах по Вашим настройкам
>* 📜  история запросов

Пользователь может нажать на кнопку или ввести соответствующую команду /low, /high, /custom, /history. 
Далее пользователю будет предложено меню с настройками фильтра
>* ⚙️ Изменить тип рейтинга
>* ⚙️ Значение рейтинга (для режима /custom)
>* ⚙️ Выбрать тип фильма
>* ⚙️  Выбрать страну
>* ⚙️  Установить год
>* 📽️  Получить список фильмов
>* ↖️  В главное меню

При выборе соответствующего меню, пользователю будет предложено задать конкретные значения фильтров

При нажатии кнопки:
>📽️  Получить список фильмов
> 
бот выводит на экран список фильмов соответствующих настройкам пользователя

При нажатии кнопки:
>
>📜  история запросов 
> 
бот выводит на экран последние 10 запросов пользователя

При вводе команды /help бот выведет на экран сообщение с описанием команд.

Программа поддерживает многопользовательский режим, ведёт логирование и запоминает запросы пользователя в базе данных

Программа написана на языке Python 3.11 c использованием следующих библиотек:

>* pyTelegramBotAPI 4.10.0
>* requests 2.30.0
>* loguru 0.7.0
>* python-dotenv 1.0.0
>* peewee 3.16.2
