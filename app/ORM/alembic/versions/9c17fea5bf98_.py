"""add last few columns

Revision ID: 9c17fea5bf98
Revises: d020d9fdc304
Create Date: 2022-06-30 08:53:51.688134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c17fea5bf98'
down_revision = 'd020d9fdc304'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean,
                    nullable = False, server_default = 'TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        nullable=False, server_default = sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
