"""Add custom words

Revision ID: f8979d84803f
Revises: f9352935298d
Create Date: 2023-07-26 04:37:08.068009

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f8979d84803f'
down_revision = 'f9352935298d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('custom_words',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('word', sa.VARCHAR(length=7), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__custom_words')),
    sa.UniqueConstraint('word', name=op.f('uq__custom_words__word'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('custom_words')
    # ### end Alembic commands ###
