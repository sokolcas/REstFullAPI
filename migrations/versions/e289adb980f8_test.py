"""test

Revision ID: e289adb980f8
Revises: 848d966a0743
Create Date: 2021-10-04 14:09:33.180458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e289adb980f8'
down_revision = '848d966a0743'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films', sa.Column('test', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('films', 'test')
    # ### end Alembic commands ###
