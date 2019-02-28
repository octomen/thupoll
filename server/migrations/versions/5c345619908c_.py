"""empty message

Revision ID: 5c345619908c
Revises: 
Create Date: 2019-02-28 23:48:09.111475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c345619908c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('telegram_login', sa.String(), nullable=False),
                    sa.Column('created_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('change_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('role_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('poll',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('expire_date', sa.DateTime(), nullable=False),
                    sa.Column('created_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('change_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('role',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('theme',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('author_id', sa.Integer(), nullable=False),
                    sa.Column('reporter_id', sa.Integer(), nullable=False),
                    sa.Column('status_id', sa.Integer(), nullable=False),
                    sa.Column('created_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('change_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('theme_poll',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('theme_id', sa.Integer(), nullable=False),
                    sa.Column('poll_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('theme_status',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('volume',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('change_date', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('themepoll_id', sa.Integer(), nullable=False),
                    sa.Column('people_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('volume')
    op.drop_table('theme_status')
    op.drop_table('theme_poll')
    op.drop_table('theme')
    op.drop_table('role')
    op.drop_table('poll')
    op.drop_table('people')
    # ### end Alembic commands ###
