
from flask_restful import Resource
from flask import request
from src import db
from src.schemas.actors import ActorSchema
from marshmallow import ValidationError
from src.database.models import Actor


class ActorListApi(Resource):
    actor_schema = ActorSchema()

    def get(self, id=None):
        if not id:
            actors = db.session.query(Actor).all()  # Получаем все записи из db
            return self.actor_schema.dump(actors, many=True), 200
        actor = db.session.query(Actor).filter_by(
            id=id).first()  # фильтруем по id
        if not actor:
            return '', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    def put(self, id):
        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return {'message': 'Wrong data'}, 404
        try:
            actor = self.actor_schema.load(
                request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(actor)
        db.session.commit()
        # 200 означает был изменен ресурс
        return self.actor_schema.dump(actor), 200

    def patch(self, id):  # В PATCH меняем только один параметр за раз!

        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return '', 400

        actor_json = request.json
        actor = Actor.patching(actor_json, actor)

        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    def delete(self, id=None):
        if not id:
            db.session.query(Actor).delete()  # Получаем все записи из db
            db.session.commit()
            return '', 205
        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return '', 400
        db.session.delete(actor)  # команда удаления из дб
        db.session.commit()
        return '', 204  # фильм удален
