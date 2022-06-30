"""add phone number

Revision ID: 73a950ddc041
Revises: 50419b4c3f61
Create Date: 2022-06-30 09:11:23.995598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73a950ddc041'
down_revision = '50419b4c3f61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###