"""remove field username

Revision ID: e65394e4dbea
Revises: 9130dd1cccef
Create Date: 2023-03-01 17:02:16.714881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e65394e4dbea'
down_revision = '9130dd1cccef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
