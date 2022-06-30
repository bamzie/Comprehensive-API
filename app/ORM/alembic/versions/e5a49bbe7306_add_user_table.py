"""add user table

Revision ID: e5a49bbe7306
Revises: 00ddb92f3521
Create Date: 2022-06-30 07:11:51.823244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a49bbe7306'
down_revision = '00ddb92f3521'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),        
                    sa.UniqueConstraint('email')
                    )
                    

    pass


def downgrade() -> None:
    # Dop users table
    op.drop_table('users')
    pass
