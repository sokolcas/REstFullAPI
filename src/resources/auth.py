from flask_restful import Resource
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from functools import wraps

from src.database.models import User
from src.schemas.users import UserSchema
from src import db, app

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
import jwt
from werkzeug.security import check_password_hash

class AuthRegister(Resource):
    user_schema= UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Such user exists"}, 409
        return self.user_schema.dump(user), 201

class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user= User.find_user_by_username(auth.get('username', ''))
        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY']
        )
        return jsonify(
            {
                "token": token
            }
        )

# напишем декоратор, чтобы определенные методы ресурса были доступны только аутентифицированными пользователями
def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except (KeyError, jwt.ExpiredSignatureError): #значит время жизни токена
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = db.session.query(User).filter_by(uuid=uuid).first()
        user = User.find_user_by_uuid(uuid)
        if not user:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper