from peewee import Model, SqliteDatabase, IntegerField, CharField, DateTimeField
import datetime
import os.path

rel_path = os.path.join("database", "history.db")
abs_path = os.path.abspath(rel_path)
db = SqliteDatabase(abs_path)


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
    """
    Модель базы данных для хранения истории запросов
    Поля соответствуют параметам фильтра
    """
    user_id = IntegerField()
    date = DateTimeField(default=datetime.datetime.now)
    state = CharField()
    sortType = CharField()
    rating_type = CharField()
    rating = CharField()
    typeNumber = CharField()
    countries = CharField()
    year = CharField()
    m_sort = CharField()
    m_rating_type = CharField()
    m_rating = CharField()
    m_type = CharField()
    m_countries = CharField()
    m_year = CharField()


with db:
    History.create_table()
