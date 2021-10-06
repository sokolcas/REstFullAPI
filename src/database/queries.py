""" -- SELECT QUERIES --  """
""" import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) """
from operator import and_
from src import db
from database import models
from sqlalchemy import and_

def run():
   # films=db.session.query(models.Film).all() #ПОлучаем все модели
    films=db.session.query(models.Film).order_by(models.Film.rating).all() #Sort by rating from min to max
    films=db.session.query(models.Film).order_by(models.Film.rating.desc()).all()# From max to min
    harry_potter = db.session.query(models.Film).filter(
        models.Film.title == 'Harry Potter'
    ).first() # фильтруем по параметру и получаем первый фильм. filter в сложных запросах, filter_by где +- один критерий
    american_pie = db.session.query(models.Film).filter_by(
        title = 'American Pie'
    ).first() 
    films
    and_statement_harry_potter= db.session.query(models.Film).filter(
        models.Film.title != 'American Pie' ,# Все, кроме 
        models.Film.rating >= 7.5 # rating >= 7.5
    ).all()
    and_statement_american_pie= db.session.query(models.Film).filter(
        and_(  # функция фильтра от sqlalchemy, непонятно нафига
        models.Film.title != 'Harry Pitter' ,# Все, кроме 
        models.Film.rating >= 7.5, # rating >= 7.5
        models.Film.title.like('The second part'), # Поик по тексту в тайтле, учитывая регистр, вывели бы все вторые части
        models.Film.title.ilike('the second part'), # не учитывая регистр 
        )
    ).all()
    sorted_by_length= db.session.query(models.Film).filter(
        models.Film.length.in_([152,161])).all(), # фильмы с длиной 152 или 161
    sorted_by_length2= db.session.query(models.Film).filter(
        models.Film.length.in_([152,161]))[:2], # можно использовать слайсы и возвращать 2 фильма 

    """QUERING WITH JOINS """
    
    film_with_actors = db.session.query(models.Film).join(models.Film.actors).all()
    # так мы присоединили две таблицы
    a= db.session.query(models.Actor).first()
    a.films # так мы вызвали backref и знаем в каких фильмах снимался актер
    print(a.films)
