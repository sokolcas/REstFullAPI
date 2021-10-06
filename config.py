import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # отключаем функцию о сигнализировании приложению, когда должны быть изменения
    SECRET_KEY = 'you-will-never-know'
