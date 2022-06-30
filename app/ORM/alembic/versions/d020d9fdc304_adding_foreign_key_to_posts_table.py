"""Adding foreign key to posts table

Revision ID: d020d9fdc304
Revises: e5a49bbe7306
Create Date: 2022-06-30 08:41:55.097158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd020d9fdc304'
down_revision = 'e5a49bbe7306'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    # Create a foreign key with owners_id in posts referenced from id in users
    op.create_foreign_key('post_users_fk', source_table= "posts",
                            referent_table="users", local_cols=['owner_id'],
                            remote_cols=['id'], 
                            ondelete='CASCADE')
    pass


def downgrade() -> None:
    # drop foreign key
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
