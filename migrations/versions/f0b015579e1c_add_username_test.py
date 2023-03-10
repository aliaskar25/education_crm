"""add username test

Revision ID: f0b015579e1c
Revises: f43bd16cca4c
Create Date: 2023-03-02 14:43:32.192404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0b015579e1c'
down_revision = 'f43bd16cca4c'
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
