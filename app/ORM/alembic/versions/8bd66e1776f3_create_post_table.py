"""create post table

Revision ID: 8bd66e1776f3
Revises: 
Create Date: 2022-06-30 06:56:09.992517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bd66e1776f3'
down_revision = None
branch_labels = None
depends_on = None

# You must always have an upgrade()
# and downgrade() in Alembic

def upgrade() -> None:
    # This is how you create a table in alembic
    # similar structure to sqlalchemy just with op
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key= True),
                    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    # Drop posts table
    op.drop_table('posts')
    pass
