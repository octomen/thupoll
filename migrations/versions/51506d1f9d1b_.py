"""empty message

Revision ID: 51506d1f9d1b
Revises: 850a36268e3a
Create Date: 2019-03-31 06:48:27.652357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51506d1f9d1b'
down_revision = '850a36268e3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('theme_poll', sa.Column('order_no', sa.Integer(), nullable=False))
    op.create_index('theme_poll_poll_id_order_no_uidx', 'theme_poll', ['poll_id', 'order_no'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('theme_poll_poll_id_order_no_uidx', table_name='theme_poll')
    op.drop_column('theme_poll', 'order_no')
    # ### end Alembic commands ###