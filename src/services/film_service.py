from src.database.models import Film
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class FilmService:
    @staticmethod
    def fetch_all_films(session):
        return session.query(Film)

    @classmethod
    def fetch_film_by_uuid(cls, session, uuid):
        return cls.fetch_all_films(session).filter_by(
            uuid=uuid
        ).first()
