"""add username

Revision ID: 9130dd1cccef
Revises: e787c15a9303
Create Date: 2023-02-28 16:46:29.706610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9130dd1cccef'
down_revision = 'e787c15a9303'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
