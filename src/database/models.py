from enum import unique
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import db
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


movies_actors=db.Table( #создали таблицу общую
    'movies_actor',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('films.id'), primary_key=True)
)

class Film(db.Model):
    __tablename__ = 'films'
    
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120), nullable = False) # null- может ли поле быть пустым
    release_date = db.Column(db.Date, index = True, nullable = False)
    uuid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.Text)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)
    test = db.Column(db.Float)
    actors=db.relationship('Actor', secondary=movies_actors, lazy=True, backref=db.backref('films', lazy=True)) # создали отношение
    # backref= у каждого актера теперь есть поле films, в котором указано, в каких фильмах снимались актеры.
    # lazy = отложенная загрузка, чтобы память не убивать . subquery для решения N+1 проблемы. 
    

    
    def __init__(self, title, release_date, description, distributed_by, length, rating, actors = None):
        self.title = title
        self.release_date = release_date
        self.uuid = str(uuid.uuid4())
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        if not actors:
            self.actors=[]
        else:
            self.actors=actors

    def __repr__(self):
        return f'Film({self.title}, {self.release_date}, {self.uuid}, {self.distributed_by}, {self.rating}, {self.actors}'
    
    def patching(patcher, object_to_patch):
        title=patcher.get('title') 
        release_date= datetime.strptime(patcher.get('release_date'), '%B %d %Y') if patcher.get('release date') else None 
        distributed_by=patcher.get('distributed_by')
        description=patcher.get('description')
        length=patcher.get('length')
        rating=patcher.get('rating')

        if title:
            object_to_patch.title = title
        elif release_date:
            object_to_patch.release_date = release_date
        elif distributed_by:
            object_to_patch.distributed_by = distributed_by
        elif description:
            object_to_patch.description = description
        elif length:
            object_to_patch.length = length
        elif rating:
            object_to_patch.rating = rating
            
        return (object_to_patch)


class Actor(db.Model):
    __tablename__='actors' #название таблички в бд 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    birthday= db.Column(db.Date)
    is_active= db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Actor({self.name}, {self.birthday})'

    def patching(patcher, object_to_patch):

        name=patcher.get('name') 
        birthday= datetime.strptime(patcher.get('birthday'), '%B %d %Y') if patcher.get('birthday') else None 
        is_active=patcher.get('is_active')

        if name:
            object_to_patch.name = name
        elif birthday:
            object_to_patch.birthday = birthday
        elif is_active:
            object_to_patch.is_active = is_active
            
        return (object_to_patch)


class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    is_admin=db.Column(db.Boolean, default=False)
    uuid=db.Column(db.String(36), unique=True)

    def __init__(self, username, email, password, is_admin=False):
            self.username=username
            self.email=email
            self.password=generate_password_hash(password)
            self.is_admin=is_admin
            self.uuid=str(uuid.uuid4())

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.uuid})'

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_user_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()
