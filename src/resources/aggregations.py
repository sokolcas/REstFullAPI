from flask_restful import Resource
from src import db
from src.database.models import Film
from sqlalchemy import func # чтобы использовать аггрегативные функции

class AggregationApi(Resource):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar() # считаем фильмы по id и возвращаем значение
        max_rating= db.session.query(func.max(Film.rating)).scalar() # максимальный рейтинг
        min_rating= db.session.query(func.min(Film.rating)).scalar() # минимальный
        avg_rating= db.session.query(func.avg(Film.rating)).scalar() # средний
        sum_rating= db.session.query(func.sum(Film.rating)).scalar() # сумма всех рейтингов
        return {
            'count': films_count,
            'max': max_rating,
            'min': min_rating,
            'avg': avg_rating,
            'sum':sum_rating
        }