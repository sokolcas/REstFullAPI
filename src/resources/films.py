from flask_restful import Resource
from flask import request
from sqlalchemy.orm import joinedload
from src import db
from src.resources.auth import token_required
from src.schemas.films import FilmSchema
from marshmallow import ValidationError
from src.database.models import Film
from src.services.film_service import FilmService


class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session).options(
                joinedload(Film.actors)  # для решения N+1 подгружаем сразу
            ).all()  # Получаем все записи из db
            return self.film_schema.dump(films, many=True), 200
        film = FilmService.fetch_film_by_uuid(
            db.session, uuid)  # фильтруем по uuid
        if not film:
            return '', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    def put(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return {'message': 'Wrong data'}, 404
        try:
            film = self.film_schema.load(
                request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        # 200 означает был изменен ресурс
        return self.film_schema.dump(film), 200

    def patch(self, uuid):  # В PATCH меняем только один параметр за раз!

        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 400

        film_json = request.json
        film = Film.patching(film_json, film)

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    def delete(self, uuid=None):
        if not uuid:
            db.session.query(Film).delete()  # Получаем все записи из db
            db.session.commit()
            return '', 205
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 400
        db.session.delete(film)  # команда удаления из дб
        db.session.commit()
        return '', 204  # фильм удален
