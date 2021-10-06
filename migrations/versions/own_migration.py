"""test

Revision ID: e289adb980f9
Revises: 848d966a0743
Create Date: 2021-10-04 14:09:33.180458

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'e289adb980f9'
down_revision = 'e289adb980f8'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind() # получаем коннекшн к бд
    conn.execute( # выполнить 
        text(
        """ 
            UPDATE films
            SET test = 100
            WHERE title like '%Harry%' 
        """
        ) # %Harry% титл содержит этот набор букв, не в точности
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                UPDATE films
                SET test = NULL
                WHERE title like '%Harry%'
            """
        )
    )