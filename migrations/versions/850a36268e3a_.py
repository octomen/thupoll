"""empty message

Revision ID: 850a36268e3a
Revises: 6c8c9eae800c
Create Date: 2019-03-30 21:45:23.244858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '850a36268e3a'
down_revision = '6c8c9eae800c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO theme_status (id, name) VALUES (2, 'planned')")


def downgrade():
    op.execute("DELETE FROM theme_status WHERE id = 2")
