from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.database.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['id', 'is_admin']
        load_instance = True
        # какое поле не будет возращаться после создания.
        load_only = ('password',)
