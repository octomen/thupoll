"""empty message

Revision ID: a189ed3ee2df
Revises: 15500d089742
Create Date: 2019-03-17 14:52:22.523877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a189ed3ee2df'
down_revision = '15500d089742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('theme', 'reporter_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('theme', 'reporter_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
