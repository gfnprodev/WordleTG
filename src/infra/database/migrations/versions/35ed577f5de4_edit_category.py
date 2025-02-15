"""edit category

Revision ID: 35ed577f5de4
Revises: ba364296b44a
Create Date: 2023-07-25 15:28:27.816745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35ed577f5de4'
down_revision = 'ba364296b44a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categorys', sa.Column('description', sa.TEXT(), nullable=False, server_default="description"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categorys', 'description')
    # ### end Alembic commands ###
