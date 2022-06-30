"""add content column to post table

Revision ID: 00ddb92f3521
Revises: 8bd66e1776f3
Create Date: 2022-06-30 07:07:13.478723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ddb92f3521'
down_revision = '8bd66e1776f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # example of adding a column in alembic
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    # dropping a column
    op.drop_column('posts', 'content')
    pass
